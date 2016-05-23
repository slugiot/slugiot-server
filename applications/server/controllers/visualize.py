import datetime
import random


def test_fill():
    """Fills some data for visualization."""
    device_id = "device1"
    procedure_id = 12580
    name = "cpp03"
    log_level = 1
    # Clear previous data.
    db(db.outputs).delete()
    db(db.logs).delete()

    # fill some data for module_values table
    db(db.module_values).delete()
    db.module_values.insert(device_id=device_id,
                            procedure_id=procedure_id,
                            name=name,
                            module_value="egg",
                            time_stamp=datetime.datetime.now(),
                            received_time_stamp=datetime.datetime.now()
                            )

    db.module_values.insert(device_id=device_id,
                            procedure_id=procedure_id,
                            name=name,
                            module_value="leg",
                            time_stamp=datetime.datetime.now(),
                            received_time_stamp=datetime.datetime.now()
                            )

    # Let us insert some new random data.
    now = datetime.datetime.utcnow()
    for i in range(5):
        db.outputs.insert(device_id=device_id,
                          procedure_id=procedure_id,
                          name=name,
                          time_stamp=now - datetime.timedelta(days=i) - datetime.timedelta(hours=i),
                          output_value=random.random() * 20,
                          tag="1")
        db.logs.insert(device_id=device_id,
                       procedure_id=procedure_id,
                       time_stamp=now - datetime.timedelta(days=i),
                       log_level=log_level,
                       log_message='This is message' + str(i) + '.')


def fill_device():
    db(db.procedure_revisions).delete()
    print 2222222
    db.procedure_revisions.insert(procedure_id=10086,
                                  procedure_data="text information",
                                  is_stable=True,
                                  )
    db.procedure_revisions.insert(procedure_id=12580,
                                  procedure_data="text information",
                                  is_stable=True,
                                  )
    db(db.device).delete()
    print 1111111
    db.device.insert(device_id='device1',
                     user_email='admin@google.com',
                     name='admin',
                     )
    db.device.insert(device_id='device2',
                     user_email='admin@google.com',
                     name='admin',
                     )
    db(db.procedures).delete()
    print 1111111
    db.procedures.insert(device_id='device1',
                         name='app01'
                         )
    db.procedures.insert(device_id='device1',
                         name='bpp02'
                         )
    db.procedures.insert(device_id='device1',
                         name='cpp03'
                         )
    db.procedures.insert(device_id='device2',
                         name='app01'
                         )
    db.procedures.insert(device_id='device2',
                         name='bpp02'
                         )
    db.procedures.insert(device_id='device2',
                         name='cpp03'
                         )
    print 1111111


# @auth.requires_signature()
def get_modulename():
    device_id = request.vars.device_id
    modulename = []
    for row in db(db.module_values.device_id == device_id).select():
        modulename.append(row.procedure_id)
    print modulename
    print "end of get_modulename"
    result = {'module_name': modulename}
    return response.json(result)


def get_parameter():
    fill_device()

    device_id = request.vars.device_id
    print device_id

    print 1111111111

    name = []
    procedure_id = []

    for row in db(db.procedures.device_id == device_id).select():
        name.append({'name': row.name})

    for row in db(db.procedure_revisions).select():
        procedure_id.append({'procedure_id': row.procedure_id})

    result = {'name': name, 'procedure_id': procedure_id}
    return response.json(result)


# @auth.requires_signature()
def get_data():
    """Ajax method that returns all data in a given date range.
    Generate with: URL('visualize', 'get_data', args=[
    device_id, module_name, name, date1, date2
    ]
    """
    s = request.vars.start
    e = request.vars.end
    device_id = request.vars.device_id
    procedure_id = request.vars.procedure_id
    name = request.vars.name

    print s

    # start = datetime.strptime("2016-05-03 21:20:20", "%Y-%m-%d %H:%M:%S")
    # parse the start date and end date
    start_year = int(s[0:4])
    start_month = int(s[5:7])
    start_day = int(s[8:10])
    start_hour = int(s[11:13])
    start_minute = int(s[14:16])
    start_second = int(s[17:19])

    end_year = int(e[0:4])
    end_month = int(e[5:7])
    end_day = int(e[8:10])
    end_hour = int(e[11:13])
    end_minute = int(e[14:16])
    end_second = int(e[17:19])

    # transform the start date and end date into datetime format
    start = datetime.datetime(start_year, start_month, start_day, start_hour, start_minute, start_second)
    end = datetime.datetime(end_year, end_month, end_day, end_hour, end_minute, end_second)

    # <<<<<<< HEAD
    #
    #     print 111111
    # =======
    #     # generate random data depend on how many day picked
    #     num_days = end - start
    #     test_fill(num_days.days)
    #
    # >>>>>>> refs/remotes/origin/visual_team
    test_fill()
    output_data = db((db.outputs.time_stamp >= start) &
                     (db.outputs.time_stamp <= end) &
                     (db.outputs.device_id == device_id) &
                     (db.outputs.procedure_id == procedure_id) &
                     (db.outputs.name == name)).select(orderby=db.outputs.time_stamp)
    print "output_data is :"
    print output_data

    log_data = db((db.logs.time_stamp >= start) &
                  (db.logs.time_stamp <= end) &
                  (db.logs.device_id == device_id) &
                  (db.logs.procedure_id == procedure_id)).select(orderby=db.logs.time_stamp)
    mixed_data = []

    print 111111
    # print "111111111111111111111111"

    # for row in db((db.outputs.time_stamp >= start) & (db.outputs.time_stamp <= end)).select(
    #         orderby=db.outputs.time_stamp):
    for row in db((db.outputs.time_stamp >= start) &
                          (db.outputs.time_stamp <= end) &
                          (db.outputs.device_id == device_id) &
                          (db.outputs.procedure_id == procedure_id) &
                          (db.outputs.name == name)).select(orderby=db.outputs.time_stamp):
        type = 'output'
        device_id = row.device_id
        modulename = row.procedure_id
        time_stamp = row.time_stamp
        name = row.name
        value = row.output_value
        tag = row.tag
        content = 'name: ' + str(name) + ', value: ' + str(value) + ', tag: ' + str(tag)
        mixed_data.append({'type': type, 'device_id': device_id, 'modulename': modulename, 'time_stamp': time_stamp,
                           'content': content})
    print 222222222

    # print "111111111111111111111111"
    # add log_data in
    # for row in db((db.logs.time_stamp >= start) & (db.logs.time_stamp <= end)).select(orderby=db.logs.time_stamp):
    for row in db((db.logs.time_stamp >= start) &
                          (db.logs.time_stamp <= end) &
                          (db.logs.device_id == device_id) &
                          (db.logs.procedure_id == procedure_id)).select(orderby=db.logs.time_stamp):
        type = 'log'
        device_id = row.device_id
        modulename = row.procedure_id
        time_stamp = row.time_stamp
        log_level = row.log_level
        log_message = row.log_message
        content = 'name: ' + str(log_level) + ', value: ' + str(log_message)
        mixed_data.append({'type': type, 'device_id': device_id, 'modulename': modulename, 'time_stamp': time_stamp,
                           'content': content})

    print 222222222
    # print "111111111111111111111111"
    mixed_data.sort(key=lambda r: r['time_stamp'])

    result = {'output_data': output_data, 'log_data': log_data, 'mixed_data': mixed_data}

    return response.json(result)


def visualization():
    # storage device_id, and module in session for testing (fake)
    # later need to read them from UI backend
    session.device_id = "chicken"
    session.module = ["egg", "eggnog"]
    return dict(session=session)
