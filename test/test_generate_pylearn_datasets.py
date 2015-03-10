
import unittest
from paths import TEST_RAW_PYLEARN_DIR, TEST_RAW_GAZEBO_DIR

from generate_pylearn_datasets import PylearnDatasetGenerator


class TestGraspRGBDCapture(unittest.TestCase):

    def setUp(self):

        in_dset_filename = "contact_and_potential_grasps.h5"
        in_dset_dir = TEST_RAW_GAZEBO_DIR
        out_dset_dir = TEST_RAW_PYLEARN_DIR
        weights = (.8, .2, .2)

        self.pylearn_dataset_generator = PylearnDatasetGenerator(in_dset_filename, in_dset_dir, out_dset_dir, weights)

    def test_image_capture(self):
        self.pylearn_dataset_generator.run()


if __name__ == '__main__':
    unittest.main()