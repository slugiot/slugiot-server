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


# @auth.requires_signature()
def get_data():
    """Ajax method that returns all data in a given date range.
    Generate with: URL('visualize', 'get_data', args=[
    device_id, module_name, name, date1, date2
    ]
    """
    # Read chapter 3 of web2py book.  Or maybe
    device_id = request.args(0)
    module = request.args(1)
    out_var = request.args(2)
    date1 = datetime.parsedate(request.args(3))
    date2 = datetime.parsedate(request.args(4))
    if (device_id is None or module is None):
        raise HTTP(500)
    result = []
    for row in db((db.outputs.device_id == device_id) &
                          (db.outputs.modulename == module) &
                          (db.outputs.name == out_var) &
                          (db.output.timesteamp <= date2) &
                          (db.output.timestamp >= date1)).select():
        result.append(dict(d=row.timestamp.isoformat(), v=row.value))
    return response.json(result=result)


def visualization():
    return dict()
