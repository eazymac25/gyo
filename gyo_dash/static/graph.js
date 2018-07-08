(function(w, d, $){

    var hChart = null;
    var tChart = null;

    var data = null;
    var settings = {
      "async": true,
      "crossDomain": true,
      "url": null,
      "method": "GET",
      "headers": {
        "content-type": "application/json",
        "cache-control": "no-cache",
      },
      "processData": false,
    }

    function getMoistureLevel(){
        settings.url = "http://eazymac25.pythonanywhere.com/rest/api/1/moisture";

        $.ajax(settings).done(function (response){
            $('#moistureLevel').text(response.record.moistureLevel);
        });
    }

    function getMeasurements(timeframe, period){

        settings.url = "http://eazymac25.pythonanywhere.com/rest/api/1/measureHistory?timeframe=" + timeframe +
        "&period=" + period +  "&startAt=0&maxResults=1000";

        $.ajax(settings).done(function (response){
            createChart(response);
        });
    }

    function createChart(data){
        
        console.log(data.measureHistory.max_results);

        var humidity = data.measureHistory.records.map(obj => obj.humidity);
        var temperature = data.measureHistory.records.map(obj => obj.temperature);
        var dates = data.measureHistory.records.map(obj => obj.createTime);

        if (hChart == null) {
            var hctx = $("#humidityChart");
            var tctx = $("#temperatureChart");
            hChart = new Chart(hctx, {
                type: 'line',
                data: {
                    labels: dates,
                    datasets: [{
                        label: 'Humidity',
                        data: humidity,
                        yAxisID: 'H',
                        borderColor: "#3e95cd",
                        fill: false
                    }]
                },
                options: {
                    title: {
                        text: "Humidity Over Time",
                        fontSize: 24,
                        display: true
                    },
                    scales: {
                        yAxes: [{
                            id: 'H',
                            type: 'linear',
                            position: 'left',
                            scaleLabel: {
                                display: true,
                                labelString: 'Relative Humidity (%)',
                                fontSize: 16
                            }
                        }]
                    }
                }
            });

            tChart = new Chart(tctx, {
                type: 'line',
                data: {
                    labels: dates,
                    datasets: [{
                        label: 'Temperature',
                        data: temperature,
                        yAxisID: 'T',
                        borderColor: "#c45850",
                        fill: false
                    }]
                },
                options: {
                    title: {
                        text: "Temperature Over Time",
                        fontSize: 24,
                        display: true
                    },
                    scales: {
                        yAxes: [{
                            id: 'T',
                            type: 'linear',
                            position: 'left',
                            scaleLabel: {
                                display: true,
                                labelString: 'Temperature (C)',
                                fontSize: 16
                            },
                            ticks: {
                                min: 18,
                                max: 30
                            }
                        }]
                    }
                }
            });

        } else {
            hChart.data.labels = dates;
            hChart.data.datasets[0].data = humidity;

            tChart.data.labels = dates;
            tChart.data.datasets[0].data = temperature;

            hChart.update(0);
            tChart.update(0);
        }
    }

    function textToPeriod(text){
        if (text.toLowerCase().includes("min")){
            return "M";
        }
        if (text.toLowerCase().includes("hr")){
            return "H";
        }
        if (text.toLowerCase().includes("day")){
            return "D";
        }
        if (text.toLowerCase().includes("week")){
            return "W";
        }
        return null;
    }

    $(d).ready(function(){
        $('button').on('click', function() {

            var temp = this.textContent.split(" ");
            var timeframe = temp[0];
            var period = textToPeriod(temp[1]);

            getMeasurements(timeframe, period);
        });

        getMoistureLevel();
        // load default
        getMeasurements("30", "M");
    });

})(window, document, $);
