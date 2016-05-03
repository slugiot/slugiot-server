import datetime
import random


def test_fill():
    """Fills some data for visualization."""
    device_id = "chicken"
    module = "egg"
    out_var = "x"
    # Let us clear previous data.
    db((db.outputs.device_id == device_id) &
       (db.outputs.modulename == module) &
       (db.outputs.name == out_var)).delete()
    # Let us insert some new random data.
    now = datetime.datetime.utcnow()
    for i in range(10):
        db.outputs.insert(device_id=device_id,
                          modulename=module,
                          name=out_var,
                          timestamp=now - datetime.timedelta(hours=i),
                          output_value=random.random())
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

    result = {
        'mixed_data': [
            {
                'type': 'output',
                'deivce_id': 'home',
                'modulename': 'batman',
                'time_stamp': '2016-04-01',
                'content': 'name: temperature, value: 22, tag: 1'
            },
            {
                'type': 'log',
                'deivce_id': 'office',
                'modulename': 'superman',
                'time_stamp': '2016-04-02',
                'content': 'name: normal log, value: Your system went smoothly'
            },
            {
                'type': 'output',
                'deivce_id': 'office',
                'modulename': 'batman',
                'time_stamp': '2016-04-03',
                'content': 'name: temperature, value: 21, tag: 1'
            },
            {
                'type': 'log',
                'deivce_id': 'scholl',
                'modulename': 'superman',
                'time_stamp': '2016-04-04',
                'content': 'name: normal log, value: administrator logged in'
            }
        ],
        'output_data': [
            {
                'deivce_id': 'home',
                'modulename': 'batman',
                'name': 'temperature',
                'output_value': 22,
                'tag': '1',
                'time_stamp': '2016-04-01'
            },
            {
                'deivce_id': 'office',
                'modulename': 'batman',
                'name': 'temperature',
                'output_value': 26,
                'tag': '1',
                'time_stamp': '2016-04-02'
            },
            {
                'deivce_id': 'home',
                'modulename': 'batman',
                'name': 'temperature',
                'output_value': 20,
                'tag': '1',
                'time_stamp': '2016-04-03'
            },
            {
                'deivce_id': 'office',
                'modulename': 'batman',
                'name': 'temperature',
                'output_value': 23,
                'tag': '1',
                'time_stamp': '2016-04-04'
            }],
        'log_data': [
            {
                'device_id': 'office',
                'modulename': 'superman',
                'name': 'normal log',
                'output_value': 'Your system went smoothly',
                'time_stamp': '2016-04-01',
                'log_level': '0'
            },
            {
                'device_id': 'home',
                'modulename': 'superman',
                'name': 'normal log',
                'output_value': 'Your system just got modified',
                'time_stamp': '2016-04-02',
                'log_level': '0'
            },
            {
                'device_id': 'office',
                'modulename': 'superman',
                'name': 'critical log',
                'output_value': 'Unauthorized logged in',
                'time_stamp': '2016-04-03',
                'log_level': '4'
            },
            {
                'device_id': 'home',
                'modulename': 'superman',
                'name': 'normal log',
                'output_value': 'guest logged in',
                'time_stamp': '2016-04-04',
                'log_level': '0'
            }
        ]
    }
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
    
    return response.json(result)


def visualization():
    return dict()
