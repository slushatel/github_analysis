$(function () {
    var ctx = document.getElementById("data-chart").getContext("2d");

    function loadParameters() {
        $.ajax({
            url: "/parameters",
        }).done(function (data) {
            data.forEach(function (item) {
                var newElem = $("<div>").attr("id", item.id).text(item.text).data({"reverseUrl": item.reverse_url})
                    .addClass("parameter-link");
                $("#parameters").append(newElem);
            })

            $(".parameter-link").click(function () {
                $.ajax({
                    url: $(this).data("reverseUrl"),
                }).done(function (data) {
                    console.log(data);
                    if (data.value !== undefined) {
                        chart_data = JSON.parse(data.value);
                        axises = [];
                        axis_names = [];
                        backgroundColor = [];
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

                        for (var i = 0; i < axises[0].length; i++) {
                            backgroundColor.push(randomColorGenerator());
                        }
                        data_for_chart = {
                            labels: axises[0],
                            datasets: [{
                                label: '',
                                data: axises[1],
                                backgroundColor: backgroundColor, //'rgba(255, 99, 132, 0.2)',
                                borderColor: backgroundColor, //'rgba(255,99,132,1)',
                                borderWidth: 1
                            }]
                        };
                        drawFunction(data_for_chart);
                    }
                });
            });
        });
    }

    var randomColorGenerator = function () {
        return '#' + (Math.random().toString(16) + '0000000').slice(2, 8);
    };

    loadParameters();

    var drawFunction = function (data) {
        options = {};
        var myBarChart = new Chart(ctx, {
            type: 'bar',
            data: data,
            options: options
        });
    };

    new LoadingIndicator();

});