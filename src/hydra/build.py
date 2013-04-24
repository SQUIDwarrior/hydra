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

class Build(object):
    '''
    Basic class that represents a Build, which is essentially a list
    of build steps to be executed. 
    '''

    def __init__(self, buildSteps):
        '''
        Constructor
        '''
        self.buildSteps = buildSteps;
        
    def getBuildSteps(self):
        return self.buildSteps;
    
    def addBuildStep(self, order, buildStep):
        self.buildSteps.insert(order, buildStep);
        
    def runBuild(self):
        i = 0
        status = 0
        for step in self.buildSteps:
            print "Executing step #" + `i` + " - " + step.getStepName();
            status = self.executeStep(step);
            if status != 0:
                print "Error executing step! Status code was " + `status`
                break
            i += 1;
        return status    
        
    def executeStep(self, buildStep):
        return os.system(buildStep.getCommand())
                
        
class BuildStep(object):
    '''
    This represents a single step in a build. A step consists
    of a step name, and a command. Commands need to be complete, 
    i.e. "ant compile"
    '''
    
    def __init__(self, stepName, command): 
        self.stepName = stepName
        self.command = command
        
    def getStepName(self):
        return self.stepName
    
    def getCommand(self):
        return self.command;