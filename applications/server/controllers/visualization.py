# This controller contains some code useful for the visualization.

import access
import json_plus
import numbers


@auth.requires_login()
def visualize_output():
    """This controller visualizes an output variable.  In fact, the controller per se
    does very little: it simply validates the access and returns the javascript page.
    All the work is then done by the js in the page, along with the AJAX methods
    below in this controller file.
    Arguments:
        device_id/procedure_id/name
    """
    device_id = request.args(0)
    procedure_id = request.args(1)
    name = request.args(2)
    if device_id is None or procedure_id is None or name is None:
        logger.info("Missing parameters.")
        session.flash = T('Not Authorized.')
        redirect(URL('default', 'index'))
    # Validates access.
    if not access.can_view_procedure(auth.user_email, device_id, procedure_id):
        logger.info("Not authorized.")
        session.flash = T('Not Authorized.')
        redirect(URL('default', 'index'))
    # Does the procedure actually run on the device?
    r = db((db.runs_on.device_id == device_id) &
           (db.runs_on.procedure_id == procedure_id)).select().first()
    if r is None:
        logger.info("Procedure not running on device")
    # Builds a signed URL for the Ajax.
    ajax_url = URL('visualization', 'get_output_data',
                   args=[device_id, procedure_id, name], user_signature=True)
    return dict(ajax_url=ajax_url,
                procedure_name=r.procedure_name)


# Comment the following line out if you wish during testing, but remember
# to put it back or it is a BIG security risk.
@auth.requires_signature()
def get_output_data():
    """This is an AJAX function.
    Given an output device/table/variable name and a date range, returns
    the csv data consisting of the NUMERICAL data points (and their timestamps)
    in the date range.
    TODO: implement the daterange.
    args:
    device_id/procedure_id/name

    Returns:
        A json dictionary with two fields:
        "numerical_data": an array of numerical data in format suitable for dygraphs.
        "text_data": an array of timestamped text suitable for log visualization.
    """
    device_id = request.args(0)
    procedure_id = request.args(1)
    name = request.args(2)
    # I am assuming that the user has access to this information due to the signed URL.
    # Prepares the lists of data to be returned.
    numerical_data = []
    text_data = []
    for row in db((db.outputs.device_id == device_id) &
                          (db.outputs.procedure_id == procedure_id) &
                          (db.outputs.name == name)).select(orderby=db.outputs.output_time_stamp):
        # The output value is in json, so we decode it and we append it to the numerical or
        # text data, as appropriate.
        if row.output_value is not None:
            v = json_plus.Serializable.loads(row.output_value)
            if isinstance(v, numbers.Number):
                numerical_data.append(dict(data_date=row.output_time_stamp.isoformat(),
                                           data_value=v))
            else:
                text_data.append(dict(data_date=row.output_time_stamp.isoformat(),
                                      data_value=v))
    # That's all, folks.
    return response.json(dict(numerical_data=numerical_data,
                              text_data=text_data))


