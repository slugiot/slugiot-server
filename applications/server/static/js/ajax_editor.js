

/**
 * @param procedure_id
 * request procedure data from server and initialize the html content of editor
 */
function load_procedure(url ,procedure_id, stable) {
    $.ajax({
        dataType: "json",
        url: url,
        data: {
            procedure_id : procedure_id,
            stable: stable
        },
        success: function(json) {
            if(typeof (json['plain_html']) !== undefined) {
            if($('#' + json['id']).length === 0 ) {
              //  the code in it
              var tab_body = '<div id="' + json['id'] + '" class="tab-pane fade in " >' + json['plain_html'] + '</div>';
            $('#myTabContent').append($(tab_body)); // First load the body
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