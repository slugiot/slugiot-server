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
    // Extra plotting style
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
    };

    function multiColumnBarPlotter(e) {
        // We need to handle all the series simultaneously.
        if (e.seriesIndex !== 0) return;

        var g = e.dygraph;
        var ctx = e.drawingContext;
        var sets = e.allSeriesPoints;
        var y_bottom = e.dygraph.toDomYCoord(0);

        // Find the minimum separation between x-values.
        // This determines the bar width.
        var min_sep = Infinity;
        for (var j = 0; j < sets.length; j++) {
            var points = sets[j];
            for (var i = 1; i < points.length; i++) {
              var sep = points[i].canvasx - points[i - 1].canvasx;
              if (sep < min_sep) min_sep = sep;
            }
        }
        var bar_width = Math.floor(2.0 / 3 * min_sep);

        var fillColors = [];
        var strokeColors = g.getColors();
        for (var i = 0; i < strokeColors.length; i++) {
            fillColors.push(darkenColor(strokeColors[i]));
        }

        for (var j = 0; j < sets.length; j++) {
            ctx.fillStyle = fillColors[j];
            ctx.strokeStyle = strokeColors[j];
            for (var i = 0; i < sets[j].length; i++) {
                var p = sets[j][i];
                var center_x = p.canvasx;
                var x_left = center_x - (bar_width / 2) * (1 - j/(sets.length-1));

                ctx.fillRect(x_left, p.canvasy,
                    bar_width/sets.length, y_bottom - p.canvasy);

                ctx.strokeRect(x_left, p.canvasy,
                    bar_width/sets.length, y_bottom - p.canvasy);
            }
        }
    };

    // Darken a color
    function darkenColor(colorStr) {
        // Defined in dygraph-utils.js
        var color = Dygraph.toRGB_(colorStr);
        color.r = Math.floor((255 + color.r) / 2);
        color.g = Math.floor((255 + color.g) / 2);
        color.b = Math.floor((255 + color.b) / 2);
        return 'rgb(' + color.r + ',' + color.g + ',' + color.b + ')';
    };

    dy_plot = function () {
        var graph_com = document.getElementById("dygraph_target1");
        var output_data = ractive.get('output_data'); //"{{=URL('static', 'temper.csv')}}";
        var check_module = ['egg','eggnog'];  // later should get from the server (ajax or ractive)

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
            var data_dict = {};     // use dict to storage data for dygraph, then transfer to csv formate
            var dateRange = [];
            var timeSpan = $('#time_span').val();

            var label = ['Date'];
            for (var j = 0; j <check_module.length; j++){
                label.push(check_module[j]);
            }

            for (var i = 0; i < output_data.length; i++) {
                var output = output_data[i];
                if (i == 0 || i == output_data.length - 1)
                    dateRange.push(Date.parse(output.time_stamp));
                // use dict to storage
                if (output.procedure_id == check_module[0]){
                    data_dict[output.time_stamp] = [output.output_value, null];
                }
                else{
                    if (output.time_stamp in data_dict){
                        data_dict[output.time_stamp][1] = output.output_value;
                    }
                    else{
                        data_dict[output.time_stamp] = [null, output.output_value]
                    }
                }
            }
            /*if (typeof timeSpan !== "undefined") {
                var time2 = timeSpan.split("-");
                dateRange = [Date.parse(time2[0]), Date.parse(time2[1])];
            }*/

            //var datas = [];  // try to use native format, but output graph not correct (bug)
            // bug? yaxisrange not correct and rangeselector also not show up correctly.
            //var datas = label[0] + ','+ label[1] + ',' + label[2] + '\n';
            var data = '';
            for (var i in label)
                data += label[i] + ',';
            data = data.slice(0, data.length-1) + '\n';

            for (var item in data_dict)
            {
                //datas += item + ',' + data_dict[item][0] + ',' + data_dict[item][1] + '\n';
                data += item + ',';
                for (var i in data_dict[item])
                    data += data_dict[item][i] + ',';
                data = data.slice(0, data.length-1) + '\n';
            }

            g2 = new Dygraph(
                    graph_com,
                    data,
                    {
                        //labels: label,//['Date', 'Temperature'],
                        title: 'Temperature Line Chart',
                        ylabel: 'Temperature (C)',
                        legend: 'always',
                        //connectSeparatedPoints: true,
                        drawPoints: true,
                        dateWindow: dateRange,
                        //valueRange: [0,30],
                        rollPeriod: 3,
                        showRoller: true,
                        //errorBars: true,
                        showRangeSelector: true,
                        rangeSelectorHeight: 30,
                        rangeSelectorPlotStrokeColor: 'green',
                        rangeSelectorPlotFillColor: 'lightgreen'
                        //plotter: barChartPlotter,
                        //xTicker: Dygraph.dateTicker
                    }
            );

        }

    };

    function line_plot(){
        g2.updateOptions({plotter: DygraphCanvasRenderer._linePlotter, title: 'Temperature Line Chart'});
    };
    function bar_plot(){
        g2.updateOptions({plotter: multiColumnBarPlotter, title: 'Temperature Bar Chart'});
    };

    dy_plot();
