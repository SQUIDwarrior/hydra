'''
Created on Oct 14, 2013

@author: ct626c
'''
import unittest, os
from hydra.buildConfig import BuildConfig, RequiredPropertyMissing, RequiredSectionMissing, PropertyParseError
from hydra.buildStep import BuildStep

class Test(unittest.TestCase):

    def setUp(self):        
        pass


    def tearDown(self):
        try:
            os.remove("testProps.properties")
        except IOError:
            pass
        
    def testParseAllProperties(self):
        propFile = open("testProps.properties", 'w')
        '''
        Print all properties
        '''
        print("[main]", file=propFile)
        print("ProjectName: My New Project", file=propFile)
        print("BuildType: single", file=propFile)
        print("ParallelCount: 8", file=propFile)
        print("[build-step-1]", file=propFile)
        print("StepName: step1", file=propFile)
        print("Command: bleh", file=propFile)     
        propFile.close()

        config = BuildConfig("testProps.properties")

        self.assertEqual("My New Project", config.projectName)
        self.assertEqual("single", config.buildType) 
        self.assertEqual(8, config.parallelCount)
        
    def testParsePropertiesOptional(self):
        propFile = open("testProps.properties", 'w')
        '''
        Print all properties, but omit a few non-required ones
        '''
        print("[main]", file=propFile)
        print("ProjectName: My New Project", file=propFile)
        print("BuildType: single", file=propFile)
        print("[build-step-1]", file=propFile)
        print("StepName: step1", file=propFile)
        print("Command: bleh", file=propFile)
        print("[build-step-2]", file=propFile)
        print("StepName: step2", file=propFile)
        print("ParentStep: step1", file=propFile)
        print("Command: bleh", file=propFile)        
        propFile.close()

        config = BuildConfig("testProps.properties")

        self.assertEqual("My New Project", config.projectName)
        self.assertEqual("single", config.buildType) 
        self.assertIsNone(config.parallelCount)
        
    def testParseInvalidParallelCount(self):
        propFile = open("testProps.properties", 'w')
        '''
        Print all properties
        '''
        print("[main]", file=propFile)
        print("ProjectName: My New Project", file=propFile)
        print("ParallelCount: asdf", file=propFile)
        print("[build-step-1]", file=propFile)
        print("Command: bleh", file=propFile)     
        propFile.close()

        with self.assertRaises(PropertyParseError):
            BuildConfig("testProps.properties")
        

    def testMissingProperty(self):
        propFile = open("testProps.properties", 'w')
        '''
        Print the header stuff, but omit the project name 
        '''
        print("[main]", file=propFile)
        print("BuildType: single", file=propFile)
        print("[build-step-1]", file=propFile)
        print("StepName: step1", file=propFile)
        print("Command: bleh", file=propFile)
        propFile.close()
        
        with self.assertRaises(RequiredPropertyMissing):
            BuildConfig("testProps.properties")
            
    def testMissingMainSection(self):
        propFile = open("testProps.properties", 'w')

        print("[build-step-1]", file=propFile)
        print("StepName: step1", file=propFile)
        print("Command: bleh", file=propFile)
        print("[build-step-2]", file=propFile)
        print("StepName: step2", file=propFile)
        print("ParentStep: step1", file=propFile)
        print("Command: bleh", file=propFile) 
        propFile.close()
        
        with self.assertRaises(RequiredSectionMissing):
            BuildConfig("testProps.properties")
            
    def testMissingAtLeastOneBuildStepSection(self):
        propFile = open("testProps.properties", 'w')

        print("[main]", file=propFile)
        print("ProjectName: My New Project", file=propFile)
        print("BuildType: single", file=propFile)
        print("[build-step-1]", file=propFile)
        print("StepName: step1", file=propFile)
        print("Command: bleh", file=propFile)
        propFile.close()
        
        config = BuildConfig("testProps.properties")
        
        self.assertIsNotNone(config.buildGraph)
        self.assertEqual(config.buildGraph[0].stepName, "step1")
        self.assertEqual(config.buildGraph[0].command, "bleh")
        self.assertIsNone(config.buildGraph[0].parentStep)
        
    def testMultipleBuildSteps(self):
        propFile = open("testProps.properties", 'w')
        '''
        Print all properties, but omit a few non-required ones
        '''
        print("[main]", file=propFile)
        print("ProjectName: My New Project", file=propFile)
        print("BuildType: single", file=propFile)
        print("[build-step-1]", file=propFile)
        print("StepName: step1", file=propFile)
        print("Command: bleh", file=propFile)
        print("[build-step-2]", file=propFile)
        print("StepName: step2", file=propFile)
        print("ParentStep: step1", file=propFile)
        print("Command: bleh", file=propFile)     
        print("[build-step-3]", file=propFile)
        print("Command: bleh", file=propFile)     
        propFile.close()

        config = BuildConfig("testProps.properties")

        self.assertIsNotNone(config.buildGraph)
        self.assertEqual("step1", config.buildGraph[0].stepName)
        self.assertEqual("bleh", config.buildGraph[0].command)
        self.assertIsNone(config.buildGraph[0].parentStep)
        self.assertEqual("step2", config.buildGraph[1].stepName)
        self.assertEqual("bleh", config.buildGraph[1].command)
        self.assertEqual("step1", config.buildGraph[1].parentStep)
        self.assertEqual("build-step-3", config.buildGraph[2].stepName)
        self.assertEqual("bleh", config.buildGraph[2].command)
        self.assertIsNone(config.buildGraph[2].parentStep)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
