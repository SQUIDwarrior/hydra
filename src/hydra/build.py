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

class Build(object):
    '''
    Basic class that represents a Build, which is essentially a list
    of build steps to be executed. 
    
    Parallelization is controlled by each step's parentStepName parameter.
    Steps are executed in parallel as long as each step's parent is not a 
    currently running step. If a build step is reached whose parent is a 
    currently running step, the build sequence halts until that step has 
    finished executing. 
    '''

    def __init__(self, buildType='single', buildSteps):
        '''
        Constructor
        '''
        self.buildType = buildType
        self.buildSteps = buildSteps;
        
    def getBuildSteps(self):
        return self.buildSteps;
    
    def addBuildStep(self, order, buildStep):
        self.buildSteps.insert(order, buildStep);
        
    def runBuild(self):
        i = 0
        status = 0
        self.runningSteps = {}
        for step in self.buildSteps:
            print "Executing step #" + `i` + " - " + step.getStepName()
            
            if (self.buildType == 'single'):
                status = step.execute()
                if status != 0:
                    print "Error executing step! Status code was " + `status`
                    break
            elif (self.buildType == 'process'):
                self.updateRunningSteps()
                parent = step.getStepParentName()
                

                p = Process(target=step.execute, name=step.getStepName + i)
                
                
            i += 1;
        return status    
                
        
class BuildStep(object):
    '''
    This represents a single step in a build. A step consists
    of a step name, and a command. Commands need to be complete, 
    i.e. "ant compile".
    
    The parentStepName defines which build step is the parent of this 
    step. Build parallelization is controlled by this value. 
    '''
    
    def __init__(self, stepName, parentStepName=None, command): 
        self.stepName = stepName
        self.command = command
        self.parentStepName = parentStepName
        
    def getStepName(self):
        return self.stepName
    
    def getCommand(self):
        return self.command
    
    def execute(self):
        return os.system(self.command)
    
    def getParentStepName(self):
        return self.parentStepName
    