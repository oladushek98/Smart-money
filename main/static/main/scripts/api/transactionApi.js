const csrftoken = $('input[name="csrfmiddlewaretoken"]').attr('value');
let header = new Headers();
header.append('X-CSRFToken', csrftoken);


async function getTransactionSourse() {
    try {
        let res = await fetch('api/transaction/getsourse', {
            method: "GET",
            headers: header,
            credentials: 'same-origin'
        });
        let res2 = await res.json();
        let obj = {status: res.status, body: res2.body};

        let flag = false;
        if (obj.body.length == 0) {
            btn_add[0].setAttribute("disabled", false);
            source_select[0].setAttribute("disabled", false);
            obj.body = [{id: -1, name: 'нет источника'}];
            flag = true;
        }
        let option = null;
        source_select.children().remove();
        for (i = 0; i < obj.body.length; i++) {
            option = document.createElement('option');
            option.setAttribute('value', obj.body[i].id);
            option.textContent = obj.body[i].name;
            source_select.append(option);
        }
        if (flag) {
            return false;
        }

        source_select[0].removeAttribute('disabled');
        btn_add[0].removeAttribute('disabled');
        return true;
    } catch (e) {
        console.log(e);
    }
};

async function getTransactionDestination(id) {
    if (id === undefined) {
        return false;
    }
    try {
        let r = await fetch('api/transaction/getdest/' + id, {
            method: "GET",
            headers: header,
            credentials: 'same-origin'
        });
        let data = await r.json();
        let obj = {status: r.status, body: data.body};

        let flag = false;
        if (obj.body.length == 0) {
            btn_add[0].setAttribute("disabled", false);
            destination_select[0].setAttribute("disabled", false);
            obj.body = [{id: -1, name: 'нет пункта назначения'}]
            flag = true;
        }
        let option = null;
        destination_select.children().remove();
        for (i = 0; i < obj.body.length; i++) {
            option = document.createElement('option');
            option.setAttribute('value', obj.body[i].id);
            option.textContent = obj.body[i].name;
            destination_select.append(option);
        }
        if (flag) {
            return false;
        }

        destination_select[0].removeAttribute('disabled');
        btn_add[0].removeAttribute('disabled');
        return true;
    } catch (e) {
        console.log(e);
    }
}


async function createTransaction(body) {
    const response = await fetch('api/transaction/create', {
        method: 'PUT',
        body: JSON.stringify(body),
        headers: header,
        credentials: 'same-origin'
    });
    const json = await response.json();
    return json;
}

function compareCur() {
    try {
        let cur_1 = source_select.val().split('/')[0];
        let cur_2 = destination_select.val().split('/')[0];
        if (cur_1 !== cur_2) {
            console.log(cur_1, ' -> ', cur_2);
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
            console.log(cur_1, ' -> ', cur_2);
            cur_choice_container[0].setAttribute('style', 'display: none;')

        }
    } catch (e) {
        console.log(e);
    }
};

function updateAmount(id, value, opp) {
    switch (id.split('_')[0]) {
        case 'income':
            return updateIncomeAmount(id.split('_')[1], value, opp);
        case 'account':
            return updateAccountAmount(id.split('_')[1], value, opp);
        case 'cost':
            return updateCostAmount(id.split('_')[1], value, opp);
    }
}

function updateIncomeAmount(id, value, opp) {
    let s = $('#finNode_' + id);
    let old_value = s.parent().children()[2].children[0].textContent;
    let cc;
    if (opp) {
        cc = +old_value.split(' ')[1] + +value;
    } else {
        cc = +old_value.split(' ')[1] + +value;
    }
    let new_value = old_value.split(' ')[0] + ' ' + cc;
    s.parent().children()[2].children[0].textContent = new_value;
}

function updateAccountAmount(id, value, opp) {
    let s = $('#finNode_' + id);
    let old_value = s.parent().children()[2].children[0].textContent;
    let cc;
    if (opp) {
        cc = +old_value.split(' ')[1] - +value;
    } else {
        cc = +old_value.split(' ')[1] + +value;
    }
    let new_value = old_value.split(' ')[0] + ' ' + cc;
    s.parent().children()[2].children[0].textContent = new_value;
}

function updateCostAmount(id, value, opp) {
    let s = $('#finNode_' + id);
    let old_value = s.parent().children()[2].children[0].textContent;
    let cc = +old_value.split(' ')[1] + +value;

    let new_value = old_value.split(' ')[0] + ' ' + cc;
    s.parent().children()[2].children[0].textContent = new_value;
}

async function deleteTransaction(id) {
    const response = await fetch('api/transaction/delete', {
        method: 'PUT',
        body: JSON.stringify({id: id}),
        headers: header,
        credentials: 'same-origin'
    });
    const json = await response.json();

    return json;
}