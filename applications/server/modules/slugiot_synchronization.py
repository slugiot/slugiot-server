from gluon import current
import json_plus

"""
We want to move functions from the synchronization controller into here in the same way we did
for the client.  Then change the controller to invoke these functions.

I think we may want to skip the slugiot_setup thing we have in the client.
"""

def do_something():
    if current.db:
        print "we have db"
    else:
        print "no db!"
        
        

def receive_append_data(json_data, table_name):
    data = get_validated_data(json_data, table_name)

    # get information from document
    device_id = data.get('device_id')
    data_to_append = data.get(table_name)

    for datum in data_to_append:
        if (not isinstance(datum, dict)):
            raise Exception("all entries must be of type 'dict'")
        datum["device_id"] = device_id
        if (datum.get('id')):
            del datum['id']

    current.db[table_name].bulk_insert(data_to_append)

    return data_to_append
        
        
def receive_keyvalue_data(json_data, table_name, key_column, value_column):
    data = get_validated_data(json_data, table_name)

    # get information from document
    device_id = data.get('device_id')
    keyvalue_data = data.get(table_name)

    for datum in keyvalue_data:
        if (not isinstance(datum, dict)):
            raise Exception("all entries must be of type 'dict'")
        datum["device_id"] = device_id
        if (datum.get('id')):
            del datum['id']

    for datum in keyvalue_data:
        # get data and build record;
        key = datum[key_column]
        value = datum[value_column]
        procedure_id = None
        if (datum.has_key('procedure_id')):
            procedure_id = datum['procedure_id']
        update_or_insert_data = dict()
        update_or_insert_data['device_id']
        update_or_insert_data['procedure_id'] = procedure_id
        update_or_insert_data[key_column] = key
        update_or_insert_data[value_column] = value

        # do the insert_or_update
        current.db[table_name].update_or_insert(
            (
                (current.db[table_name][key_column] == key) &
                (current.db[table_name]['procedure_id'] == procedure_id) &
                (current.db[table_name]['device_id'] == device_id)
            ),
            update_or_insert_data)

    return keyvalue_data



def get_validated_data(request_body, data_key):
    """
    This function takes in the data and ensures that it has the right format along with a device id  - {{"James",9001},{"Jo",3474},{"Jack",323}}

       :param p1: request_body for the data to be formatted properly
       :type p1: str
       :param p1: data_key
       :type p1: str
       :return: Data in a dictionary containing json-formatted data that has a device_id
       :rtype: Dictionary
    """
    if (not request_body):
        raise Exception("no data was included")
    try:
        data = json_plus.Serializable.loads(request_body)
    except:
        raise Exception("data was not json-formatted")
    if (not isinstance(data, dict)):
        raise Exception("data was not properly formatted")
    if (not data_key in data or not isinstance(data.get(data_key), list)):
        raise Exception("data needs to have list of data entries as '" + data_key + "'")
    if (not "device_id" in data and not isinstance(data.get('device_id'), str)):
        raise Exception("data needs to have string device id as 'device_id'")
    validate_device_id(data['device_id'])

    return data

def validate_device_id(device_id):
    device_id_rows = current.db(current.db.device.device_id == device_id).select()
    if (len(device_id_rows) > 0):
        return
    else:
        raise Exception("invalid device id")