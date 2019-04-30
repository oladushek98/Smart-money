let error = $('#income_name_error');

$('#title').on('input', (event) => error[0].textContent = event.target.value ? '' : '* обязательное поле');

let incomeCreate = async (event) => {
    let body = {
        name: $('#title').val(),
        monthly_plan: $('#plan').val(),
        currency: $('#modal1 #id_currency').val(),
    };

    if (!body.name) {
        error[0].textContent = '* обязательное поле';
        error[0].setAttribute('style', 'color: red;');
        return;
    }


    const csrftoken = $('input[name="csrfmiddlewaretoken"]').attr('value');
    let header = new Headers();
    header.append('X-CSRFToken', csrftoken);

    let response = await fetch('api/income/create',
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
        $('#title').val('');
        $('#plan').val('');
        $('#modal1').modal('close');
        addNewIncome(
            resp_body.id,
            resp_body.name,
            resp_body.currency,
            0,
            resp_body.monthly_plan);
    }
};


$(document).ready(() => {
    $('#add-income').on('click', incomeCreate)
});