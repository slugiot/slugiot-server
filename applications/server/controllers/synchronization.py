# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

# -*- coding: utf-8 -*-
import json

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html
    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))


@request.restful()
def recieve_update():
    def GET(*args, **vars):
        return response.json(['foo', {'bar': ('baz', None, 1.0, 2)}])

    def POST(*args, **vars):
        # get the log data from the request and validate
        request_body = request.body.read()
        if (not request_body):
            raise HTTP(400, "no data was included")

        # get json and validate structure
        try:
            log_data = json.loads(request_body)
        except:
            raise HTTP(400, "data was not json-formatted")
        if (not isinstance(log_data, dict)):
            raise HTTP(400, "data was not properly formatted")
        if (not "logs" in log_data and not isinstance(log_data.get('logs'), list)):
            raise HTTP(400, "data needs to have list of log messages as 'logs'")
        if (not "device_id" in log_data and not isinstance(log_data.get('device_id'), str)):
            raise HTTP(400, "data needs to have string device id as 'device_id'")

        # get information from document
        device_id = log_data.get('device_id')
        logs = log_data.get('logs')

        print(logs);

        for log in logs:
            if (not isinstance(log, dict)):
                raise HTTP(400, "all log entries must be of type 'dict'")
            log["device_id"] = device_id
            log["logged_time_stamp"] = log.get('time_stamp')


        return response.json({"log_data":logs})



    return locals()


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

def test_log_message():
    log_message = request.vars.log_message
    log_level = request.vars.log_level
    import procedureapi
    api = procedureapi.ProcedureApi("Test")
    api.write_log(log_message, log_level)
    return response.json({"result" : "done"})

def writing_to_db():
    current.db.logs.insert(time_stamp=datetime.datetime.utcnow(),modulename="Test",log_level=0,log_message="Writing to database0")
    current.db.logs.insert(time_stamp=datetime.datetime.utcnow(), modulename="Test", log_level=0,log_message="Writing to database1")
    current.db.logs.insert(time_stamp=datetime.datetime.utcnow(), modulename="Test", log_level=0,log_message="Writing to database2")
    return response.json({"result": "done"})

def reading_from_db():
    for row in db(db.logs.time_stamp > 0).iterselect():
        print row.log_message,row.time_stamp
