import datetime
import random


def test_fill():
    """Fills some data for visualization."""
    device_id = "chicken"
    module = "egg"
    out_var = "x"
    log_level = 1
    # Let us clear previous data.
    # db((db.outputs.device_id == device_id) &
    #    (db.outputs.modulename == module) &
    #    (db.outputs.name == out_var)).delete()
    db(db.outputs).delete()
    db(db.logs).delete()

    # fill some data for module_values table
    # db(db.module_values).delete()
    # db.module_values.insert(device_id=device_id,
    #                         modulename="egg",
    #                         name="egg",
    #                         output_value="egg"
    #                         )
    # db.module_values.insert(device_id=device_id,
    #                         modulename="leg",
    #                         name="leg",
    #                         output_value="leg"
    #                         )

    # Let us insert some new random data.
    now = datetime.datetime.utcnow()
    for i in range(3):
        db.outputs.insert(device_id=device_id,
                          procedure_id=module,
                          name=out_var,
                          output_time_stamp=now - datetime.timedelta(hours=i),
                          output_value=random.random() * 20,
                          tag="1")
        db.logs.insert(device_id=device_id,
                       modulename=module,
                       logged_time_stamp=now - datetime.timedelta(hours=i),
                       log_level=log_level,
                       log_message='This is message' + str(i) + '.')


# @auth.requires_signature()
def get_modulename():
    device_id = request.vars.device_id
    modulename = []
    for row in db(db.module_values.device_id == device_id).select():
        modulename.append(row.modulename)
    print modulename
    print "end of get_modulename"
    result = {'module_name':modulename}
    return response.json(result)


# @auth.requires_signature()
def get_data():
    """Ajax method that returns all data in a given date range.
    Generate with: URL('visualize', 'get_data', args=[
    device_id, module_name, name, date1, date2
    ]
    """
    print 1111111111111
    test_fill()
    print 2222222222222

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

    output_data = db((db.outputs.output_time_stamp >= start) &
                     (db.outputs.output_time_stamp <= end)).select()
    log_data = db((db.logs.logged_time_stamp >= start) &
                  (db.logs.logged_time_stamp <= end)).select()
    mixed_data = []


    print 'begin of output_data reading'
    for row in db((db.outputs.output_time_stamp >= start) & (db.outputs.output_time_stamp <= end)).select(orderby=db.outputs.output_time_stamp):
        type = 'output'
        device_id = row.device_id
        modulename = row.procedure_id
        time_stamp = row.output_time_stamp
        name = row.name
        value = row.output_value
        tag = row.tag
        content = 'name: ' + str(name) + ', value: ' + str(value) + ', tag: ' + str(tag)
        mixed_data.append({'type': type, 'device_id': device_id, 'modulename': modulename, 'time_stamp': time_stamp,'content': content})
    print 'end of output_data reading'
    # add log_data in
    for row in db((db.logs.logged_time_stamp >= start) & (db.logs.logged_time_stamp <= end)).select(orderby=db.logs.logged_time_stamp):
        type = 'log'
        device_id = row.device_id
        modulename = row.modulename
        time_stamp = row.logged_time_stamp
        log_level = row.log_level
        log_message = row.log_message
        content = 'name: ' + str(log_level) + ', value: ' + str(log_message)
        mixed_data.append({'type': type, 'device_id': device_id, 'modulename': modulename, 'time_stamp': time_stamp,
                           'content': content})


    print 'end of log_data reading'
    # sorted(mixed_data, key=mixed_data.time_stamp, reverse=False)
    mixed_data.sort(key=lambda r: r['time_stamp'])

    result = {'output_data': output_data, 'log_data': log_data, 'mixed_data': mixed_data}

    return response.json(result)


def visualization():
    return dict()
