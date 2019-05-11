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


google.charts.load('current', {'packages': ['corechart']});
google.charts.setOnLoadCallback(drawChart2);


function drawChart2() {
    // Define the chart to be drawn.
    let data = new google.visualization.DataTable();
    data.addColumn('string');
    data.addColumn('number');
    data.addRows(parse_data(data_from));
    let options = {
        title: 'Получено из',
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