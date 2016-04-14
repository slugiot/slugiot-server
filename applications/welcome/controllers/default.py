# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))


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

from datetime import datetime

"""
inorder to test we need to define a table

db.define_table('coding',
            Field('procedures', 'text'),
            Field('times','datetime')
            )
"""

def edit():
    return dict()

def edit_procedure():
    """ return json data to show the editor content """
    # Load json only if it is ajax edited...
    preferences={'theme':'web2py', 'editor': 'default', 'closetag': 'true', 'codefolding': 'false', 'tabwidth':'4', 'indentwithtabs':'false', 'linenumbers':'true', 'highlightline':'true'}
    codeId = request.vars.code
    data =  db(db.coding.id == co).select(db.coding.procedures).first().procedures
    file_details = dict(
                    editor_settings=preferences,
                    data=data,
                    id=codeId,
                    )
    plain_html = response.render('default/edit_js.html', file_details)
    file_details['plain_html'] = plain_html
    return response.json(file_details)


def create():
    """
    create a new procedure
    """
    now = datetime.utcnow()
    code = "# enter your new procedure in the following" + now.strftime("%Y-%m-%d %H:%M:%S")
    db.coding.insert(procedures=code, times=now)
    result = 'ok'
    return dict(result = now)

def select():
    """
    search for the exit procedure in the database
    :return:
    """
    row= db(db.coding).select().first()
    if row is not None:
        rows = db(db.coding).select()
        code_list = [{'id': r.id, 'procedures': r.procedures, 'times': r.times} for r in rows]
        return dict(exit = 1, code_list = code_list)
    return dict(exit = 0)