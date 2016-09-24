#! /bin/python

import boto

connection	=	boto.connect_ec2()
regions		=	connection.get_all_regions()

instances	=	connection.get_only_instances()
for instance in instances:
	if 'InstanceName' in instance.tags:
		print(instance.tags['InstanceName'])
	else:
		print("Instance has no InstanceName tag")
