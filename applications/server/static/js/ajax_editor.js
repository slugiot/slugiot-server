function load_file(url) {
  $.getJSON(url, function (json) {

      if(typeof (json['plain_html']) !== undefined) {
        if($('#' + json['id']).length === 0 ) {
          //  the code in it
          var tab_body = '<div id="' + json['id'] + '" class="tab-pane fade in " >' + json['plain_html'] + '</div>';
            $('#myTabContent').append($(tab_body)); // First load the body
        }
      }
  }).fail(function() {
      on_error();
  });
  return false;
}

