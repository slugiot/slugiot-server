
# -*- coding: utf-8 -*-
# this file is used to test the editor


from datetime import datetime

def edit_procedure():
    """
    return json data to show the editor content
    """
    #parameter for CodeMirror option parameter used for setting the editor feature
    preferences={'theme':'web2py', 'editor': 'default', 'closetag': 'true', 'codefolding': 'false', 'tabwidth':'4', 'indentwithtabs':'false', 'linenumbers':'true', 'highlightline':'true'}

    code_id = request.vars.procedure_id

    #the final edition will use Team 2 API "get_procedure_data(procedure_id, stable)"  to get the data
    #we debug with temporary table to validate the function of editor
    data =  db(db.coding.id == code_id).select(db.coding.procedures).first().procedures

    file_details = dict(
                    editor_settings=preferences, #the option parameters used for setting editor feature.
                    id=code_id, #the procedure_id in the procedures TALBE
                    data=data, # code for procedure which is related with the id.
                    )

    #generated HTML code for editor by parameters in file_details
    plain_html = response.render('editor/edit_js.html', file_details)

    file_details['plain_html'] = plain_html
    return response.json(file_details)

def save_procedure():
    """
    return the save result for the saving procedure
    """
    code_id = request.vars.procedure_id
    data = request.vars.procedure
    stable = request.vars.stable
    #save the procedure data to the database
    if stable is False:

        #the final edition will use Team 2 API save(procedure_id, stable) to save the data
        #we debug with temporary table to validate the function of editor
        db(db.coding.id == code_id).update(procedures =data)
    return dict(result='true')


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
    return dict(result = now)

def select():
    """
    This function is only used for self debug to show exited procedure in database
    Team 2 provide the API get_procedures_for_user(user_id) to return the list of procedure_id belong to a user
    This function will be deleted in the final edition
    """
    return dict(code_list = db(db.coding).select())


def test_edit():
    """
    This is served for the test example view page, which help UI team to integrate editor
    This function will be delete at final edition
    """
    procedure_id = request.vars.procedure_id
    return dict(procedure_id = procedure_id)
