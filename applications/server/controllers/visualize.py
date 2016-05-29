import datetime
import random


def test_fill():
    """Fills some data for visualization."""
    device_id = "device1"
    procedure_id = 12580
    name = "cpp03"
    # Clear previous data.
    db(db.outputs).delete()
    db(db.logs).delete()

    # fill some data for module_values table
    db(db.module_values).delete()
    db.module_values.insert(device_id=device_id,
                            procedure_id=procedure_id,
                            name=name,
                            output_value="egg",
                            value_time_stamp=datetime.datetime.now(),
                            received_time_stamp=datetime.datetime.now()
                            )

    db.module_values.insert(device_id=device_id,
                            procedure_id=procedure_id,
                            name=name,
                            output_value="leg",
                            value_time_stamp=datetime.datetime.now(),
                            received_time_stamp=datetime.datetime.now()
                            )

    # Let us insert some new random data.
    now = datetime.datetime.utcnow()
    for i in range(5):
        db.outputs.insert(device_id=device_id,
                          procedure_id=procedure_id,
                          name=name,
                          output_time_stamp=now - datetime.timedelta(days=i) - datetime.timedelta(hours=i),
                          output_value=random.random() * 20,
                          tag="1")
        db.logs.insert(device_id=device_id,
                       procedure_id=procedure_id,
                       logged_time_stamp=now - datetime.timedelta(days=i),
                       log_level=random.randint(0, 4),
                       log_message='This is message' + str(i) + '.')


def fill_device():
    db(db.procedure_revisions).delete()
    db.procedure_revisions.insert(procedure_id=10086,
                                  procedure_data="text information",
                                  is_stable=True,
                                  )
    db.procedure_revisions.insert(procedure_id=12580,
                                  procedure_data="text information",
                                  is_stable=True,
                                  )
    db(db.device).delete()
    db.device.insert(device_id='device1',
                     user_email='admin@google.com',
                     name='admin',
                     )
    db.device.insert(device_id='device2',
                     user_email='admin@google.com',
                     name='admin',
                     )
    db(db.procedures).delete()
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
    # date1
    s = request.vars.start
    # date2
    e = request.vars.end
    # device_id
    device_id = request.vars.device_id
    # module_name or procedure_id
    procedure_id = request.vars.procedure_id
    # name
    name = request.vars.name

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


    # print 111111111111111111111111
    # transform the start date and end date into datetime format
    start = datetime.datetime(start_year, start_month, start_day, start_hour, start_minute, start_second)
    end = datetime.datetime(end_year, end_month, end_day, end_hour, end_minute, end_second)

    test_fill()

    print "----------finish test fill-----------------------"
    # get output_data and sort by time_stamp
    output_data = db((db.outputs.output_time_stamp >= start) &
                     (db.outputs.output_time_stamp <= end) &
                     (db.outputs.device_id == device_id) &
                     (db.outputs.procedure_id == procedure_id) &
                     (db.outputs.name == name)).select(orderby=db.outputs.output_time_stamp)
    # get log_data and sort by time_stamp
    log_data = db((db.logs.logged_time_stamp >= start) &
                  (db.logs.logged_time_stamp <= end) &
                  (db.logs.device_id == device_id) &
                  (db.logs.procedure_id == procedure_id)).select(orderby=db.logs.logged_time_stamp)
    # generate mixed_data from output_data and log_data and sort by time_stamp
    print 111111111111111111111111
    mixed_data = []
    # transform output_data into mixed_data
    for row in db((db.outputs.output_time_stamp >= start) &
                          (db.outputs.output_time_stamp <= end) &
                          (db.outputs.device_id == device_id) &
                          (db.outputs.procedure_id == procedure_id) &
                          (db.outputs.name == name)).select(orderby=db.outputs.output_time_stamp):
        type = 'output'
        device_id = row.device_id
        modulename = row.procedure_id
        time_stamp = row.output_time_stamp
        name = row.name
        value = row.output_value
        tag = row.tag
        content = 'name: ' + str(name) + ', value: ' + str(value) + ', tag: ' + str(tag)
        mixed_data.append({'type': type, 'device_id': device_id, 'modulename': modulename, 'time_stamp': time_stamp,
                           'content': content})
    print 111111111111111111111111
    # transform log_data into mixed_data
    for row in db((db.logs.logged_time_stamp >= start) &
                          (db.logs.logged_time_stamp <= end) &
                          (db.logs.device_id == device_id) &
                          (db.logs.procedure_id == procedure_id)).select(orderby=db.logs.logged_time_stamp):
        type = 'log'
        device_id = row.device_id
        modulename = row.procedure_id
        time_stamp = row.logged_time_stamp
        log_level = row.log_level
        log_message = row.log_message
        content = 'name: ' + str(log_level) + ', value: ' + str(log_message)
        mixed_data.append({'type': type, 'device_id': device_id, 'modulename': modulename, 'time_stamp': time_stamp,
                           'content': content})
    print 111111111111111111111111
    # sort the mixed_data by time_stamp
    mixed_data.sort(key=lambda r: r['time_stamp'])
    # build the return data in dict format
    result = {'output_data': output_data, 'log_data': log_data, 'mixed_data': mixed_data}
    # dump into json format
    return response.json(result)


def visualization():
    # storage device_id, and module in session for testing (fake)
    # later need to read them from UI backend
    session.device_id = "chicken"
    session.module = ["egg", "eggnog"]
    return dict(session=session)

def visual_d3():
    response.view = 'visualize/visual_d3.html'
    return dict(message='Hello D3')
