# -*- coding: utf-8 -*-
""" log_test.py
    Python Code for CMPS 276 Project
    This file is used to test logs database.
    First, it will generate some fake data for log table, output table.
    Then, log_report function will construct the form for visualizing in View.
"""

# add random log data by populate
from gluon.contrib.populate import populate
from gluon import current
# db = current.db
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
    db.logs.id.label = "#"
    header_dict = {'logs.log_level': 'Level', 'logs.log_message': 'Msg'}
    fieldID = db.logs.log_level # Use log_levl as id to each row of table and also sorted.
    grid = SQLFORM.grid(db.logs, deletable=False, editable=False, details=False,
                        create=False, csv=False, paginate=20, formstyle='table3cols',
                        headers=header_dict, field_id=fieldID, orderby=db.logs.id)

    # STYLE(XML('table,td,tr {padding: 50px}'))  <-- testing view API
    # this work but not useful
    grid['_style'] = 'padding: 10px'
    # print type(grid)
    # Change the height of rows in table
    tbodys = grid.elements('tbody')
    for tb in tbodys:
        tb['_style'] = 'line-height: 2.5'
    # Change the background color of rows of table depend on log_level
    tr_3 = grid.elements('tr', _id=3)
    for tr in tr_3:
        tr['_style'] = 'background-color: #D9534F'
    # print len(tr_3)

    # Write fake temperature data to a csv file
    import csv
    import os
    import datetime
    now = datetime.datetime.utcnow()
    now -= datetime.timedelta(days=len(k_temp))
    m_path = os.getcwd()
    tot_path = os.path.join(m_path, 'applications', 'server', 'static', 'temper.csv')
    with open(tot_path, 'wb') as csvfile:
        tmpwriter = csv.writer(csvfile, delimiter=',')
        tmpwriter.writerow(['data', 'Kitchen', 'Living_room'])
        for i in range(len(k_temp)):
            now += datetime.timedelta(days=1)
            tmpwriter.writerow([now.isoformat(), str(k_temp[i].Temperature), str(l_temp[i].Temperature)])

    return dict(grid=grid)