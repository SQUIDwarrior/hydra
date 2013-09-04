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
import unittest, os
from hydra.build import Build
from hydra.buildStep import BuildStep


class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        try:
            os.remove("file1")
            os.remove("file2")
            os.remove("file3")
        except IOError:
            pass

    def testAddBuildStep(self):
        print("Running testAddBuildStep")
        buildSteps = [BuildStep("step1", "cmd"), BuildStep("step3", "cmd")]
        build = Build(buildSteps)
        newStep = BuildStep("step2", "cmd")
        build.addBuildStep(1, newStep)    
        assert newStep == build.getBuildSteps()[1]
        assert newStep.getParentStep() == build.getBuildSteps()[0]
            
    def testRunBuild(self):
        print("Running testRunBuild")
        buildSteps = [BuildStep("step1", "touch file1"), 
                      BuildStep("step2", "cp file1 file2"), 
                      BuildStep("step3", "rm file1")];
        build = Build(buildSteps)
        assert build.runBuild() == 0
        
        try:
            with open('file2'): pass
        except IOError:
            self.fail("step2 did not execute")
            
        try:
            with open('file1'): 
                self.fail("step3 did not execute")
        except IOError:
            pass
        
    def testRunBuildProcessSeqence(self):
        print("Running testRunBuildStepSeqence")
        step1 = BuildStep("step1", "echo step1 > file1")
        step2_1 = BuildStep("step2.1", "echo step2.1 >> file1", step1) 
        step2_2 = BuildStep("step2.2", "echo step2.2 >> file1", step1)
        step3 = BuildStep("step3", "cp file1 file3", step2_2)
        
        buildSteps = [step1, step2_1, step2_2, step3]
        
        build = Build(buildSteps, 'process')
        assert build.runBuild() == 0
        
        try:
            lines = [line.strip() for line in open('file1')]            
            assert lines[0] == 'step1'
            assert lines[1] == 'step2.1' or lines[1] == 'step2.2'
            assert lines[2] == 'step2.1' or lines[2] == 'step2.2'
        except IOError:
            self.fail("steps 1, 2.1, and 2.2 did not execute")
            
        try:
            lines = [line.strip() for line in open('file3')]            
            assert lines[0] == 'step1'
            assert lines[1] == 'step2.1' or lines[1] == 'step2.2'
            assert lines[2] == 'step2.1' or lines[2] == 'step2.2'
        except IOError:
            self.fail("step 3 did not execute")
            
        
            

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
