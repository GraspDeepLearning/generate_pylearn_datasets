
from choose import choose_from, choose_from_or_none
from paths import RAW_PYLEARN_DIR, RAW_GAZEBO_DIR, DATASET_TEMPLATE_PATH
from grasp_dataset import GraspDataset
import random


def weighted_choice(choices):
   total = sum(w for c, w in choices)
   r = random.uniform(0, total)
   upto = 0
   for c, w in choices:
      if upto + w > r:
         return c
      upto += w
   assert False, "Shouldn't get here"


class PylearnDatasetGenerator():

    def __init__(self, in_dset_filename, in_dset_dir, out_dset_dir, weights):

        self.in_dset_filename = in_dset_filename
        self.in_dset_dir = in_dset_dir
        self.out_dset_dir = out_dset_dir
        self.weights = weights

    #write to valid, train, test, grasp_priors
    def run(self):

        grasp_dataset = GraspDataset(self.in_dset_dir + self.in_dset_filename,
                                     DATASET_TEMPLATE_PATH + "/dataset_configs/gazebo_capture_config.yaml")

        train_dataset = GraspDataset(self.out_dset_dir + self.in_dset_filename[:-3] + "_train.h5",
                             DATASET_TEMPLATE_PATH + "/dataset_configs/gazebo_capture_config.yaml")
        valid_dataset = GraspDataset(self.out_dset_dir + self.in_dset_filename[:-3] + "_valid.h5",
                             DATASET_TEMPLATE_PATH + "/dataset_configs/gazebo_capture_config.yaml")
        test_dataset = GraspDataset(self.out_dset_dir + self.in_dset_filename[:-3] + "_test.h5",
                             DATASET_TEMPLATE_PATH + "/dataset_configs/gazebo_capture_config.yaml")

        datasets_and_weights = zip([train_dataset, valid_dataset, test_dataset], self.weights)
        for grasp in grasp_dataset.iterator():
            dataset = weighted_choice(datasets_and_weights)
            dataset.add_grasp(grasp)


if __name__ == "__main__":

    gazebo_h5 = choose_from(RAW_GAZEBO_DIR)

    dataset_generator = PylearnDatasetGenerator(gazebo_h5, RAW_GAZEBO_DIR, RAW_PYLEARN_DIR, (.8,.1,.1))