import pandas as pd
import sys
import test_generatefixtures
import unittest
import os
from csvcombiner import CsvCombiner
from io import StringIO


class TestCombineMethod(unittest.TestCase):

    # initialize all paths
    test_output_path = "./test_output.csv"
    csv_c_path = "./csv_combiner.py"
    acc_path = "./test_fixtures/accessories.csv"
    clo_path = "./test_fixtures/clothing.csv"
    hc_path = "./test_fixtures/household_cleaners.csv"
    ef_path = "./test_fixtures/empty_file.csv"

    # initialize the test output
    backup = sys.stdout
    test_output = open(test_output_path, 'w+')
    combiner = CsvCombiner()

    @classmethod
    def setUpClass(cls):
        # generate the test fixture files located in ./test_fixtures/
        test_generatefixtures.main()

        # redirect the output to ./test_output.csv
        sys.stdout = cls.test_output

    @classmethod
    def tearDownClass(cls):

        cls.test_output.close()

        if os.path.exists(cls.acc_path):
            os.remove(cls.acc_path)
        if os.path.exists(cls.clo_path):
            os.remove(cls.clo_path)
        if os.path.exists(cls.hc_path):
            os.remove(cls.hc_path)
        if os.path.exists(cls.ef_path):
            os.remove(cls.ef_path)
        if os.path.exists(cls.test_output_path):
            os.remove(cls.test_output_path)
        if os.path.exists("./test_fixtures"):
            os.rmdir("./test_fixtures")

    def setUp(self):
        # setup
        self.output = StringIO()
        sys.stdout = self.output
        self.test_output = open(self.test_output_path, 'w+')

    def tearDown(self):
        self.test_output.close()
        self.test_output = open(self.test_output_path, 'w+')
        sys.stdout = self.backup
        self.test_output.truncate(0)
        self.test_output.write(self.output.getvalue())
        self.test_output.close()

    def test_no_file_paths(self):

        # run csv_combiner with no arguments
        argv = [self.csv_c_path]
        self.combiner.comboFiles(argv)

        self.assertIn("Must have MORE THAN 2 inputs.", self.output.getvalue())

    def test_empty_files(self):

        # run csv_combiner with an empty file
        argv = [self.csv_c_path, self.ef_path]
        self.combiner.comboFiles(argv)

        self.assertIn("Warning: The following file is empty: ", self.output.getvalue())

    def test_non_existent_files(self):

        # run csv_combiner with a file that doesn't exist
        argv = [self.csv_c_path, "non_existent.csv"]
        self.combiner.comboFiles(argv)

        self.assertTrue("File is not found!" in self.output.getvalue())


    def test_all_values_exist_in_combined(self):

        # run csv_combiner with valid arguments
        argv = [self.csv_c_path, self.acc_path, self.clo_path,
                self.hc_path]
        self.combiner.comboFiles(argv)

        # update the test_output.csv file
        self.test_output.write(self.output.getvalue())
        self.test_output.close()

        # open all test data-frames

        acc_df = pd.read_csv(filepath_or_buffer=self.acc_path, lineterminator='\n')
        clo_df = pd.read_csv(filepath_or_buffer=self.clo_path, lineterminator='\n')
        hc_df = pd.read_csv(filepath_or_buffer=self.hc_path, lineterminator='\n')

        # ensure that all data from the fixtures exist in the resulting combined csv file

        with open(self.test_output_path) as f:
            combined_df = pd.read_csv(filepath_or_buffer=f, lineterminator='\n')
        self.assertEqual(len(combined_df.merge(acc_df)), len(combined_df.drop_duplicates()))
        self.assertEqual(len(combined_df.merge(clo_df)), len(combined_df.drop_duplicates()))
        self.assertEqual(len(combined_df.merge(hc_df)), len(combined_df.drop_duplicates()))
    




