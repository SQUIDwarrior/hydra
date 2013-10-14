'''
Created on Oct 14, 2013

@author: ct626c
'''
from configparser import ConfigParser, NoOptionError
from hydra.buildStep import BuildStep
class BuildConfig(object):
    '''
    classdocs
    '''


    def __init__(self, propertiesFile):
        '''
        Constructor
        '''
        self.propertiesFile = propertiesFile
        self.parser = ConfigParser()
        self.parser.read(self.propertiesFile)
        
        '''
        Base properties
        '''
        self.projectName = None
        self.buildType = None
        self.parallelCount = None
        self.buildGraph = None
        
        self.populateBuildProperties()
        self.populateBuildGraph()
        
    def populateBuildProperties(self):
        if (self.parser.has_section("main")):
            self.projectName = self.getProperty("main", "ProjectName", True)
            self.buildType = self.getProperty("main", "BuildType", False)
            try:
                self.parallelCount = int(self.getProperty("main", "ParallelCount", False))
            except TypeError:
                pass
            except ValueError as err:
                raise PropertyParseError("main", "ParallelCount", str(err))
                
        else:
            raise RequiredSectionMissing("main", "Could not find required section \'main\'")
        
    def populateBuildGraph(self):
        '''
        Check if at least build-step-1 exists
        '''
        if (self.parser.has_section('build-step-1')):
            self.buildGraph = []
            i = 1
            nextStepName="build-step-" + str(i)
            while(self.parser.has_section(nextStepName)):
                stepName = self.getProperty(nextStepName, "StepName", False, nextStepName)
                parentStep = self.getProperty(nextStepName, "ParentStep", False)
                command = self.getProperty(nextStepName, "Command", True)
                buildStep = BuildStep(stepName, command, parentStep)
                self.buildGraph.append(buildStep) 
                i += 1               
                nextStepName="build-step-" + str(i)
                  
        else:
            raise RequiredSectionMissing('build-step-1', 'Could not find required section \'build-step-1\'')
            
        
    def getProperty(self, section, key, required, default=None):
        if(not required):
            try:
                return self.parser.get(section, key)
            except NoOptionError:
                return default
        else:
            try:
                return self.parser.get(section, key)
            except NoOptionError as err:
                raise RequiredPropertyMissing(section, key, "Error getting required property! " + err.message)                           
            
         
class PropertiesFileError(Exception):
    """Base class for exceptions in this module."""
    pass

class RequiredSectionMissing(PropertiesFileError):    
    
    def __init__(self, section, message):
        self.section = section
        self.message = message

class RequiredPropertyMissing(PropertiesFileError):    
    
    def __init__(self, section, key, message):
        self.section = section
        self.key = key
        self.message = message
        
class PropertyParseError(PropertiesFileError):    
    
    def __init__(self, section, key, message):
        self.section = section
        self.key = key
        self.message = message
        
    
