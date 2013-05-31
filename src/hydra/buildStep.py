"""
   Copyright 2013 Mike Deats

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
   
   @author Mike Deats
""" 
import os
from multiprocessing import Process

class BuildStep(object):
    '''
    This represents a single step in a build. A step consists
    of a step name, and a command. Commands need to be complete, 
    i.e. "ant compile".
    
    The parentStepName defines which build step is the parent of this 
    step. Build parallelization is controlled by this value. 
    '''
    
    def __init__(self, stepName, command, parentStep=None): 
        self.stepName = stepName
        self.command = command
        self.parentStep = parentStep
        
    def getStepName(self):
        return self.stepName
    
    def getCommand(self):
        return self.command
    
    def execute(self):
        return os.system(self.command)
    
    def getParentStep(self):
        return self.parentStep
    
class BuildStepProcess(BuildStep):
    '''
    classdocs
    '''


    def __init__(self, buildStep, stepId):
        '''
        Constructor
        '''
        self.buildStep = buildStep;
        self.stepId = stepId;
        self.process = Process(target=buildStep.execute, name=buildStep.getStepName + stepId)
        
    def getBuildStep(self):
        return self.buildStep
    
    def getStepId(self):
        return self.stepId
    
    def getProcess(self):
        return self.process