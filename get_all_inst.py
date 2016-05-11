#!/usr/bin/python

# Script to look at all running AWS instances and show a comparison between active & reserved instance types.

from datetime import date, timedelta
import os
from os.path import expanduser
import tabulate


home_dir = expanduser("~")
report_delete_date = date.today() - timedelta(days=7)
report_home = home_dir + '/reports/instances'

def get_all_instances():


    from boto.ec2 import connect_to_region
    import time
    # Setting global variables
    envn = 'RIComparisonServiceAccount'  # this is used to call the proper .aws profile for credentials
    region = 'us-east-1'
    ec2conn = connect_to_region(region, profile_name=envn)
    instance_count = 0
    instance_report = open(report_home + '/all_instances_' + time.strftime("%Y%m%d" + ".txt"),'w')

    try:
        reservations = ec2conn.get_all_instances()  # return all AWS instances
        mydict = {}
        for res in reservations:
            for inst in res.instances:
                instance_count += 1
                if 'Name' in inst.tags:
                    mydict[inst.tags['Name']] = { 'id': inst.id, 'state': inst.state, 'type': inst.instance_type, 'name': inst.tags['Name'] }
                    ordered_dict = sorted(mydict.itervalues(), key=lambda x: x['type'])

        instance_report.write(tabulate.tabulate(ordered_dict, headers="keys"))
        instance_report.write("\n\nInstance Count: " + str(instance_count) + "\n")

    except Exception, e:
        print e

get_all_instances()

try:
    os.remove(report_home + '/all_instances_' + str(report_delete_date.strftime("%Y%m%d")) + ".txt")
except OSError:
    pass