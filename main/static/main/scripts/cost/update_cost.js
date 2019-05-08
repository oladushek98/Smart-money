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
        window.location.href = '/'
    }
};