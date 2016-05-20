import datetime
import random


def test_fill():
    """Fills some data for visualization."""
    device_id = "chicken"
    module = "egg"
    out_var = "x"
    log_level = 1
    # Clear previous data.
    db(db.outputs).delete()
    db(db.logs).delete()

    # fill some data for module_values table
    db(db.module_values).delete()
    db.module_values.insert(device_id=device_id,
                            procedure_id="egg",
                            name="egg",
                            module_value="egg",
                            time_stamp=datetime.datetime.now(),
                            received_time_stamp=datetime.datetime.now()
                            )

    db.module_values.insert(device_id=device_id,
                            procedure_id="leg",
                            name="leg",
                            module_value="leg",
                            time_stamp=datetime.datetime.now(),
                            received_time_stamp=datetime.datetime.now()
                            )

    # Let us insert some new random data.
    now = datetime.datetime.utcnow()
    for i in range(5):
        db.outputs.insert(device_id=device_id,
                          procedure_id=module,
                          name=out_var,
                          time_stamp=now - datetime.timedelta(days=i) - datetime.timedelta(hours=i),
                          output_value=random.random() * 20,
                          tag="1")
        db.logs.insert(device_id=device_id,
                       procedure_id=module,
                       time_stamp=now - datetime.timedelta(days=i),
                       log_level=log_level,
                       log_message='This is message' + str(i) + '.')


def fill_device():
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
                   name='app02'
                   )
    db.procedures.insert(device_id='device1',
                   name='app03'
                   )
    db.procedures.insert(device_id='device2',
                   name='app01'
                   )
    db.procedures.insert(device_id='device2',
                   name='app02'
                   )
    db.procedures.insert(device_id='device2',
                   name='app03'
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


def get_name():
    fill_device()

    device_id = request.vars.device_id
    print device_id

    print 1111111111

    name = []

    for row in db(db.procedures.device_id == device_id).select():
        name.append({'name': row.name})

    result = {'name': name}
    return response.json(result)


# @auth.requires_signature()
def get_data():
    """Ajax method that returns all data in a given date range.
    Generate with: URL('visualize', 'get_data', args=[
    device_id, module_name, name, date1, date2
    ]
    """
    test_fill()
    s = request.vars.start
    e = request.vars.end

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

    output_data = db((db.outputs.time_stamp >= start) &
                     (db.outputs.time_stamp <= end)).select(orderby=db.outputs.time_stamp)
    log_data = db((db.logs.time_stamp >= start) &
                  (db.logs.time_stamp <= end)).select(orderby=db.logs.time_stamp)
    mixed_data = []

    # print "111111111111111111111111"

    for row in db((db.outputs.time_stamp >= start) & (db.outputs.time_stamp <= end)).select(
            orderby=db.outputs.time_stamp):
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

    # print "111111111111111111111111"
    # add log_data in
    for row in db((db.logs.time_stamp >= start) & (db.logs.time_stamp <= end)).select(orderby=db.logs.time_stamp):
        type = 'log'
        device_id = row.device_id
        modulename = row.procedure_id
        time_stamp = row.time_stamp
        log_level = row.log_level
        log_message = row.log_message
        content = 'name: ' + str(log_level) + ', value: ' + str(log_message)
        mixed_data.append({'type': type, 'device_id': device_id, 'modulename': modulename, 'time_stamp': time_stamp,
                           'content': content})

    # print "111111111111111111111111"
    mixed_data.sort(key=lambda r: r['time_stamp'])

    result = {'output_data': output_data, 'log_data': log_data, 'mixed_data': mixed_data}

    return response.json(result)


def visualization():
    return dict()
