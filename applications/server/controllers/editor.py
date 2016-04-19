
# -*- coding: utf-8 -*-
# this file is used to test the editor


from datetime import datetime

def edit_procedure():
    """
    return json data to show the editor content
    """
    # Load json only if it is ajax edited...
    preferences={'theme':'web2py', 'editor': 'default', 'closetag': 'true', 'codefolding': 'false', 'tabwidth':'4', 'indentwithtabs':'false', 'linenumbers':'true', 'highlightline':'true'}
    codeId = request.vars.procedure_id
    """
    the final edition will use Team 2 API get_procedures_for_user(user_id) to get the data
    we debug with temporary table to validate the function of editor
    """
    data =  db(db.coding.id == codeId).select(db.coding.procedures).first().procedures
    file_details = dict(
                    editor_settings=preferences,
                    data=data,
                    id=codeId,
                    )
    plain_html = response.render('editor/edit_js.html', file_details)
    file_details['plain_html'] = plain_html
    return response.json(file_details)





## all the following function is used for self debug and will be deleted at final edition

def create():
    """
    This function is only used for self debug to create a new procedure
    Team 2 provide the API create_procedure() to create a new procedure and return the procedure_id
    This function will be deleted in the final edition
    """
    now = datetime.utcnow()
    code = "# enter your new procedure in the following" + now.strftime("%Y-%m-%d %H:%M:%S")
    db.coding.insert(procedures=code, times=now)
    result = 'ok'
    return dict(result = now)

def select():
    """
    This function is only used for self debug to show exited procedure in database
    Team 2 provide the API get_procedures_for_user(user_id) to return the list of procedure_id belong to a user
    This function will be deleted in the final edition
    """
    row= db(db.coding).select().first()
    if row is not None:
        rows = db(db.coding).select()
        code_list = [{'id': r.id, 'procedures': r.procedures, 'times': r.times} for r in rows]
        return dict(exit = 1, code_list = code_list)
    return dict(exit = 0)

def test_edit():
    """
    This is served for the test demon view page, which help UI team to integrate editor
    This function will be delete at final edition
    """
    procedure_id = request.vars.procedure_id
    return dict(procedure_id = procedure_id)
