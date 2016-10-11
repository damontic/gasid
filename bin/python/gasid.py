from __future__ import print_function
import boto
import graphviz
import pickle
import os
import sys

DIRECTORY_PICKLES = "pickles"
DIRECTORY_OUTPUT = "output"
FILE_INSTANCES = "instances.pickle"
FULL_FILE_INSTANCES_PATH = DIRECTORY_PICKLES+os.sep+FILE_INSTANCES
INSTANCE_NAME_TAG = "Name"
FILE_WRITE_BYTES = "wb"
FILE_READ_BYTES = "rb"
FILE_DOT = "graph.dot"
FULL_FILE_RESULT_PATH = DIRECTORY_OUTPUT+os.sep+FILE_DOT
ENGINE_FDP = "fdp"
IMAGE_FORMAT_PNG = "png"
NODE_ATTRIBUTES = {"image":'icons/ec2_instance.png', "peripheries":"0", "shape":"none"}

ERROR_NO_INSTANCE_NAME_TAG = "Instance has no InstanceName tag"

def hello():
        print("hello")

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
                instances = self.get_instances(connection)

                return self.create_image(file_dot = self.create_dot_file(instances))

        def get_instances(self, connection):
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
                graph = graphviz.Graph("Principal")
                graph1 = graphviz.Graph()
                graph2 = graphviz.Graph()

                for instance in instances:
                        if INSTANCE_NAME_TAG in instance.tags:
                                graph.node(instance.tags[INSTANCE_NAME_TAG], _attributes=NODE_ATTRIBUTES)
                                #if instance.vpc_id not in vpcs.keys():
                                #        vpcs[instance.vpc_id] = []
                                #else:
                                #        vpcs[instance.vpc_id].append(instance)
                        else:
                                eprint(ERROR_NO_INSTANCE_NAME_TAG)

                for instance_a in instances:
                        for instance_b in instances:
                                if INSTANCE_NAME_TAG in instance_a.tags and INSTANCE_NAME_TAG in instance_b.tags:
                                        graph.edge(instance_a.tags[INSTANCE_NAME_TAG], instance_b.tags[INSTANCE_NAME_TAG])

                graph1.node("otro nodo 1")
                graph2.node("otro nodo 2")
                graph.subgraph(graph1)
                graph.subgraph(graph2)
                graph.edge("otro nodo 1", "otro nodo 2")
                print(graph._subgraph)
                graph.save(FULL_FILE_RESULT_PATH)

                return FULL_FILE_RESULT_PATH

        def create_image(self, engine = ENGINE_FDP, format = IMAGE_FORMAT_PNG, file_dot = None):
                graphviz.render(engine, format, file_dot)

        def eprint(*args, **kwargs):
                print(*args, file=sys.stderr, **kwargs)