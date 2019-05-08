let parse_data = (row_data) => {
    row_data = row_data.replace(/&quot;/g, '"');
    row_data = JSON.parse(row_data);
    try {
        row_data[1][0] = row_data[1][0].replace(/&#39;/g, '"');
    } catch (err) {
    }
    return row_data
};

google.charts.load('current', {'packages': ['corechart']});
google.charts.setOnLoadCallback(drawChart);
google.charts.setOnLoadCallback(drawChart1);
google.charts.setOnLoadCallback(drawChart2);

function drawChart() {
    let data = new google.visualization.arrayToDataTable(parse_data(data_about));

    let options = {
        curveType: 'point',
        legend: {position: 'bottom'},

        title: 'Влияние транзакции на состояние счета',
        height: 355,
        pieStartAngle: 100,
        colors: ['red', 'rgb(255, 162, 47)'],
        fontSize: 14,
        width: '100%',
        fontName: 'Roboto',
    };

    let chart = new google.visualization.LineChart(document.getElementById('curve_chart'));
    chart.draw(data, options);
}

function drawChart1() {
    // Define the chart to be drawn.
    let data = new google.visualization.DataTable();
    data.addColumn('string');
    data.addColumn('number');
    data.addRows(parse_data(data_to));
    let options = {
        title: 'Доходы',
        legend: 'top',
        pieHole: 0.4,
        height: 500,
        width: 555,
        fontSize: 14,
        fontName: 'Roboto',
    };

    // Instantiate and draw the chart.
    let chart = new google.visualization.PieChart(document.getElementById('to_chart'));
    chart.draw(data, options);
}

function drawChart2() {
    // Define the chart to be drawn.
    let data = new google.visualization.DataTable();
    data.addColumn('string');
    data.addColumn('number');
    data.addRows(parse_data(data_from));
    let options = {
        title: 'Расходы',
        legend: 'top',
        pieHole: 0.4,
        height: 500,
        width: 555,
        fontSize: 14,
        fontName: 'Roboto',
    };

    // Instantiate and draw the chart.
    let chart = new google.visualization.PieChart(document.getElementById('from_chart'));
    chart.draw(data, options);
}

let deleteNode = async (id) => {
    const body = {
        'id': id
    };

    const csrftoken = $('input[name="csrfmiddlewaretoken"]').attr('value');
    let header = new Headers();
    header.append('X-CSRFToken', csrftoken);

    let response = await fetch(delete_url,
        {
            method: 'PUT',
            body: JSON.stringify(body),
            headers: header,
            credentials: 'same-origin'
        }
)
    ;

    if (response.ok) {
        goToPage('/')
    }
};