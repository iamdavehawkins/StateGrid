'''
Created on Apr 28, 2015

@author: DHawkins
'''
import os
import unittest
import filecmp
from stategrid.statedata import StateData, FormatError, DuplicateDataError

class StateGridTest(unittest.TestCase):
    
    def setUp(self):
        try:
            # remove the file so the test doesn't wrongfully pass
            os.remove('./plots/population.png')
        except OSError:
            pass
    
    def tearDown(self):
        try:
            # remove the file so the test doesn't wrongfully pass next time
            os.remove('./plots/population.png')
        except OSError:
            pass

    def test_no_state_column(self):
        '''test no state column'''
        brk_path = "./data/popdata_broke.csv"
        self.assertRaises(FormatError, StateData, brk_path)
        
    def test_dupe_state_data(self):
        '''test dupe state data'''
        brk_path = "./data/popdata_dupes.csv"
        self.assertRaises(DuplicateDataError, StateData, brk_path)
        
    def test_number_in_state_data(self):
        '''test number in state data'''
        brk_path = "./data/popdata_tests.csv"
        self.assertRaises(ValueError, StateData, brk_path)
        
    def test_extra_data(self):
        '''test extra data'''
        brk_path = "./data/popdata_extra.csv"
        sd = StateData(brk_path)
        sd.plot_grid("population", fname='./plots/population.png')
        self.assertTrue(os.path.isfile('./plots/population.png'))
        
    def test_plot_saves(self):
        '''test plot saves'''
        dat_path = "./data/popdata.csv"
        sd = StateData(dat_path)
        sd.plot_grid("population", fname='./plots/population.png')
        self.assertTrue(os.path.isfile('./plots/population.png'))
        self.assertTrue(filecmp.cmp('./plots/population.png', './plots/population_master.png'))
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()