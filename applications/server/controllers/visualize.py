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

    # Let us insert some new random data.
    now = datetime.datetime.utcnow()
    for i in range(3):
        db.outputs.insert(device_id=device_id,
                          modulename=module,
                          name=out_var,
                          time_stamp=now - datetime.timedelta(hours=i),
                          output_value=random.random(),
                          tag="1")
        db.logs.insert(device_id=device_id,
                       modulename=module,
                       time_stamp=now - datetime.timedelta(hours=i),
                       log_level=log_level,
                       log_message='This is message' + str(i) + '.')


# @auth.requires_signature()
def get_data():
    """Ajax method that returns all data in a given date range.
    Generate with: URL('visualize', 'get_data', args=[
    device_id, module_name, name, date1, date2
    ]
    """

    # result = {
    #     'mixed_data': [
    #         {
    #             'type': 'output',
    #             'deivce_id': 'home',
    #             'modulename': 'batman',
    #             'time_stamp': '2016-04-01',
    #             'content': 'name: temperature, value: 22, tag: 1'
    #         },
    #         {
    #             'type': 'log',
    #             'deivce_id': 'office',
    #             'modulename': 'superman',
    #             'time_stamp': '2016-04-02',
    #             'content': 'name: normal log, value: Your system went smoothly'
    #         },
    #         {
    #             'type': 'output',
    #             'deivce_id': 'office',
    #             'modulename': 'batman',
    #             'time_stamp': '2016-04-03',
    #             'content': 'name: temperature, value: 21, tag: 1'
    #         },
    #         {
    #             'type': 'log',
    #             'deivce_id': 'scholl',
    #             'modulename': 'superman',
    #             'time_stamp': '2016-04-04',
    #             'content': 'name: normal log, value: administrator logged in'
    #         }
    #     ],
    #     'output_data': [
    #         {
    #             'deivce_id': 'home',
    #             'modulename': 'batman',
    #             'name': 'temperature',
    #             'output_value': 22,
    #             'tag': '1',
    #             'time_stamp': '2016-04-01'
    #         },
    #         {
    #             'deivce_id': 'office',
    #             'modulename': 'batman',
    #             'name': 'temperature',
    #             'output_value': 26,
    #             'tag': '1',
    #             'time_stamp': '2016-04-02'
    #         },
    #         {
    #             'deivce_id': 'home',
    #             'modulename': 'batman',
    #             'name': 'temperature',
    #             'output_value': 20,
    #             'tag': '1',
    #             'time_stamp': '2016-04-03'
    #         },
    #         {
    #             'deivce_id': 'office',
    #             'modulename': 'batman',
    #             'name': 'temperature',
    #             'output_value': 23,
    #             'tag': '1',
    #             'time_stamp': '2016-04-04'
    #         }],
    #     'log_data': [
    #         {
    #             'device_id': 'office',
    #             'modulename': 'superman',
    #             'name': 'normal log',
    #             'output_value': 'Your system went smoothly',
    #             'time_stamp': '2016-04-01',
    #             'log_level': '0'
    #         },
    #         {
    #             'device_id': 'home',
    #             'modulename': 'superman',
    #             'name': 'normal log',
    #             'output_value': 'Your system just got modified',
    #             'time_stamp': '2016-04-02',
    #             'log_level': '0'
    #         },
    #         {
    #             'device_id': 'office',
    #             'modulename': 'superman',
    #             'name': 'critical log',
    #             'output_value': 'Unauthorized logged in',
    #             'time_stamp': '2016-04-03',
    #             'log_level': '4'
    #         },
    #         {
    #             'device_id': 'home',
    #             'modulename': 'superman',
    #             'name': 'normal log',
    #             'output_value': 'guest logged in',
    #             'time_stamp': '2016-04-04',
    #             'log_level': '0'
    #         }
    #     ]
    # }
    # Read chapter 3 of web2py book.  Or maybe
    # device_id = request.args(0)
    # module = request.args(1)
    # out_var = request.args(2)
    # date1 = datetime.parsedate(request.args(3))
    # date2 = datetime.parsedate(request.args(4))
    # if (device_id is None or module is None):
    #     raise HTTP(500)
    # for row in db((db.outputs.device_id == device_id) &
    #                       (db.outputs.modulename == module) &
    #                       (db.outputs.name == out_var) &
    #                       (db.output.timesteamp <= date2) &
    #                       (db.output.timestamp >= date1)).select():
    #     result.append(dict(d=row.timestamp.isoformat(), v=row.value))
    test_fill()
    result = []
    print 111
    print 1
    # dd = db(db.outpts).select()
    print 3

    # s = request.get('start')
    # e = request.get('end')
    #
    # print s
    # print e
    s = request.vars.start
    e = request.vars.end

    print s
    # start = datetime.strptime("2016-05-03 21:20:20", "%Y-%m-%d %H:%M:%S")
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

    start = datetime.datetime(start_year, start_month, start_day, start_hour, start_minute, start_second)
    end = datetime.datetime(end_year, end_month, end_day, end_hour, end_minute, end_second)
    print start
    print end
    print s

    output_data = db((db.outputs.time_stamp >= start) &
                     (db.outputs.time_stamp <= end)).select()
    log_data = db((db.logs.time_stamp >= start) &
                  (db.logs.time_stamp <= end)).select()
    mixed_data = []

    for row in db((db.outputs.time_stamp >= start) & (db.outputs.time_stamp <= end)).select(orderby=db.outputs.time_stamp):
        type = 'output'
        device_id = row.device_id
        modulename = row.modulename
        time_stamp = row.time_stamp
        name = row.name
        value = row.output_value
        tag = row.tag
        content = 'name: ' + str(name) + ', value: ' + str(value) + ', tag: ' + str(tag)
        mixed_data.append({'type': type, 'device_id': device_id, 'modulename': modulename, 'time_stamp': time_stamp,
                           'content': content})
        print "before mixed"
        # db.mixed_data.insert(device_type=type,
        #                      device_id=device_id,
        #                      modulename=modulename,
        #                      time_stamp=time_stamp,
        #                      device_content=content
        #                      )
        #             'type': 'log',
        #             'deivce_id': 'scholl',
        #             'modulename': 'superman',
        #             'time_stamp': '2016-04-04',
        #             'content': 'name: normal log, value: administrator logged in'
    # add log_data in
    for row in db((db.logs.time_stamp >= start) & (db.logs.time_stamp <= end)).select(orderby=db.logs.time_stamp):
        type = 'log'
        device_id = row.device_id
        modulename = row.modulename
        time_stamp = row.time_stamp
        log_level = row.log_level
        log_message = row.log_message
        content = 'name: ' + str(log_level) + ', value: ' + str(log_message)
        mixed_data.append({'type': type, 'device_id': device_id, 'modulename': modulename, 'time_stamp': time_stamp,
                           'content': content})
        # db.mixed_data.insert(device_type=type,
        #                      device_id=device_id,
        #                      modulename=modulename,
        #                      time_stamp=time_stamp,
        #                      device_content=content
        #                      )
    # for row in db(db.mixed_data).select(orderby=db.mixed_data.time_stamp):
    #     type = row.device_type
    #     device_id = row.device_id
    #     modulename = row.modulename
    #     time_stamp = row.time_stamp
    #     content = row.device_content
    #     mixed_data.append({'type': type, 'device_id': device_id, 'modulename': modulename, 'time_stamp': time_stamp,
    #                        'content': content})
    # print log_data
    print 222
    # sorted(mixed_data, key=mixed_data.time_stamp, reverse=False)
    mixed_data.sort(key=lambda r: r['time_stamp'])
    # print "the size of the mixed_data is " + str(mixed_data.count())
    print mixed_data
    print 333
    result = {'output_data': output_data, 'log_data': log_data, 'mixed_data': mixed_data}

    return response.json(result)


def visualization():
    return dict()
