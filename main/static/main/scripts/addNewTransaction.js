let createNewTransactionCategory = (id, source, destination, amount, date) => {
    let container = document.createElement('div');
    container.setAttribute('class', 'transaction z-depth-1');
    container.setAttribute('id', 'transaction_' + id);

    let title = document.createElement('div');
    title.setAttribute('class', 'transaction-from');
    title.textContent = source;

    let icon_wrapper = document.createElement('div');
    icon_wrapper.setAttribute('class', 'transaction-icon-way_wrapper');

    let fill = document.createElement('div');
    let icon = document.createElement('div');

    fill.setAttribute('class', 'transaction-amount');
    icon.setAttribute('class', 'transaction-icon-way');
    fill.textContent = amount;

    icon_wrapper.appendChild(fill);
    icon_wrapper.appendChild(icon);

    let amount_div = document.createElement('div');
    amount_div.setAttribute('class', 'transaction-to');
    amount_div.textContent = destination;


    let date_div = document.createElement('div');
    date_div.setAttribute('class', 'transaction-date');
    date_div.textContent = date;

    container.appendChild(title);
    container.appendChild(icon_wrapper);
    container.appendChild(amount_div);
    container.appendChild(date_div);

    return container
};

let addNewTransaction = (id, source, destination, amount, date) => {
    let container = createNewTransactionCategory(id, source, destination, amount, date);
    const table = $('.sm-transaction-block');
    table.append(container);
    $('#transaction_' + id).on('click', (event) => window.location.href = 'http://localhost:8000/' + 'transaction/' + id );
};

let setNewAmount = (s, opp, amount ) => {
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

let recalculateAmounts = (transaction, cur_from, cur_to) => {
    let element_from = $('#finNode_' + transaction.transaction_from);
    let element_to = $('#finNode_' + transaction.transaction_to);
    if(transaction.currency === cur_from){
        setNewAmount(element_from, true, transaction.amount);
    }else{
        let amount = getConvertedValue(transaction.amount, cur_from, cur_to);
        setNewAmount(element_to, false, amount);
    }
};