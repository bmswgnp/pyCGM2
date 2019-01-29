args.BandpassFrequencies# -*- coding: utf-8 -*-
import logging
import argparse


import pyCGM2
from pyCGM2 import log; log.setLoggingLevel(logging.INFO)
from pyCGM2.Utils import files
from pyCGM2.Lib import analysis
from pyCGM2.Lib import plot
from pyCGM2.Report import normativeDatasets


import ViconNexus


if __name__ == "__main__":


    NEXUS = ViconNexus.ViconNexus()
    NEXUS_PYTHON_CONNECTED = NEXUS.Client.IsConnected()

    parser = argparse.ArgumentParser(description='EMG-plot_temporalEMG')
    parser.add_argument('-bpf', '--BandpassFrequencies', nargs='+',help='bandpass filter')
    parser.add_argument('-elf','--EnvelopLowpassFrequency', type=int, help='cutoff frequency for emg envelops')
    parser.add_argument('-fs','--fileSuffix', type=str, help='suffix of the processed file')
    parser.add_argument('-c','--consistency', action='store_true', help='consistency plots')
    args = parser.parse_args()


    if NEXUS_PYTHON_CONNECTED: # run Operation

        emgSettings = files.openFile(pyCGM2.PYCGM2_APPDATA_PATH,"emg.settings")

        # ----------------------INPUTS-------------------------------------------
        bandPassFilterFrequencies = emgSettings["Processing"]["BandpassFrequencies"]
        if args.BandpassFrequencies is not None:
            if len(args.BandpassFrequencies) != 2:
                raise Exception("[pyCGM2] - bad configuration of the bandpass frequencies ... set 2 frequencies only")
            else:
                bandPassFilterFrequencies = [float(args.BandpassFrequencies[0]),float(args.BandpassFrequencies[1])]
                logging.info("Band pass frequency set to %i - %i instead of 20-200Hz",bandPassFilterFrequencies[0],bandPassFilterFrequencies[1])

        envelopCutOffFrequency = emgSettings["Processing"]["EnvelopLowpassFrequency"]
        if args.EnvelopLowpassFrequency is not None:
            envelopCutOffFrequency =  args.EnvelopLowpassFrequency
            logging.info("Cut-off frequency set to %i instead of 6Hz ",envelopCutOffFrequency)

        consistencyFlag = True if args.consistency else False

        fileSuffix = args.fileSuffix

        # --- acquisition file and path----
        DEBUG = False
        if DEBUG:
            DATA_PATH = pyCGM2.TEST_DATA_PATH + "EMG\\SampleNantes_prepost\\"
            inputFileNoExt = "pre" #"static Cal 01-noKAD-noAnkleMed" #

            NEXUS.OpenTrial( str(DATA_PATH+inputFileNoExt), 10 )

        else:
            DATA_PATH, inputFileNoExt = NEXUS.GetTrialName()

        inputFile = inputFileNoExt+".c3d"



        # reconfiguration of emg settings as lists
        EMG_LABELS = []
        EMG_CONTEXT =[]
        NORMAL_ACTIVITIES = []
        EMG_MUSCLES =[]
        for emg in emgSettings["CHANNELS"].keys():
            if emg !="None":
                if emgSettings["CHANNELS"][emg]["Muscle"] != "None":
                    EMG_LABELS.append(str(emg))
                    EMG_MUSCLES.append(str(emgSettings["CHANNELS"][emg]["Muscle"]))
                    EMG_CONTEXT.append(str(emgSettings["CHANNELS"][emg]["Context"])) if emgSettings["CHANNELS"][emg]["Context"] != "None" else EMG_CONTEXT.append(None)
                    NORMAL_ACTIVITIES.append(str(emgSettings["CHANNELS"][emg]["NormalActivity"])) if emgSettings["CHANNELS"][emg]["NormalActivity"] != "None" else EMG_CONTEXT.append(None)

        # EMG_LABELS=['EMG1','EMG2','EMG3','EMG4'] # list of emg labels in your c3d
        # EMG_CONTEXT=['Left','Left','Right','Left'] # A context is not the body side. A context is relative to the gait cycle. EMG1 will plot for the Left Gait Cycle.
        # NORMAL_ACTIVITIES = ["RECFEM","RECFEM",None,"VASLAT"]



        analysis.processEMG(DATA_PATH, [inputFile], EMG_LABELS,
            highPassFrequencies=bandPassFilterFrequencies,
            envelopFrequency=envelopCutOffFrequency,fileSuffix=fileSuffix) # high pass then low pass for all c3ds

        emgAnalysis = analysis.makeEmgAnalysis("Gait",DATA_PATH, [inputFile], EMG_LABELS,None, None)

        if fileSuffix is not None:
            inputfile = inputFile +"_"+ fileSuffix

        if not consistencyFlag:
            plot.plotDescriptiveEnvelopEMGpanel(DATA_PATH,emgAnalysis, EMG_LABELS,EMG_MUSCLES,EMG_CONTEXT, NORMAL_ACTIVITIES, normalized=False,exportPdf=True,outputName=inputFile)
        else:
            plot.plotConsistencyEnvelopEMGpanel(DATA_PATH,emgAnalysis, EMG_LABELS,EMG_MUSCLES,EMG_CONTEXT, NORMAL_ACTIVITIES, normalized=False,exportPdf=True,outputName=inputFile)


    else:
        raise Exception("NO Nexus connection. Turn on Nexus")
