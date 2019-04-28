let createNewCostCategory = (id, name, currency, monthly_plan) => {
    let container = document.createElement('div');
    container.setAttribute('class', 'sm-category sm-category_expense ');
    let title = document.createElement('div');
    title.setAttribute('class', 'sm-category_title');
    title.textContent = name;
    let icon_wrapper = document.createElement('div');
    icon_wrapper.setAttribute('class', 'sm-category_icon-wrapper');
    icon_wrapper.setAttribute('id', 'cost_' + id);
    let fill = document.createElement('div');
    let icon = document.createElement('div');
    fill.setAttribute('class', 'sm-category_fill');
    icon.setAttribute('class', 'sm-category_icon sm-category_icon-car');
    fill.setAttribute('style', 'height: 100%');
    icon_wrapper.appendChild(fill);
    icon_wrapper.appendChild(icon);

    let amount_div = document.createElement('div');
    amount_div.setAttribute('class', 'sm-category_amount');
    let amount_val = document.createElement('div');
    let amount_plan = document.createElement('div');
    amount_val.setAttribute('class', 'sm-category_actual-amount');
    amount_val.textContent = currency + " " + 0;
    amount_plan.setAttribute('class', 'sm-category_plan-amount');
    amount_plan.textContent = monthly_plan;

    amount_div.appendChild(amount_val);
    amount_div.appendChild(amount_plan);

    container.appendChild(title);
    container.appendChild(icon_wrapper);
    container.appendChild(amount_div);

    return container
};

let addNewCost = (id, name, currency, monthly_plan) => {
    let container = createNewCostCategory(id, name, currency, monthly_plan);
    const table = $('#cost_table');
    const add_item = table.children()[table.children().length - 1];
    table.children()[table.children().length - 1].remove();
    table.append(container);
    table.append(add_item);
    $('#cost_' + id).on('click',
        (event) => window.location.href = 'http://localhost:8000/' + 'cost/' + id);
    updateCostStatistic();
    getTransactionSourse();
};

let updateCostStatistic = async () => {
    let plan = $('#costs_stat');
    let sum_spent = $('#spent_money');

    let plan_count = 0;
    let spent_count = 0;

    const plans = $('.sm-category_expense .sm-category_amount .sm-category_plan-amount');
    const costs = $('.sm-category_expense .sm-category_amount .sm-category_actual-amount');

    let obj1 = {};
    let obj2 = {};

    for(let i = 0; i < plans.length; i++){
        currency = costs[i].textContent.split(' ')[0];

        spent = parseInt(costs[i].textContent.split(' ')[1], 10);
        amount = parseInt(plans[i].textContent, 10);

        obj1[i] = {'amount': amount, 'convert_from': currency, 'convert_to': 'BYN'};
        obj2[i] = {'amount': spent, 'convert_from': currency, 'convert_to': 'BYN'};
    }
    spent_count = await getConvertedValue(obj2);
    plan_count = await getConvertedValue(obj1);
    sum_spent[0].textContent = "Br" + " " + spent_count;
    plan[0].textContent = "Br" + " " + plan_count
};
