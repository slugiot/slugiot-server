

/**
 * @param procedure_id
 * request procedure data from server and initialize the html content of editor
 */
function load_procedure(url ,procedure_id, stable, device_id) {
    $.ajax({
        dataType: "json",
        url: url,
        data: {
            procedure_id : procedure_id,
            stable: stable,
            device_id: device_id
        },
        success: function(json) {
            if(typeof (json['plain_html']) !== undefined) {
                if($('#' + json['id']).length === 0 ) {
                    //  the code in it
                    var tab_body = '<div id="' + json['id'] + '" class="tab-pane fade in " >' + json['plain_html'] + '</div>';
                    $('#myTabContent').append($(tab_body)); // First load the body
                    
                    // Load procedure list at left side
                    var procedure_list = '';
                    for (var i = 0; i < json['id_list'].length; i++) {
                        procedure_list += '<button ';
                        procedure_list += 'type = "button" ';
                        procedure_list += 'class="list-group-item" ';
                        procedure_list += 'id="' + json['id_list'][i] + '" ';
                        procedure_list += 'href="{{=URL(' + '"editor","test_edit",vars=dict(device_id=' + json['dev_id'] + ',procedure_id=' + json['id_list'][i] + ',stable="false"),user_signature=True)}}' + '">';
                        // href="{{=URL('editor','test_edit',vars=dict(device_id='1',procedure_id=id_list[0],stable='false'),user_signature=True)}}"
                        procedure_list += json['id_list'][i];
                        procedure_list += '</button>';
                        //procedure_list += '<button type="button" class="list-group-item" id="' + json['id_list'][i] + '">' + json['id_list'][i] + '</button>';
                    }
                    $('#procedures').append($(procedure_list));
                }
            }
        },
        error: function() {
            console.log('load_procedure error');
        }

    });
}


/**
 * @param procedure_id
 * @param stable
 * save procedure data to server, if stable is false save temporary procedure, if stable is true save stable procedure
 */
function save_procedure(url, procedure_id, stable) {
    var editor = $('textarea').data('editor');
    var code_data = editor.getValue();
    $('#save_result').html('<div>saving files ...</div>')
    $.ajax({
        dataType: "json",
        url: url,
        method: "POST",
        data: {
           procedure_id : procedure_id,
           stable : stable,
           procedure : code_data
        },
        success: function(json) {
            $('#save_result').html(json['result']);
            if(json.highlight) {
            doHighlight(json.highlight);
            }
        },
        error: function() {
            console.log('save_procedure error');
        }
    });
}


/**
 * @param highlight
 * doHighlight will move the cursor to the line which have compile error
 */
function doHighlight(highlight) {
  // Put the cursor at the offending line:
  editor.setCursor({
    line: highlight.lineno - 1,
    ch: highlight.offset + 1
  });
}

/**
 * @param procedure_id
 * @param device_id
 * delete procedure data to server
 */
function delete_procedure(url ,procedure_id, device_id) {
    console.log(procedure_id);
    console.log("oo");
    console.log(device_id);
    $.ajax({
        dataType: "json",
        url: url,
        method: "POST",
        data: {
            procedure_id : procedure_id,
            device_id: device_id
        },
        success: function(json) {
        },
        error: function() {
            console.log('delete_procedure error');
        }

    });
}
