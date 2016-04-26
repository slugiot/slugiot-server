jQuery(function() {

    // Ractive object
    var MAIN = new Ractive({
        el: '#target',
        template: '#template',
        delimiters: ['{%', '%}'],
        tripleDelimiters: ['{%%', '%%}'],
        data: {
            text_output: [],
        },
    });

    function get_data() {
        // Call server to get data.
        $.ajax({
            url: server_url,
            method: 'GET',
            data: {},
            success: function (data) {
                // Hide the spinner.
                $("#result-spinner").hide();

                // Set the output logs.
                MAIN.set('text_output', data['text_output']);

                // Create the dygraph.

                // Show the output.
                $("#output_section").show();

            }
            }
        )



    };



}