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





