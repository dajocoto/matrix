import sys
import yaml
from pathlib import Path


def getData():    
    CONFIG_FILE = Path(__file__).resolve().parent / "global.yaml"
    
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(f"Config file not found: {CONFIG_FILE}")

    with CONFIG_FILE.open("r") as f:
        data = yaml.safe_load(f)

    if not isinstance(data['codecut'], dict):
        raise ValueError("YAML must contain a 'aiq_dist_path' key")
    return data

def getCodeCut():
    return getData()['codecut']
    
def getStartUpSettings():
    return getData()['startup_settings']

def getDesigner():
    return getData()['designer']
    
def getProperties():
    return getData()['properties']
    
def getHelp():
    return getData()['java_utilities']

def getHacks():
    return getData()['properties']
    
def getDebug():
    return getData()['debug']

def getMatrix():
    return getData()['matrix']
    
def getLogParser():
    return getData()['logParser']    


def getAWSsetting():
    return getData()['aws_settings']    
    