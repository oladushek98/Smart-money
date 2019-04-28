let createNewAccountCategory = (id, name, currency, amount) => {

    let container = document.createElement('div');
    container.setAttribute('class', 'sm-category sm-category_account');
    let title = document.createElement('div');
    title.setAttribute('class', 'sm-category_title');
    title.textContent = name;
    let icon_wrapper = document.createElement('div');
    icon_wrapper.setAttribute('class', 'sm-category_icon-wrapper');
    icon_wrapper.setAttribute('id', 'account_' + id);
    let fill = document.createElement('div');
    let icon = document.createElement('div');
    fill.setAttribute('class', 'sm-category_fill');
    icon.setAttribute('class', 'sm-category_icon sm-category_icon-cash');
    icon_wrapper.appendChild(fill);
    icon_wrapper.appendChild(icon);

    let amount_div = document.createElement('div');
    amount_div.setAttribute('class', 'sm-category_amount');
    let amount_val = document.createElement('div');
    let amount_plan = document.createElement('div');
    amount_val.setAttribute('class', 'sm-category_actual-amount');
    amount_val.textContent = amount + " " + currency;

    amount_div.appendChild(amount_val);
    amount_div.appendChild(amount_plan);

    container.appendChild(title);
    container.appendChild(icon_wrapper);
    container.appendChild(amount_div);


    return container
};

let addNewAccount = (id, name, currency, amount, taka_into_balance) => {
    let container = createNewAccountCategory(id, name, currency, amount);
    if (taka_into_balance == '0') {
        container.setAttribute('class', 'sm-category sm-category_account excluded');
    }
    const table = $('#account_table');
    const add_item = table.children()[table.children().length - 1];
    table.children()[table.children().length - 1].remove();
    table.append(container);
    table.append(add_item);
    $('#account_' + id).on('click',
        (event) => window.location.href = 'http://localhost:8000/' + 'account/' + id);
    updateAccountStatistic();
    getTransactionSourse();
};

let updateAccountStatistic = async () => {
    let plan = $('#accounts_stat');
    let plan_count = 0;
    const accounts = $('.sm-category_account:not(.excluded) .sm-category_amount .sm-category_actual-amount');
    for(let i = 0; i < accounts.length; i++){
        let currency = accounts[i].textContent.split(' ')[0];
        amount = parseInt(accounts[i].textContent.split(' ')[1], 10);

        amount = await getConvertedValue(amount, currency);

        plan_count += amount;
    }
    plan[0].textContent = "Br" + " " + plan_count;
};

async function getConvertedValue (amount, currency) {
    const body = {
        'amount': amount,
        'convert_from': currency,
        'convert_to': "BYN"
        };

    const csrftoken = $('input[name="csrfmiddlewaretoken"]').attr('value');
        let header = new Headers();
        header.append('X-CSRFToken', csrftoken);

        let response = await fetch( 'api/convert',
            {
                method: 'PUT',
                body: JSON.stringify(body),
                headers: header,
                credentials: 'same-origin'
            }
        );

        const resp_body = await response.json();
        return resp_body.result
}