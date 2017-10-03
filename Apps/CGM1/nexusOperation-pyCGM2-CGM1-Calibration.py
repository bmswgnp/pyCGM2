# -*- coding: utf-8 -*-
#import ipdb
import logging
import matplotlib.pyplot as plt
import argparse


# pyCGM2 settings
import pyCGM2
pyCGM2.CONFIG.setLoggingLevel(logging.INFO)

# vicon nexus
import ViconNexus

# pyCGM2 libraries
from pyCGM2.Tools import btkTools
import pyCGM2.enums as pyCGM2Enums

from pyCGM2.Model import modelFilters, modelDecorator
from pyCGM2.Model.CGM2 import cgm

from pyCGM2.Utils import files
from pyCGM2.Nexus import nexusFilters, nexusUtils,nexusTools

if __name__ == "__main__":

    plt.close("all")
    DEBUG = False

    parser = argparse.ArgumentParser(description='CGM1 Calibration')
    parser.add_argument('-l','--leftFlatFoot', type=int, help='left flat foot option')
    parser.add_argument('-r','--rightFlatFoot',type=int,  help='right flat foot option')
    parser.add_argument('-md','--markerDiameter', type=float, help='marker diameter')
    parser.add_argument('-ps','--pointSuffix', type=str, help='suffix of model outputs')
    parser.add_argument('--check', action='store_true', help='force model output suffix' )
    parser.add_argument('--resetMP', action='store_false', help='reset optional mass parameters')
    args = parser.parse_args()

    NEXUS = ViconNexus.ViconNexus()
    NEXUS_PYTHON_CONNECTED = NEXUS.Client.IsConnected()


    if NEXUS_PYTHON_CONNECTED: # run Operation

        # --------------------------GLOBAL SETTINGS ------------------------------------
        # global setting ( in user/AppData)
        settings = files.openJson(pyCGM2.CONFIG.PYCGM2_APPDATA_PATH,"CGM1-pyCGM2.settings")

        # --------------------------LOADING ------------------------------------
        if DEBUG:
            DATA_PATH = pyCGM2.CONFIG.TEST_DATA_PATH + "CGM1\\CGM1-NexusPlugin\\pyCGM2- CGM1-KAD\\"
            calibrateFilenameLabelledNoExt = "Gait Trial 02" #"static Cal 01-noKAD-noAnkleMed" #
            NEXUS.OpenTrial( str(DATA_PATH+calibrateFilenameLabelledNoExt), 30 )

        else:
            DATA_PATH, calibrateFilenameLabelledNoExt = NEXUS.GetTrialName()

        calibrateFilenameLabelled = calibrateFilenameLabelledNoExt+".c3d"

        logging.info( "data Path: "+ DATA_PATH )
        logging.info( "calibration file: "+ calibrateFilenameLabelled)

        # --------------------------SUBJECT ------------------------------------
        subjects = NEXUS.GetSubjectNames()
        subject = nexusTools.checkActivatedSubject(NEXUS,subjects)
        Parameters = NEXUS.GetSubjectParamNames(subject)

        required_mp,optional_mp = nexusUtils.getNexusSubjectMp(NEXUS,subject,resetFlag=args.resetMP)

        # --------------------------SESSION INFOS ------------------------------------
        # info file
        info = files.manage_pycgm2SessionInfos(DATA_PATH,subject)

        #  translators management
        translators = files.manage_pycgm2Translators(DATA_PATH,"CGM1.translators")
        if not translators:
           translators = settings["Translators"]

        # --------------------------CONFIG ------------------------------------
        if args.leftFlatFoot is not None:
            flag_leftFlatFoot = bool(args.leftFlatFoot)
            logging.warning("Left flat foot forces : %s"%(str(bool(args.leftFlatFoot))))
        else:
            flag_leftFlatFoot = bool(settings["Calibration"]["Left flat foot"])


        if args.rightFlatFoot is not None:
            flag_rightFlatFoot = bool(args.rightFlatFoot)
            logging.warning("Right flat foot forces : %s"%(str(bool(args.rightFlatFoot))))
        else:
            flag_rightFlatFoot =  bool(settings["Calibration"]["Right flat foot"])


        if args.markerDiameter is not None:
            markerDiameter = float(args.markerDiameter)
            logging.warning("marker diameter forced : %s", str(float(args.markerDiameter)))
        else:
            markerDiameter = float(settings["Global"]["Marker diameter"])


        if args.check:
            pointSuffix="cgm1.0"
        else:
            if args.pointSuffix is not None:
                pointSuffix = args.pointSuffix
            else:
                pointSuffix = settings["Global"]["Point suffix"]

        # --------------------------ACQUISITION ------------------------------------

        # ---btk acquisition---
        acqStatic = btkTools.smartReader(str(DATA_PATH+calibrateFilenameLabelled))
        btkTools.checkMultipleSubject(acqStatic)

        acqStatic =  btkTools.applyTranslators(acqStatic,translators)

        # ---definition---
        model=cgm.CGM1LowerLimbs()
        model.configure()

        model.setStaticFilename(calibrateFilenameLabelled)
        model.addAnthropoInputParameters(required_mp,optional=optional_mp)


        # ---check marker set used----
        staticMarkerConfiguration= cgm.CGM.checkCGM1_StaticMarkerConfig(acqStatic)


        # --------------------------STATIC CALBRATION--------------------------
        scp=modelFilters.StaticCalibrationProcedure(model) # load calibration procedure

        # ---initial calibration filter----
        # use if all optional mp are zero
        modelFilters.ModelCalibrationFilter(scp,acqStatic,model,
                                            leftFlatFoot = flag_leftFlatFoot, rightFlatFoot = flag_rightFlatFoot,
                                            markerDiameter=markerDiameter,
                                            ).compute()
        # ---- Decorators -----
        # Goal = modified calibration according the identified marker set or if offsets manually set

        # initialisation of node label and marker labels
        # hip joint centres ---
        useLeftHJCnodeLabel = "LHJC_cgm1"
        useRightHJCnodeLabel = "RHJC_cgm1"

        useLeftKJCnodeLabel = "LKJC_chord"
        useLeftAJCnodeLabel = "LAJC_chord"
        useRightKJCnodeLabel = "RKJC_chord"
        useRightAJCnodeLabel = "RAJC_chord"

        useLeftKJCmarkerLabel = "LKJC"
        useLeftAJCmarkerLabel = "LAJC"
        useRightKJCmarkerLabel = "RKJC"
        useRightAJCmarkerLabel = "RAJC"


        # case 1 : NO kad, NO medial ankle BUT thighRotation different from zero ( mean manual modification or new calibration from a previous one )
        #  case not necessary - static PIG operation - dont consider any offsets
        if not staticMarkerConfiguration["leftKadFlag"]  and not staticMarkerConfiguration["leftMedialAnkleFlag"] and not staticMarkerConfiguration["leftMedialKneeFlag"] and optional_mp["LeftThighRotation"] !=0:
            logging.warning("CASE FOUND ===> Left Side - CGM1 - Origine - manual offsets")
            modelDecorator.Cgm1ManualOffsets(model).compute(acqStatic,"left",optional_mp["LeftThighRotation"],markerDiameter,optional_mp["LeftTibialTorsion"],optional_mp["LeftShankRotation"])
            useLeftKJCnodeLabel = "LKJC_mo"
            useLeftAJCnodeLabel = "LAJC_mo"


        if not staticMarkerConfiguration["rightKadFlag"]  and not staticMarkerConfiguration["rightMedialAnkleFlag"] and not staticMarkerConfiguration["rightMedialKneeFlag"] and optional_mp["RightThighRotation"] !=0:
            logging.warning("CASE FOUND ===> Right Side - CGM1 - Origine - manual offsets")
            modelDecorator.Cgm1ManualOffsets(model).compute(acqStatic,"right",optional_mp["RightThighRotation"],markerDiameter,optional_mp["RightTibialTorsion"],optional_mp["RightShankRotation"])
            useRightKJCnodeLabel = "RKJC_mo"
            useRightAJCnodeLabel = "RAJC_mo"

        # case 2 : kad FOUND and NO medial Ankle
        if staticMarkerConfiguration["leftKadFlag"]:
            logging.warning("CASE FOUND ===> Left Side - CGM1 - KAD variant")
            modelDecorator.Kad(model,acqStatic).compute(markerDiameter=markerDiameter, side="left")
            useLeftKJCnodeLabel = "LKJC_kad"
            useLeftAJCnodeLabel = "LAJC_kad"

            useLeftKJCmarkerLabel = "LKJC_KAD"
            useLeftAJCmarkerLabel = "LAJC_KAD"

        if staticMarkerConfiguration["rightKadFlag"]:
            logging.warning("CASE FOUND ===> Right Side - CGM1 - KAD variant")
            modelDecorator.Kad(model,acqStatic).compute(markerDiameter=markerDiameter, side="right")
            useRightKJCnodeLabel = "RKJC_kad"
            useRightAJCnodeLabel = "RAJC_kad"

            useRightKJCmarkerLabel = "RKJC_KAD"
            useRightAJCmarkerLabel = "RAJC_KAD"


        # case 3 : both kad and medial ankle FOUND
        if staticMarkerConfiguration["leftKadFlag"]:
            if staticMarkerConfiguration["leftMedialAnkleFlag"]:
                logging.warning("CASE FOUND ===> Left Side - CGM1 - KAD + medial ankle ")
                modelDecorator.AnkleCalibrationDecorator(model).midMaleolus(acqStatic, markerDiameter=markerDiameter, side="left")
                useLeftAJCnodeLabel = "LAJC_mid"

                useLeftAJCmarkerLabel = "LAJC_MID"


        if staticMarkerConfiguration["rightKadFlag"]:
            if staticMarkerConfiguration["rightMedialAnkleFlag"]:
                logging.warning("CASE FOUND ===> Right Side - CGM1 - KAD + medial ankle ")
                modelDecorator.AnkleCalibrationDecorator(model).midMaleolus(acqStatic, markerDiameter=markerDiameter, side="right")
                useRightAJCnodeLabel = "RAJC_mid"

                useRightAJCmarkerLabel = "RAJC_MID"

        properties_initialCalibration=dict()
        properties_initialCalibration["LHJC_node"] = useLeftHJCnodeLabel
        properties_initialCalibration["RHJC_node"] = useRightHJCnodeLabel
        properties_initialCalibration["LKJC_node"] = useLeftKJCnodeLabel
        properties_initialCalibration["RKJC_node"] = useRightKJCnodeLabel
        properties_initialCalibration["LAJC_node"] = useLeftAJCnodeLabel
        properties_initialCalibration["RAJC_node"] = useRightAJCnodeLabel
        properties_initialCalibration["rightFlatFoot"] = useRightAJCnodeLabel
        properties_initialCalibration["leftFlatFoot"] = flag_rightFlatFoot
        properties_initialCalibration["markerDiameter"] = markerDiameter


        # ----Final Calibration filter if model previously decorated -----
        if model.decoratedModel:
            # initial static filter
            modelFilters.ModelCalibrationFilter(scp,acqStatic,model,
                               useLeftKJCnode=useLeftKJCnodeLabel, useLeftAJCnode=useLeftAJCnodeLabel,
                               useRightKJCnode=useRightKJCnodeLabel, useRightAJCnode=useRightAJCnodeLabel,
                               leftFlatFoot = flag_leftFlatFoot, rightFlatFoot = flag_rightFlatFoot,
                               markerDiameter=markerDiameter).compute()

        # set initial calibration as model property
        model.m_properties["CalibrationParameters0"] = properties_initialCalibration


        # ----------------------CGM MODELLING----------------------------------
        # ----motion filter----
        # notice : viconCGM1compatible option duplicate error on Construction of the foot coordinate system

        modMotion=modelFilters.ModelMotionFilter(scp,acqStatic,model,pyCGM2Enums.motionMethod.Determinist,
                                                  markerDiameter=markerDiameter,
                                                  viconCGM1compatible=False,
                                                  pigStatic=True,
                                                  useRightKJCmarker=useRightKJCmarkerLabel, useRightAJCmarker=useRightAJCmarkerLabel,
                                                  useLeftKJCmarker=useLeftKJCmarkerLabel, useLeftAJCmarker=useLeftAJCmarkerLabel)
        modMotion.compute()


        #---- Joint kinematics----
        # relative angles
        modelFilters.ModelJCSFilter(model,acqStatic).compute(description="vectoriel", pointLabelSuffix=pointSuffix)

        # detection of traveling axis
        longitudinalAxis,forwardProgression,globalFrame = btkTools.findProgressionAxisFromPelvicMarkers(acqStatic,["LASI","RASI","RPSI","LPSI"])


        # absolute angles
        modelFilters.ModelAbsoluteAnglesFilter(model,acqStatic,
                                               segmentLabels=["Left Foot","Right Foot","Pelvis"],
                                                angleLabels=["LFootProgress", "RFootProgress","Pelvis"],
                                                eulerSequences=["TOR","TOR", "TOR"],
                                                globalFrameOrientation = globalFrame,
                                                forwardProgression = forwardProgression).compute(pointLabelSuffix=pointSuffix)



        # ----------------------SAVE-------------------------------------------
        #pyCGM2.model
        files.saveModel(model,DATA_PATH,subject)

        # ----------------------DISPLAY ON VICON-------------------------------
        nexusUtils.updateNexusSubjectMp(NEXUS,model,subject)
        nexusFilters.NexusModelFilter(NEXUS,
                                      model,acqStatic,subject,
                                      pointSuffix,
                                      staticProcessing=True).run()

        # ========END of the nexus OPERATION if run from Nexus  =========

        if DEBUG:
            NEXUS.SaveTrial(30)
    else:
        raise Exception("NO Nexus connection. Turn on Nexus")
