(function(w, d, $){

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

    function getMeasurements(timeframe, period){

        settings.url = "http://eazymac25.pythonanywhere.com/rest/api/1/measureHistory?timeframe=" + timeframe + 
        "&period=" + period +  "&startAt=0&maxResults=1000";

        $.ajax(settings).done(function (response){
            createChart(response);
        });
    }

    function createChart(data){

        console.log('hello');
        console.log(data.measureHistory.max_results);

        var humidity = data.measureHistory.records.map(obj => obj.humidity);
        var temperature = data.measureHistory.records.map(obj => obj.temperature);
        var dates = data.measureHistory.records.map(obj => obj.createTime);

        var ctx = $("#myChart");
        var myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: dates,
                datasets: [{
                    label: 'Humidity',
                    data: humidity,
                    borderColor: "#3e95cd",
                    fill: false
                },
                {
                    label: 'Temperature',
                    data: temperature,
                    borderColor: "#c45850",
                    fill: false
                }]
            },
            options: {
                title: {
                    text: "Humidity Over Time",
                    display: true
                },
                // scales: {
                //     yAxes: [{
                //         ticks: {
                //             beginAtZero: true
                //         }
                //     }]
                // }
            }
        });
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

            console.log(this.textContent);

            getMeasurements(timeframe, period);
        });
    });

    // load default
    getMeasurements("30", "M");

})(window, document, $);
