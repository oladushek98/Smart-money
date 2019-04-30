let accountCreate = async (event) => {
    let body = {
        name: $('#title1').val(),
        amount: $('#amount').val(),
        currency: $('#modal2 #id_currency').val(),
        take_into_balance: String($('#id_take_into_balance')[0].checked)
    };

    const csrftoken = $('input[name="csrfmiddlewaretoken"]').attr('value');
    let header = new Headers();
    header.append('X-CSRFToken', csrftoken);

    let response = await fetch('api/account/create',
        {
            method: 'PUT',
            body: JSON.stringify(body),
            headers: header,
            credentials: 'same-origin'
        }
)
    ;
    if (response.ok) {
        if (body.amount == '') {
            body.amount = 0;
        }
        const resp_body = await response.json();
        $('#title1').val('');
        $('#amount').val('');
        $('#modal2').modal('close');
        addNewAccount(
            resp_body.id,
            resp_body.name,
            resp_body.amount,
            resp_body.currency,
            resp_body.take_into_balance
        );
    }
};

$(document).ready(() => {
    $('#add-account').on('click', accountCreate)
});