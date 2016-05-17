/**
 * Created by patrickyu on 4/21/16.
 */


    var ractive = new Ractive({
        el: '#target',
        template: '#template',
        delimiters: ['{%', '%}'],
        data: {
            mixed_data: [],
            output_data: [],
            log_data: []
        }
    });


    // ------------------------------------ START Refresh Button  ------------------------------------
    function refresh() {


        // ----------- get the parameter in the control panel --------------------------
        var time_span = $('#time_span').val();
        var elems = time_span.trim().split("-");
        var start = elems[0].slice(6, 10) + "-" + elems[0].slice(0, 2) + "-" + elems[0].slice(3, 5) + " 00:00:00";
        var end = elems[1].slice(7, 12) + "-" + elems[1].slice(1, 3) + "-" + elems[1].slice(4, 6) + " 23:59:59";

        $.ajax({
            'url': 'get_data',
            'type': 'post',
            'dataType': 'json',
            'data': {start: start, end: end},
            'success': function (data) {
                ractive.set({mixed_data: data.mixed_data});
                ractive.set({output_data: data.output_data});
                ractive.set({log_data: data.log_data});
                //  ---------- showing test output dygraph ----------
                dy_plot();
            }
        });

        //  ---------- showing test output dygraph ----------
        dy_plot();
    } // -------- END Refresh Button --------


    // ------------------------------------  Tab  ------------------------------------
    $('#myTabs a').click(function (e) {
        e.preventDefault()
        $(this).tab('show')
    })
    // ------------  Date Picker  ------------
    $(function () {
        $('#time_span').daterangepicker();
    });

    // ------------  Dygraph testing  ------------
    function barChartPlotter(e) {
        var ctx = e.drawingContext;
        var points = e.points;
        var y_bottom = e.dygraph.toDomYCoord(0);  // see <a href="http://dygraphs.com/jsdoc/symbols/Dygraph.html#toDomYCoord">jsdoc</a>

        // This should really be based on the minimum gap
        var bar_width = 2 / 3 * (points[1].canvasx - points[0].canvasx);
        ctx.fillStyle = e.color;  // a lighter shade might be more aesthetically pleasing

        // Do the actual plotting.
        for (var i = 0; i < points.length; i++) {
            var p = points[i];
            var center_x = p.canvasx;  // center of the bar

            ctx.fillRect(center_x - bar_width / 2, p.canvasy, bar_width, y_bottom - p.canvasy);
            ctx.strokeRect(center_x - bar_width / 2, p.canvasy, bar_width, y_bottom - p.canvasy);
        }
    }
    ;

    dy_plot = function () {
        var graph_com = document.getElementById("dygraph_target1");
        var output_data = ractive.get('output_data'); //"{{=URL('static', 'temper.csv')}}";


        // collecting output data
        if (typeof output_data === "undefined") {
            g = new Dygraph(
                    graph_com,
                    data,
                    {
                        //rollPeriod: 5,
                        //showRoller: true,
                        title: 'Temperature Line Chart',
                        ylabel: 'Temperature (C)',
                        legend: 'always',
                        showRangeSelector: true,
                        rangeSelectorHeight: 30,
                        rangeSelectorPlotStrokeColor: 'green',
                        rangeSelectorPlotFillColor: 'lightgreen'
                    }
            );
        }
        else if (output_data.length > 0) {
            var data = "Date, Temperature\n";   //[['Date', 'Temperature']];
            var dateRange = [];
            var timeSpan = $('#time_span').val();
            for (var i = 0; i < output_data.length; i++) {
                var output = output_data[i];
                data = data + output.output_time_stamp + ',' + output.output_value.toString() + '\n'
                if (i == 0 || i == output_data.length - 1)
                    dateRange.push(Date.parse(output.output_time_stamp));
                //data.push([output.time_stamp, output.output_value]);
            }
            /*if (typeof timeSpan !== "undefined") {
                var time2 = timeSpan.split("-");
                dateRange = [Date.parse(time2[0]), Date.parse(time2[1])];
            }*/

            g2 = new Dygraph(
                    graph_com,
                    data,
                    {
                        //labels: ['Date', 'Temperature'],
                        //plotter: barChartPlotter,
                        title: 'Temperature Line Chart',
                        ylabel: 'Temperature (C)',
                        legend: 'always',
                        dateWindow: dateRange,
                        showRangeSelector: true,
                        rangeSelectorHeight: 30,
                        rangeSelectorPlotStrokeColor: 'green',
                        rangeSelectorPlotFillColor: 'lightgreen'
                        //xTicker: Dygraph.dateTicker
                    }
            );

        }

    };

    dy_plot();
