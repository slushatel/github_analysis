$(function () {
    var ctx = document.getElementById("data-chart");
    var myChart = null;

    function loadParameters() {
        $.ajax({
            url: "/parameters",
        }).done(function (data) {
            data.forEach(function (item) {
                var newElem = $("<div>").attr("id", item.id).text(item.text).data({"reverseUrl": item.reverse_url})
                    .addClass("parameter-link");
                $("#parameters").append(newElem);
            })
        });
    }

    $("body").on("click", ".parameter-link", function () {
        $.ajax({
            url: $(this).data("reverseUrl"),
        }).done(function (data) {
            console.log(data);
            if (data.value !== undefined) {
                var chart_datasets = data.value.chart_datasets;
                var chart_title = data.value.chart_title;

                var chart_data = JSON.parse(data.value.chart_json);
                var axises = [];
                var axis_names = [];
                for (var prop in chart_data) {
                    axis_names.push(prop);
                    axis_data = [];
                    for (var prop_axis in chart_data[prop]) {
                        axis_data.push(chart_data[prop][prop_axis]);
                    }
                    axises.push(axis_data);
                }
                console.log(axis_names);
                console.log(axises);

                // create datasets
                var drawing_ds = [];
                chart_datasets.split(",").forEach(function (ds_name, i) {
                    // var backgroundColors = generateBgColors(axises[0].length);
                    var backgroundColors = randomColorGenerator();
                    drawing_ds.push({
                        label: ds_name,
                        data: axises[i + 1],
                        backgroundColor: backgroundColors,
                        borderColor: backgroundColors,
                        borderWidth: 1,
                        PointBackgroundColor: backgroundColors,
                        PointBorderColor: backgroundColors,
                        fill: axises.length <= 2
                    });
                })

                var data_for_chart = {
                    labels: axises[0],
                    datasets: drawing_ds
                };
                drawFunction(data_for_chart, chart_title);
            }
        });
    });

    function generateBgColors(count) {
        var backgroundColor = [];
        for (var i = 0; i < count; i++) {
            backgroundColor.push(randomColorGenerator());
        }
        return backgroundColor
    }

    var randomColorGenerator = function () {
        return '#' + (Math.random().toString(16) + '0000000').slice(2, 8);
    };

    loadParameters();

    var drawFunction = function (data, chart_title) {
        if (myChart !== null) {
            myChart.destroy();
        }
        options = {
            title: {
                display: true,
                text: chart_title
            },
            scaleShowValues: true,
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: false
                    }
                }],
                xAxes: [{
                    ticks: {
                        autoSkip: false
                    }
                }]
            }
        };

        var chart_type = data.datasets.length === 1 ? "bar" : "line";
        myChart = new Chart(ctx, {
            type: chart_type,
            data: data,
            options: options
        });
    };

    new LoadingIndicator();

});