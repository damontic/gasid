#! /bin/python

from __future__ import print_function
import boto
import graphviz
import pickle
import os
import sys

DIRECTORY_PICKLES = "pickles"
FILE_INSTANCES = "instances.pickle"
FULL_FILE_INSTANCES_PATH = DIRECTORY_PICKLES+os.sep+FILE_INSTANCES
INSTANCE_NAME_TAG = "Name"
FILE_WRITE_BYTES = "wb"
FILE_READ_BYTES = "rb"
FILE_DOT = "my_graph.dot"


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

class Gasid(object):
        """
        Creates an infraestructure image from an Amazon Web Service account.

        :rtype: png
        :return: A png file
        """

        def __init__(self):
                if not os.path.isdir(DIRECTORY_PICKLES):
                        os.mkdir(DIRECTORY_PICKLES)

                connection = boto.connect_ec2()
                instances = self.get_instances()

                return self.create_image(file_dot = self.create_dot_file(instances))

        def get_instances(self):
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

        def create_dot_file(self, instances):
                graph = graphviz.Graph()
                for instance in instances:
                        if INSTANCE_NAME_TAG in instance.tags:
                                graph.node(instance.tags[INSTANCE_NAME_TAG])
                        else:
                                eprint("Instance has no InstanceName tag")

                for instance_a in instances:
                        for instance_b in instances:
                                if INSTANCE_NAME_TAG in instance_a.tags and INSTANCE_NAME_TAG in instance_b.tags:
                                        graph.edge(instance_a.tags[INSTANCE_NAME_TAG], instance_b.tags[INSTANCE_NAME_TAG])

                graph.save(FILE_DOT)

                return FILE_DOT

        def create_image(self, engine = "fdp", format = "svg", file_dot = None):
                graphviz.render(engine, format, file_dot)

if __name__ == "__main__":
        gasid = Gasid()
