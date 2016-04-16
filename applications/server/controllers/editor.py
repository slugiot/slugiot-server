
# -*- coding: utf-8 -*-
# this file is used to test the editor


from datetime import datetime


def test_edit():
    return dict()

def edit_procedure():
    """ return json data to show the editor content """
    # Load json only if it is ajax edited...
    preferences={'theme':'web2py', 'editor': 'default', 'closetag': 'true', 'codefolding': 'false', 'tabwidth':'4', 'indentwithtabs':'false', 'linenumbers':'true', 'highlightline':'true'}
    codeId = request.vars.code
    data =  db(db.coding.id == codeId).select(db.coding.procedures).first().procedures
    file_details = dict(
                    editor_settings=preferences,
                    data=data,
                    id=codeId,
                    )
    plain_html = response.render('editor/edit_js.html', file_details)
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

