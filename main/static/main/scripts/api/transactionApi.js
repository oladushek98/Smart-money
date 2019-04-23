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
    const response = await fetch('api/transaction/create', {
        method: 'PUT',
        body: JSON.stringify(body),
        headers: header,
        credentials: 'same-origin'
    });
    const json = await response.json();

    return json;
};

let compareCur = () => {
    let cur_1 = source_select.val().split('/')[0];
    let cur_2 = destination_select.val().split('/')[0];
    if (cur_1 !== cur_2) {
        cur_choice_container[0].setAttribute('style', 'display: block;');
        let option = document.createElement('option');
        option.setAttribute('value', cur_1);
        option.textContent = cur_1;
        currency.children().remove();
        currency.append(option);
        option = document.createElement('option');
        option.setAttribute('value', cur_2);
        option.textContent = cur_2;
        currency.append(option);
    } else {
        cur_choice_container[0].setAttribute('style', 'display: none;')

    }
};

let updateAmount = (id, value, opp) => {
    switch(id.split('_')[0]){
        case 'income': return updateIncomeAmount(id, value, opp);
        case 'account': return updateAccountAmount(id, value, opp);
        case 'cost': return updateCostAmount(id, value, opp);
    }
};

let updateIncomeAmount= (id, value, opp) => {
    let s = $('#'+id);
    let old_value = s.parent().children()[2].children[0].textContent;
    let cc;
    if(opp){
        cc = +old_value.split(' ')[1] + +value;
    }else{
        cc = +old_value.split(' ')[1] + +value;
    }
    let new_value = old_value.split(' ')[0] + ' ' +  cc;
    s.parent().children()[2].children[0].textContent = new_value;
};

let updateAccountAmount= (id, value, opp) => {
    let s = $('#'+id);
    let old_value = s.parent().children()[2].children[0].textContent;
    let cc;
    if(opp){
        cc = +old_value.split(' ')[1] - +value;
    }else{
        cc = +old_value.split(' ')[1] + +value;
    }
    let new_value = old_value.split(' ')[0] + ' ' +  cc;
    s.parent().children()[2].children[0].textContent = new_value;
};

let updateCostAmount= (id, value, opp) => {
    let s = $('#'+id);
    let old_value = s.parent().children()[2].children[0].textContent;
    let cc = +old_value.split(' ')[1] + +value;

    let new_value = old_value.split(' ')[0] + ' ' +  cc;
    s.parent().children()[2].children[0].textContent = new_value;
};