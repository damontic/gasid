#! /bin/python

import boto
import pickle
import os

DIRECTORY_PICKLES = "pickles"
FILE_INSTANCES = "instances.pickle"
FULL_FILE_INSTANCES_PATH = DIRECTORY_PICKLES+os.sep+FILE_INSTANCES
INSTANCE_NAME_TAG = "Name"
FILE_WRITE_BYTES = "wb"
FILE_READ_BYTES = "rb"

def get_instances():
        """
        Returns the instances from AWS and stores them in the pickles directory.
        If the pickles directory and the FILE_INSTANCES file already exist then
        it reads the instances information from it.

        :rtype: list
        :return: A list of  :class:`boto.ec2.instance.Instance`
        """

        if not os.path.isfile(FULL_FILE_INSTANCES_PATH):
                file_instances = open(FULL_FILE_INSTANCES_PATH, FILE_WRITE_BYTES)
                instances = connection.get_only_instances()
                pickle.dump(instances, file_instances)
        else:
                file_instances = open(FULL_FILE_INSTANCES_PATH, FILE_READ_BYTES)
                instances = pickle.load(file_instances)
        file_instances.close()

        return instances

if __name__ == "__main__":
        if not os.path.isdir(DIRECTORY_PICKLES):
                os.mkdir(DIRECTORY_PICKLES)

        connection = boto.connect_ec2()
        instances = get_instances()

        for instance in instances:
                if INSTANCE_NAME_TAG in instance.tags:
                        print(instance.tags[INSTANCE_NAME_TAG])
                else:
                        print("Instance has no InstanceName tag")
