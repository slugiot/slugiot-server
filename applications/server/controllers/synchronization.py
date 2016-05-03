# -*- coding: utf-8 -*-
import json

@request.restful()
def receive_logs():
    """
    This method is to recieve log data.  It accepts two HTTP methods:
        GET: returns the latest three log entries.  planning on adding
            filtering based on device_id, and how many records to return
        POST: accepts a JSON document with the log entries to ingest.  an
            example document is described below:
            {
                "device_id":"my_device",
                "logs":
                    [
                        {"modulename":"my_module","log_level":3,"log_message":"some message","time_stamp":"2016-03-19 20:48:41"},
                        {"modulename":"my_module","log_level":2,"log_message":"some other message","time_stamp":"2016-03-19 20:49:41"}
                    ]
            }
    """
    def GET(*args, **vars):
        logs = db(db.logs).select(orderby="received_time_stamp DESC",limitby=(0,3))
        return response.json(logs)

    def POST(*args, **vars):
        # get the log data from the request and validate
        request_body = request.body.read()
        log_data = __get_valdiated_data(request_body, "logs")

        # get information from document
        device_id = log_data.get('device_id')
        logs = log_data.get('logs')

        for log in logs:
            if (not isinstance(log, dict)):
                raise HTTP(400, "all log entries must be of type 'dict'")
            log["device_id"] = device_id
            if (log.get('time_stamp')):
                log["logged_time_stamp"] = log.get('time_stamp')
                del log['time_stamp']
            if (log.get('id')):
                del log['id']

        try:
            db.logs.bulk_insert(logs)
        except Exception as e:
            raise HTTP(400, "there was an error saving log data: " + e.message)

        return response.json({"saved_logs":logs})

    return locals()


@request.restful()
def receive_outputs():
    """
    This method is to recieve output data.  It accepts two HTTP methods:
        GET: returns the latest output entries.  planning on adding
            filtering based on device_id, and how many records to return
        POST: accepts a JSON document with the output entries to ingest.  an
            example document is described below:
            {
                "device_id":"my_device",
                "output":
                    [
                        {"modulename":"my_module","name":"variable","output_value":"10","tag":"example","time_stamp":"2016-03-19 20:48:41"}
                    ]
            }
    """

    def GET(*args, **vars):
        logs = db(db.outputs).select(orderby="received_time_stamp DESC", limitby=(0, 3))
        return response.json(logs)

    def POST(*args, **vars):
        # get the log data from the request and validate
        request_body = request.body.read()
        output_data = __get_valdiated_data(request_body, 'outputs')

        # get information from document
        device_id = output_data.get('device_id')
        output = output_data.get('outputs')

        for out in output:
            if (not isinstance(out, dict)):
                raise HTTP(400, "all output entries must be of type 'dict'")
            out["device_id"] = device_id
            if (out.get('time_stamp')):
                out["output_time_stamp"] = out.get('time_stamp')
                del out['time_stamp']
            if (out.get('id')):
                del out['id']

        try:
            db.outputs.bulk_insert(output)
        except Exception as e:
            raise HTTP(400, "there was an error saving log data: " + e.message)

        return response.json({"saved_logs": output})

    return locals()


@request.restful()
def receive_values():
    """
    This method is to receive value data.  It accepts two HTTP methods:
        GET: returns all the current output entries (for the device id)
        POST: accepts a JSON document with the value entries to ingest.
            all current entries (for the device_id) will be removed and replaced
            with the ones submitted.
            an example document is described below:
            {
                "device_id":"my_device",
                "values":
                    [
                        {"procedure_id":"proc1","name":"some_name","output_value":"some_value","time_stamp":"2016-04-19 01:04:25"},
                        {"procedure_id":"proc2","name":"some_other_name","output_value":"some_other_value"}
                    ]
            }
    """

    def GET(*args, **vars):
        if (vars == None or not vars.has_key('device_id')):
            raise HTTP(400, "Please specify 'device_id' as a parameter to retrieve values")
        device_id = vars['device_id']
        vars = db(db.module_values.device_id == device_id).select()
        return response.json(vars)

    def POST(*args, **vars):
        # get the log data from the request and validate
        request_body = request.body.read()
        values_data = __get_valdiated_data(request_body, 'values')

        # get information from document
        device_id = values_data.get('device_id')
        values = values_data.get('values')

        for value in values:
            if (not isinstance(value, dict)):
                raise HTTP(400, "all value entries must be of type 'dict'")
            value["device_id"] = device_id
            if (value.get('time_stamp')):
                value["value_time_stamp"] = value.get('time_stamp')
                del value['time_stamp']
            if (value.get('id')):
                del value['id']

        try:
            db(db.module_values.device_id == device_id).delete()
            db.module_values.bulk_insert(values)
        except Exception as e:
            db.rollback()
            raise HTTP(400, "there was an error saving value data: " + e.message)

        return response.json({"saved_values": values})

    return locals()


@request.restful()
def get_settings():
    """
    This method is to receive setting data.  Given a device_id, it returns
    all the setting information that the client needs.  If the parameter
    'last_updated' is set, it will only select changed settings
    since that time

    If you POST to this endpoint, it will save posted settings to the DB.
    This is intended to be used for debugging:
    {
      "device_id":"trevor",
      "settings":[
            {"procedure_id":"proc1","setting_name":"some_setting","setting_value":"42"},
            {"setting_name":"some_global_setting","setting_value":True}
      ]
    }
    """

    def GET(*args, **vars):
        if (vars == None or not vars.has_key('device_id')):
            raise HTTP(400, "Please specify 'device_id' as a parameter to retrieve settings")
        device_id = vars['device_id']
        last_updated = datetime.fromtimestamp(1)
        if (vars.has_key('last_updated')):
            last_updated = vars['last_updated']

        settings = db((db.client_setting.device_id == device_id) & (db.client_setting.last_updated > last_updated)).select()
        return response.json(settings)

    def POST(*args, **vars):
        # get the log data from the request and validate
        request_body = request.body.read()
        values_data = __get_valdiated_data(request_body, 'settings')

        # get information from document
        device_id = values_data.get('device_id')
        settings = values_data.get('settings')

        for setting in settings:
            if (not isinstance(setting, dict)):
                raise HTTP(400, "all setting entries must be of type 'dict'")
            setting["device_id"] = device_id
            if (setting.get('id')):
                del setting['id']

        try:
            if (vars.has_key('delete_existing_settings') and vars['delete_existing_settings'] == "true"):
                db(db.client_setting.device_id == device_id).delete()
            for setting in settings:
                setting_name = setting['setting_name']
                setting_value = setting['setting_value']
                procedure_id = None
                if (setting.has_key('procedure_id')):
                    procedure_id = setting['procedure_id']
                db.client_setting.update_or_insert(
                    ((db.client_setting.setting_name == setting_name) & (db.client_setting.procedure_id == procedure_id) & (db.client_setting.device_id == device_id)),
                    setting_name=setting_name, setting_value=setting_value, procedure_id=procedure_id, device_id=device_id)

        except Exception as e:
            db.rollback()
            raise HTTP(400, "there was an error saving setting data: " + e.message)

        return response.json({"saved_settings": settings})

    return locals()


def __get_valdiated_data(request_body, data_key):
    if (not request_body):
        raise HTTP(400, "no data was included")

    # get json and validate structure
    try:
        data = json.loads(request_body)
    except:
        raise HTTP(400, "data was not json-formatted")
    if (not isinstance(data, dict)):
        raise HTTP(400, "data was not properly formatted")
    if (not data_key in data or not isinstance(data.get(data_key), list)):
        raise HTTP(400, "data needs to have list of data entries as '" + data_key + "'")
    if (not "device_id" in data and not isinstance(data.get('device_id'), str)):
        raise HTTP(400, "data needs to have string device id as 'device_id'")

    return data

"""
This function takes in a table_name (logs, outputs, etc) and returns the latest timestamp the data was synchronized

   :param p1: table_name
   :type p1: str
   :return: Timestamp of latest entry in a database table
   :rtype: datetime
"""

def __get_last_synchronized(table_name):
    timestamp =  db(db.table_name == table_name).select(db.time_stamp, orderby="time_stamp DESC", limitby=(0, 1))
    if (not timestamp):
        return datetime.datetime.fromtimestamp(0)
    return timestamp[0].time_stamp

"""
   This method checks the last timestamp that is stored in the server against the timestamp stored in the client
   and puts all the unsycnhed information into the server database, after which, it sends a response if successful
"""

def synch():

#Retreiving last timestamp from the three tables to be synched to server from client
    a = __get_last_synchronized(db.logs)
    b = __get_last_synchronized(db.outputs)
    c = __get_last_synchronized(db.module_values)

#Retreiving last timestamp from the three tables in client





