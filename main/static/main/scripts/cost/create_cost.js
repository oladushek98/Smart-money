async function costCreate(event){
    let body = {
        name: $('#title2').val(),
        monthly_plan: $('#cost_plan').val(),
        currency: $('#modal3 #id_currency').val(),
    };

    const csrftoken = $('input[name="csrfmiddlewaretoken"]').attr('value');
    let header = new Headers();
    header.append('X-CSRFToken', csrftoken);

    let response = await fetch('api/cost/create',
        {
            method: 'PUT',
            body: JSON.stringify(body),
            headers: header,
            credentials: 'same-origin'
        }
)
    ;
    if (response.ok) {
        const resp_body = await response.json();

        $('#modal3').modal('close');
        $('#title2').val('');
        $('#cost_plan').val('');
        addNewCost(
            resp_body.id,
            resp_body.name,
            resp_body.currency,
            resp_body.monthly_plan
        );
    }
}


$(document).ready(function(){
    $('#add-cost').on('click', costCreate)
});