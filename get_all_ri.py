#!/usr/bin/python
# Script to look at all running AWS Reserved Instances and show type + count.
from datetime import date, timedelta
import os
from os.path import expanduser
import tabulate

home_dir = expanduser("~")
report_delete_date = date.today() - timedelta(days=7)
report_home = home_dir + '/reports/instances'


def get_all_reserved_instances():
    from boto.ec2 import connect_to_region
    import time
    # Setting global variables
    envn = 'AWSProfileAccount'  # this is used to call the proper .aws profile for credentials
    region = 'us-east-1'
    ec2conn = connect_to_region(region, profile_name=envn)
    ri_report = open(report_home + '/all_reserved_instances_' + time.strftime("%Y%m%d" + ".txt"), 'w')
    total_instance_types = 0
    total_reserved_instances = 0

    try:
        reservations = ec2conn.get_all_reserved_instances()  # return all AWS instances
        mydict = {}
        for res in reservations:
            if res.state == "active":
                mydict[res.id] = {'type': res.instance_type, 'count': res.instance_count,
                                  'offer': res.offering_type, 'platform': res.description}

            total_reserved_instances += 1
            if res.state == "active":
                total_instance_types += res.instance_count

        ordered_dict = sorted(mydict.itervalues(), key=lambda x: x['type'])
        ri_report.write(tabulate.tabulate(ordered_dict, headers="keys"))
        ri_report.write("\n\n" + "Total Reserved Instance Types: " + str(total_reserved_instances) + "\n")
        ri_report.write("Total Reserved Instances: " + str(total_instance_types) + "\n")

    except Exception, e:
        print e


get_all_reserved_instances()

try:
    os.remove(report_home + '/instances/all_reserved_instances_' + str(report_delete_date.strftime("%Y%m%d")) + ".txt")
except OSError:
    pass
