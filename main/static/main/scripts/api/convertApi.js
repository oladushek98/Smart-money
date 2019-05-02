async function getConvertedValue (objects) {
    const csrftoken = $('input[name="csrfmiddlewaretoken"]').attr('value');
    let header = new Headers();
    header.append('X-CSRFToken', csrftoken);
    let response = await fetch( 'api/convert',
        {
            method: 'PUT',
            body: JSON.stringify(objects),
            headers: header,
            credentials: 'same-origin'
        }
    );
    const resp_body = await response.json();
    return resp_body.result
}