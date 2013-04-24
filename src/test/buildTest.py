'''
Created on Apr 21, 2013

@author: mike
'''
import unittest
from hydra.build import Build, BuildStep


class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testAddBuildStep(self):
        buildSteps = [BuildStep("step1", "cmd"), BuildStep("step3", "cmd")]
        build = Build(buildSteps)
        newStep = BuildStep("step2", "cmd")
        build.addBuildStep(1, newStep)
        assert newStep == build.getBuildSteps()[1]
        
    def testExecuteStep(self):
        buildStep = BuildStep("step", "touch /tmp/test_file")
        build = Build([buildStep])
        assert build.executeStep(buildStep) == 0
        try:
            with open('/tmp/test_file'): pass
        except IOError:
            self.fail("step did not execute")
            
    def testRunBuild(self):
        buildSteps = [BuildStep("step1", "touch /tmp/file1"), 
                      BuildStep("step2", "cp /tmp/file1 /tmp/file2"), 
                      BuildStep("step3", "rm /tmp/file1")];
        build = Build(buildSteps)
        assert build.runBuild() == 0
        
        try:
            with open('/tmp/file2'): pass
        except IOError:
            self.fail("step2 did not execute")
            
        try:
            with open('/tmp/file1'): 
                self.fail("step3 did not execute")
        except IOError:
            pass
            
        
        
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
