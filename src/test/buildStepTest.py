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
import os, unittest
from hydra.buildStep import BuildStep

class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testExecute(self):
        testFile = "test_file"
        cmd = "touch " + testFile
        buildStep = BuildStep("step", cmd)
        assert buildStep.execute() == 0
        try:
            with open(testFile): pass
        except IOError:
            self.fail("step did not execute")
        finally:
            os.remove(testFile)
            


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testExecute']
    unittest.main()