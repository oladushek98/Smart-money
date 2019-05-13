$(document).ready(function () {
    $('.modal').modal();
});

async function deleteNode(id, flag){
    const body = {
        'id': id,
        'flag': flag,
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
}