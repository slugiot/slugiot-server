# -*- coding: utf-8 -*-
""" log_test.py
    Python Code for CMPS 276 Project
    This file is used to test logs database.
    First, it will generate some fake data for log table, output table.
    Then, log_report function will construct the form for visualizing in View.
"""

# add random log data by populate
from gluon.contrib.populate import populate
db.logs.truncate()
db.outputs.truncate()
populate(db.logs, 50)
populate(db.outputs, 50)

# add fake testing data
db.define_table('Kitchen',
                Field('Temperature', 'double'))

db.define_table('Living_room',
                Field('Temperature', 'double'))

db.Kitchen.Temperature.requires = IS_INT_IN_RANGE(30, 45)
db.Living_room.Temperature.requires = IS_INT_IN_RANGE(20, 35)
db.Kitchen.truncate()
db.Living_room.truncate()
populate(db.Kitchen, 100)
populate(db.Living_room, 100)
k_temp = db().select(db.Kitchen.Temperature)
l_temp = db().select(db.Living_room.Temperature)


def log_report():
    """
    This function, now, use fake database of log and output to generate
    SQLFORM for log and save output to .csv for dygraph in view.

    :return: Dict with the SQLFORM for log data.
    :rtype: dict

    """
    # Construct log data into SQLFORM
    grid = SQLFORM.grid(db.logs, deletable=False, editable=False,
                        create=False, paginate=50, formstyle='table3cols')

    # Write fake temperature data to a csv file
    import csv
    import os
    m_path = os.getcwd()
    tot_path = os.path.join(m_path, 'applications', 'server', 'static', 'temper.csv')
    with open(tot_path, 'wb') as csvfile:
        tmpwriter = csv.writer(csvfile, delimiter=',')
        tmpwriter.writerow(['data', 'Kitchen', 'Living_room'])
        for i in range(len(k_temp)):
            tmpwriter.writerow([str(i), str(k_temp[i].Temperature), str(l_temp[i].Temperature)])

    return dict(grid=grid)
