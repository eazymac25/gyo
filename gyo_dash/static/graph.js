$(window).on('load', function() {
    var data = null;
    var settings = {
      "async": true,
      "crossDomain": true,
      "url": "http://eazymac25.pythonanywhere.com/rest/api/1/measureHistory?timeframe=30&period=M&startAt=0&maxResults=100",
      "method": "GET",
      "headers": {
        "content-type": "application/json",
        "cache-control": "no-cache",
      },
      "processData": false,
    }

    $.ajax(settings).done(function (response) {
      data = response;
    });
    console.log(data.maxResults);
    var humidity = data.measureHistory.records.map(obj => obj.humidity);
    var dates = data.measureHistory.records.map(obj => obj.createTime);

    var ctx = $("#myChart");
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [{
                label: 'Humidity',
                data: humidity,
            }]
        },
        options: {}
    });
});