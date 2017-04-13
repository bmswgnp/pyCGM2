# -*- coding: utf-8 -*-
import os
import json
from collections import OrderedDict

CONTENT_INPUTS_CGM1 ="""
    {  
      "Global" : {
        "Marker diameter" : 14,
        "Point suffix" : ""
      },
      "Calibration" : {
        "Left flat foot" : 1 ,
        "Right flat foot" : 1 
      },
      "Fitting" : {
        "Moment Projection" : "Distal"
      }   
    }
    """


CONTENT_INPUTS_CGM1_1 ="""
    {  
      "Global" : {
        "Marker diameter" : 14,
        "Point suffix" : ""
      },
      "Calibration" : {
        "Left flat foot" : 1 ,
        "Right flat foot" : 1 
      },
      "Fitting" : {
        "Moment Projection" : "Proximal"
      }   
    }
    """

CONTENT_INPUTS_CGM2_1 ="""
    {  
      "Global" : {
        "Marker diameter" : 14,
        "Point suffix" : ""
      },
      "Calibration" : {
        "HJC regression" : "Hara",
        "Left flat foot" : 1 ,
        "Right flat foot" : 1 
      },
      "Fitting" : {
        "Moment Projection" : "Proximal"
      }   
    }
    """

CONTENT_INPUTS_CGM2_2 ="""
    {  
      "Global" : {
        "Marker diameter" : 14,
        "Point suffix" : ""
      },
      "Calibration" : {
        "HJC regression" : "Hara",
        "Left flat foot" : 1 ,
        "Right flat foot" : 1 
      },
      "Fitting" : {
        "Moment Projection" : "Proximal",
        "Weight" :{
            "LASI" : 100,
            "RASI" : 100,
            "LPSI" : 100,
            "RPSI" : 100,
            "LTHI" : 100,
            "LKNE" : 100,
            "LTIB":  100,
            "LANK" : 100,
            "LHEE" : 100,
            "LTOE" : 100,            
            "RTHI" : 100,
            "RKNE" : 100,
            "RTIB":  100,
            "RANK" : 100,
            "RHEE" : 100,
            "RTOE" : 100
        }
      }   
    }
    """

CONTENT_INPUTS_CGM2_2_EXPERT ="""
    {  
      "Global" : {
        "Marker diameter" : 14,
        "Point suffix" : ""
      },
      "Calibration" : {
        "HJC regression" : "Hara",
        "Left flat foot" : 1 ,
        "Right flat foot" : 1 
      },
      "Fitting" : {
        "Moment Projection" : "Proximal",
        "Weight" :{
             "LASI":0,
             "LASI_posAnt":100,
             "LASI_medLat":100,
             "LASI_supInf":100,
             "RASI":0,
             "RASI_posAnt":100,
             "RASI_medLat":100,
             "RASI_supInf":100,
             "LPSI":0,
             "LPSI_posAnt":100,
             "LPSI_medLat":100,
             "LPSI_supInf":100,
             "RPSI":0,
             "RPSI_posAnt":100,
             "RPSI_medLat":100,
             "RPSI_supInf":100,
             "RTHI":0,
             "RTHI_posAnt":100,
             "RTHI_medLat":100,
             "RTHI_proDis":100,
             "RKNE":0,
             "RKNE_posAnt":100,
             "RKNE_medLat":100,
             "RKNE_proDis":100,
             "RTIB":0,
             "RTIB_posAnt":100,
             "RTIB_medLat":100,
             "RTIB_proDis":100,
             "RANK":0,
             "RANK_posAnt":100,
             "RANK_medLat":100,
             "RANK_proDis":100,
             "RHEE":0,
             "RHEE_supInf":100,
             "RHEE_medLat":100,
             "RHEE_proDis":100,
             "RTOE":0,
             "RTOE_supInf":100,
             "RTOE_medLat":100,
             "RTOE_proDis":100,

             "LTHI":0,
             "LTHI_posAnt":100,
             "LTHI_medLat":100,
             "LTHI_proDis":100,
             "LKNE":0,
             "LKNE_posAnt":100,
             "LKNE_medLat":100,
             "LKNE_proDis":100,
             "LTIB":0,
             "LTIB_posAnt":100,
             "LTIB_medLat":100,
             "LTIB_proDis":100,
             "LANK":0,
             "LANK_posAnt":100,
             "LANK_medLat":100,
             "LANK_proDis":100,
             "LHEE":0,
             "LHEE_supInf":100,
             "LHEE_medLat":100,
             "LHEE_proDis":100,
             "LTOE":0,
             "LTOE_supInf":100,
             "LTOE_medLat":100,
             "LTOE_proDis":100  
        }
      }   
    }
    """
           
CONTENT_INPUTS_CGM2_3 ="""
    {  
      "Global" : {
        "Marker diameter" : 14,
        "Point suffix" : ""
      },
      "Translators" : {
            "LASI":"",
            "RASI":"",
            "LPSI":"",
            "RPSI":"",
            "RTHI":"RTHL",
            "RKNE":"",
            "RTHIAP":"RTHAP",
            "RTHIAD":"RTHAD",
            "RTIB":"RTIBL",
            "RANK":"",
            "RTIBAP":"RTIAP",
            "RTIBAD":"RTIAD",
            "RHEE":"",
            "RTOE":"",
            "LTHI":"LTHL",
            "LKNE":"",
            "LTHIAP":"LTHAP",
            "LTHIAD":"LTHAD",
            "LTIB":"LTIBL",
            "LANK":"",
            "LTIBAP":"LTIAP",
            "LTIBAD":"LTIAD",
            "LHEE":"",
            "LTOE":""
            },
      "Calibration" : {
        "HJC regression" : "Hara",
        "Left flat foot" : 1 ,
        "Right flat foot" : 1 
      },
      "Fitting" : {
        "Moment Projection" : "Proximal",
        "Weight" :{
            "LASI":100,
            "RASI":100,
            "LPSI":100,
            "RPSI":100,
            "RTHI":100,
            "RKNE":100,
            "RTHIAP":100,
            "RTHIAD":100,
            "RTIB":100,
            "RANK":100,
            "RTIBAP":100,
            "RTIBAD":100,
            "RHEE":100,
            "RTOE":100,
            "LTHI":100,
            "LKNE":100,
            "LTHIAP":100,
            "LTHIAD":100,
            "LTIB":100,
            "LANK":100,
            "LTIBAP":100,
            "LTIBAD":100,
            "LHEE":100,
            "LTOE":100,
            "RTHL":0,
            "RTHLD":0,
            "RPAT":0,
            "RTIBL":0,
            "LTHL":0,
            "LTHLD":0,
            "LPAT":0,
            "LTIBL":0
        }
      }   
    }
    """


def generateCGM1_Settings(userAppData_path):

    if not os.path.isfile( userAppData_path + "CGM1-pyCGM2.inputs"):    
        inputs = json.loads(CONTENT_INPUTS_CGM1,object_pairs_hook=OrderedDict)
        
        F = open(str(userAppData_path+"CGM1-pyCGM2.inputs"),"w") 
        F.write( json.dumps(inputs, sort_keys=False,indent=2, separators=(',', ': ')))
        F.close()
        
def generateCGM1_1_Settings(userAppData_path):

    if not os.path.isfile( userAppData_path + "CGM1_1-pyCGM2.inputs"):    
        inputs = json.loads(CONTENT_INPUTS_CGM1_1,object_pairs_hook=OrderedDict)
        
        F = open(str(userAppData_path+"CGM1_1-pyCGM2.inputs"),"w") 
        F.write( json.dumps(inputs, sort_keys=False,indent=2, separators=(',', ': ')))
        F.close()

def generateCGM2_1_Settings(userAppData_path):

    if not os.path.isfile( userAppData_path + "CGM2_1-pyCGM2.inputs"):    
        inputs = json.loads(CONTENT_INPUTS_CGM2_1,object_pairs_hook=OrderedDict)
        
        F = open(str(userAppData_path+"CGM2_1-pyCGM2.inputs"),"w") 
        F.write( json.dumps(inputs, sort_keys=False,indent=2, separators=(',', ': ')))
        F.close()        
        
def generateCGM2_2_Settings(userAppData_path):

    if not os.path.isfile( userAppData_path + "CGM2_2-pyCGM2.inputs"):    
        inputs = json.loads(CONTENT_INPUTS_CGM2_2,object_pairs_hook=OrderedDict)
        
        F = open(str(userAppData_path+"CGM2_2-pyCGM2.inputs"),"w") 
        F.write( json.dumps(inputs, sort_keys=False,indent=2, separators=(',', ': ')))
        F.close()         
        
def generateCGM2_2_Expert_Settings(userAppData_path):

    if not os.path.isfile( userAppData_path + "CGM2_2-Expert-pyCGM2.inputs"):    
        inputs = json.loads(CONTENT_INPUTS_CGM2_2_EXPERT,object_pairs_hook=OrderedDict)
        
        F = open(str(userAppData_path+"CGM2_2-Expert-pyCGM2.inputs"),"w") 
        F.write( json.dumps(inputs, sort_keys=False,indent=2, separators=(',', ': ')))
        F.close() 

def generateCGM2_3_Settings(userAppData_path):

    if not os.path.isfile( userAppData_path + "CGM2_3-pyCGM2.inputs"):    
        inputs = json.loads(CONTENT_INPUTS_CGM2_3,object_pairs_hook=OrderedDict)
        
        F = open(str(userAppData_path+"CGM2_3-pyCGM2.inputs"),"w") 
        F.write( json.dumps(inputs, sort_keys=False,indent=2, separators=(',', ': ')))
        F.close()          