let createNewAccountCategory = (name, currency, amount) => {
    let container = document.createElement('div');
    container.setAttribute('class', 'sm-category sm-category_account');
    let title = document.createElement('div');
    title.setAttribute('class', 'sm-category_title');
    title.textContent = name;
    let icon_wrapper = document.createElement('div');
    icon_wrapper.setAttribute('class', 'sm-category_icon-wrapper');
    let fill = document.createElement('div');
    let icon = document.createElement('div');
    fill.setAttribute('class', 'sm-category_fill');
    icon.setAttribute('class', 'sm-category_icon sm-category_icon-cash');
    icon_wrapper.appendChild(fill);
    icon_wrapper.appendChild(icon);

    let amount_div = document.createElement('div');
    amount_div.setAttribute('class', 'sm-category_amount');
    let amount_val = document.createElement('div');
    amount_val.setAttribute('class', 'sm-category_actual-amount');
    amount_val.textContent = currency + ' ' + amount;

    amount_div.appendChild(amount_val);
    container.appendChild(title);
    container.appendChild(icon_wrapper);
    container.appendChild(amount_div);

    return container
};

let addNewAccount = (name, currency, amount) => {
    let container = createNewAccountCategory(name, currency, amount);
    const table = $('#account_table');
    const add_item = table.children()[table.children().length - 1];
    table.children()[table.children().length - 1].remove();
    table.append(container);
    table.append(add_item)
};