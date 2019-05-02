let createNewIncomeCategory = (id, name, currency, amount, monthly_plan) => {
    let container = document.createElement('div');
    container.setAttribute('class', 'sm-category sm-category_income');
    let title = document.createElement('div');
    title.setAttribute('class', 'sm-category_title');
    title.textContent = name;
    let icon_wrapper = document.createElement('div');
    icon_wrapper.setAttribute('class', 'sm-category_icon-wrapper');
    icon_wrapper.setAttribute('id', 'finNode_' + id);
    let fill = document.createElement('div');
    let icon = document.createElement('div');
    fill.setAttribute('class', 'sm-category_fill');
    icon.setAttribute('class', 'sm-category_icon sm-category_icon-plant');
    fill.setAttribute('style', 'height: 0%');
    icon_wrapper.appendChild(fill);
    icon_wrapper.appendChild(icon);

    let amount_div = document.createElement('div');
    amount_div.setAttribute('class', 'sm-category_amount');
    let amount_val = document.createElement('div');
    let amount_plan = document.createElement('div');
    amount_val.setAttribute('class', 'sm-category_actual-amount');
    amount_val.textContent = currency + ' ' + amount;
    amount_plan.setAttribute('class', 'sm-category_plan-amount');
    amount_plan.textContent = monthly_plan;

    amount_div.appendChild(amount_val);
    amount_div.appendChild(amount_plan);

    container.appendChild(title);
    container.appendChild(icon_wrapper);
    container.appendChild(amount_div);

    return container
};

let addNewIncome = (id, name, currency, amount, monthly_plan) => {
    let container = createNewIncomeCategory(id, name, currency, amount, monthly_plan);
    const table = $('#income_table');
    const add_item = table.children()[table.children().length - 1];
    table.children()[table.children().length - 1].remove();
    table.append(container);
    table.append(add_item);
    $('#finNode_' + id).on('click', (event) => window.location.href = 'http://localhost:8000/' + 'income/' + id);
    updateIncomeStatistic();
    getTransactionSourse();
};

let updateIncomeStatistic = async () => {
    let income = $('#income_stat-income');
    let plan = $('#income_stat-plan');
    const plans = $('.sm-category_income .sm-category_amount .sm-category_plan-amount');
    const get_incomes = $('.sm-category_income .sm-category_amount .sm-category_actual-amount');

    let objects = {};
    for(let i=0; i < plans.length; i++){
        let currency = get_incomes[i].textContent.split(' ')[0];
        amount = parseInt(plans[i].textContent, 10);
        objects[i] = {'amount': amount, 'convert_from': currency, 'convert_to': 'BYN'};
    }
    let income_count = 0;
    const incomes = $('.sm-category_income .sm-category_amount .sm-category_actual-amount');
    for(i=0; i < incomes.length; i++){
        income_count += parseInt(incomes[i].textContent.split(' ')[1], 10);
    }
    if(isNaN(income_count)){
        income_count = 0;
    }
    let plan_count = await getConvertedValue(objects);
    plan[0].textContent = "Br" + " " + plan_count;
    income[0].textContent = income[0].textContent.split(' ')[0] + ' ' + income_count;

};
