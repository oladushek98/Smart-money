const csrftoken = $('input[name="csrfmiddlewaretoken"]').attr('value');
let header = new Headers();
header.append('X-CSRFToken', csrftoken);


let getTransactionSourse = async () => {
    fetch('api/transaction/getsourse', {
        method: "GET",
        headers: header,
        credentials: 'same-origin'
    }).then(r => r.json().then(data => ({
        status: r.status, body: data.body
    }))).then(obj => {
        let option = null;
        source_select.children().remove();
        for (i = 0; i < obj.body.length; i++) {
            option = document.createElement('option');
            option.setAttribute('value', obj.body[i].id);
            option.textContent = obj.body[i].name;
            source_select.append(option);
        }
    });
};

let getTransactionDestination = (id) => {
    fetch('api/transaction/getdest/' + id, {
        method: "GET",
        headers: header,
        credentials: 'same-origin'
    }).then(r => r.json().then(data => ({
        status: r.status, body: data.body
    }))).then(obj => {
        let option = null;
        destination_select.children().remove();
        for (i = 0; i < obj.body.length; i++) {
            option = document.createElement('option');
            option.setAttribute('value', obj.body[i].id);
            option.textContent = obj.body[i].name;
            destination_select.append(option);
        }
    });
};


let createTransaction = async (body) => {
    const response = await fetch('api/transaction/create',{
        method: 'PUT',
        body: JSON.stringify(body),
        headers: header,
        credentials: 'same-origin'
    });
    const json = await response.json();

    return {ok: response.ok, body: json};
};