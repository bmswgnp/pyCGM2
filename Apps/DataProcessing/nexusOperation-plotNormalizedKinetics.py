# -*- coding: utf-8 -*-
import logging
import argparse
import matplotlib.pyplot as plt


# pyCGM2 settings
import pyCGM2
from pyCGM2 import log; log.setLoggingLevel(logging.INFO)

# vicon nexus
import ViconNexus

# pyCGM2 libraries
from pyCGM2 import enums
from pyCGM2.Lib import analysis
from pyCGM2.Lib import plot
from pyCGM2.Report import normativeDatasets

from pyCGM2.Nexus import  nexusTools
from pyCGM2.Utils import files

if __name__ == "__main__":

    plt.close("all")

    parser = argparse.ArgumentParser(description='CGM Gait Processing')
    parser.add_argument('-nd','--normativeData', type=str, help='normative Data set (Schwartz2008 or Pinzone2014)', default="Schwartz2008")
    parser.add_argument('-ndm','--normativeDataModality', type=str,
                        help="if Schwartz2008 [VerySlow,SlowFree,Fast,VeryFast] - if Pinzone2014 [CentreOne,CentreTwo]",
                        default="Free")
    parser.add_argument('-ps','--pointSuffix', type=str, help='suffix of model outputs')
    parser.add_argument('-c','--consistency', action='store_true', help='consistency plots')

    args = parser.parse_args()


    NEXUS = ViconNexus.ViconNexus()
    NEXUS_PYTHON_CONNECTED = NEXUS.Client.IsConnected()

    if NEXUS_PYTHON_CONNECTED:

        #-----------------------SETTINGS---------------------------------------
        pointSuffix = args.pointSuffix
        normativeData = {"Author" : args.normativeData, "Modality" : args.normativeDataModality}

        if normativeData["Author"] == "Schwartz2008":
            chosenModality = normativeData["Modality"]
            nds = normativeDatasets.Schwartz2008(chosenModality)    # modalites : "Very Slow" ,"Slow", "Free", "Fast", "Very Fast"
        elif normativeData["Author"] == "Pinzone2014":
            chosenModality = normativeData["Modality"]
            nds = normativeDatasets.Pinzone2014(chosenModality) # modalites : "Center One" ,"Center Two"

        consistencyFlag = True if args.consistency else False

        # --------------------------INPUTS ------------------------------------
        DEBUG= False
        if DEBUG:
            DATA_PATH = "C:\Users\HLS501\Documents\VICON DATA\pyCGM2-Data\Release Tests\CGM2.2\medial\\" #pyCGM2.TEST_DATA_PATH + "CGM1\\CGM1\\native\\"
            modelledFilenameNoExt = "Gait Trial 01"# "gait trial" #"static Cal 01-noKAD-noAnkleMed" #
            NEXUS.OpenTrial( str(DATA_PATH+modelledFilenameNoExt), 30 )
        else:
            DATA_PATH, modelledFilenameNoExt = NEXUS.GetTrialName()

        modelledFilename = modelledFilenameNoExt+".c3d"

        logging.info( "data Path: "+ DATA_PATH )
        logging.info( "file: "+ modelledFilename)

        # ----- Subject -----
        # need subject to find input files
        subjects = NEXUS.GetSubjectNames()
        subject = nexusTools.checkActivatedSubject(NEXUS,subjects)
        logging.info(  "Subject name : " + subject  )

        # --------------------pyCGM2 MODEL ------------------------------
        model = files.loadModel(DATA_PATH,subject)
        modelVersion = model.version


        # --------------------------PROCESSING --------------------------------
        analysisInstance = analysis.makeAnalysis("Gait", DATA_PATH,[modelledFilename],None, None, None,pointLabelSuffix=pointSuffix) # analysis structure gathering Time-normalized Kinematic and kinetic CGM outputs

        if not consistencyFlag:
            if model.m_bodypart in [enums.BodyPart.LowerLimb,enums.BodyPart.LowerLimbTrunk, enums.BodyPart.FullBody]:
                plot.plot_DescriptiveKinetic(DATA_PATH,analysisInstance,"LowerLimb",nds,pointLabelSuffix=pointSuffix, exportPdf=True,outputName=modelledFilename)
            if model.m_bodypart in [enums.BodyPart.LowerLimbTrunk, enums.BodyPart.FullBody]:
                plot.plot_DescriptiveKinetic(DATA_PATH,analysisInstance,"Trunk",nds,pointLabelSuffix=pointSuffix, exportPdf=True,outputName=modelledFilename)
            if model.m_bodypart in [enums.BodyPart.UpperLimb, enums.BodyPart.FullBody]:
                pass # TODO plot upperlimb panel

        else:
            if model.m_bodypart in [enums.BodyPart.LowerLimb,enums.BodyPart.LowerLimbTrunk, enums.BodyPart.FullBody]:
                plot.plot_ConsistencyKinetic(DATA_PATH,analysisInstance,bodyPart,"LowerLimb",nds,pointLabelSuffix=pointSuffix, exportPdf=True,outputName=modelledFilename)
            if model.m_bodypart in [enums.BodyPart.LowerLimbTrunk, enums.BodyPart.FullBody]:
                plot.plot_ConsistencyKinetic(DATA_PATH,analysisInstance,bodyPart,"Trunk",nds, pointLabelSuffix=pointSuffix, exportPdf=True,outputName=modelledFilename)
            if model.m_bodypart in [enums.BodyPart.UpperLimb, enums.BodyPart.FullBody]:



    else:
        raise Exception("NO Nexus connection. Turn on Nexus")
