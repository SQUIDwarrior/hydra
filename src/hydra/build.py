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
import multiprocessing
from time import sleep
from hydra.buildStep import BuildStepProcess


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

    def __init__(self, buildSteps, buildType='single', parallelCount=-1):
        '''
        Constructor
        '''
        self.buildType = buildType
        self.buildSteps = buildSteps
        self.parallelCount = parallelCount
        if (self.parallelCount == -1):
            self.parallelCount = multiprocessing.cpu_count() 
        
    def getBuildSteps(self):
        return self.buildSteps
    
    def addBuildStep(self, order, buildStep):
        parent = None
        if (order > 0):
            parent = self.buildSteps[order - 1]
        buildStep.setParentStep(parent)
        self.buildSteps.insert(order, buildStep)
        
    def runBuild(self):
        i = 0
        status = 0
        self.runningSteps = {}
        lastProcess = None
        for step in self.buildSteps:
            print("Executing step", i, "-", step.getStepName())            
            if (self.buildType == 'single'):
                status = step.execute()
                if status != 0:
                    print("Error executing step! Status code was", status)
                    break
            elif (self.buildType == 'process'):
                status += self.updateRunningSteps()
                 
                while(len(self.runningSteps) >= self.parallelCount):
                    print("Maximum number of parallel steps (", self.parallelCount, ") running.")
                    print("Waiting for running steps to complete")
                    status += self.updateRunningSteps()
                    sleep(5.0)                    
               
                parent = step.getParentStep()
                # Check if the step's parent is running
                if(parent != None):
                    parentStep = self.runningSteps.get(parent.getStepName())
                    if(parentStep != None):
                        print("Parent step is running, waiting for parent to end")
                        parentStep.getProcess().join()
                        status += self.updateRunningSteps()
                else:
                    print("Step has no parent")
                print("Starting new process")
      
                lastProcess = BuildStepProcess(step, i)
                self.runningSteps[step.getStepName()] = lastProcess
                lastProcess.getProcess().start()              
                
            i += 1;
            
        if(lastProcess != None):
            print("Waiting for final step to end")
            lastProcess.getProcess().join()
            status += self.updateRunningSteps()
        return status
    
    def updateRunningSteps(self):
        status = 0
        for step in list(self.runningSteps):
            if (not self.runningSteps.get(step).getProcess().is_alive()):
                status += self.runningSteps.pop(step).getBuildStep().getStatus()                
        return status
            
            
                
                
        

    