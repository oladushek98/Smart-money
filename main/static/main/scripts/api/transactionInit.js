const btn_add = $('#add');
btn_add[0].setAttribute("disabled", false);

let fade = document.createElement('div');

fade.setAttribute('class', 'sm-fade');

const wrapper = $('.add-transaction_wrapper');
wrapper.append(fade, wrapper.children()[0]);
wrapper.children()[0].remove();
const add_transaction_container = $('.add-transaction');

const step_1 = $('#steps');

const source_select = $('#id_transaction_from');
const destination_select = $('#id_transaction_to');
const currency = $('#id_choice_currency');
const cur_choice_container = $('#choice');
cur_choice_container[0].setAttribute('style', 'display: none;');

getTransactionSourse();
$('#id_amount').val(100);

let s = $('#id_choice_currency');

btn_add.on('click', async (event) => {
    let body;

    body = {
            transaction_from: source_select.val().split('/')[1],
            transaction_to: destination_select.val().split('/')[1],
            amount: $('#id_amount').val(),
            date: datepicker.val(),
            currency: s.val()
        };

    res = await createTransaction(body);
    if (res.ok) {
        addNewTransaction(res.body.id,
            res.body.transaction_from,
            res.body.transaction_to,
            res.body.amount,
            res.body.date);
        if (s.parent()[0].getAttribute('style') !== 'display: none;') {
            if (res.body.currency === source_select.val().split('/')[0]) {
                updateAmount(source_select.val().split('/')[2],
                    res.body.amount, true);
                let object = {};
                object[0] = {'amount': res.body.amount, 'convert_from': res.body.currency, 'convert_to': destination_select.val().split('/')[0]};
                let a = await getConvertedValue(object);
                updateAmount(destination_select.val().split('/')[2],
                    a, false);
            } else {
                updateAmount(destination_select.val().split('/')[2],
                    res.body.amount, false);
                let object = {};
                object[0] = {'amount': res.body.amount, 'convert_from': destination_select.val().split('/')[0], 'convert_to': source_select.val().split('/')[0]};
                let a = await getConvertedValue(object);
                updateAmount(source_select.val().split('/')[2],
                    a, true);
            }
        } else {
            updateAmount(source_select.val().split('/')[2],
                $('#id_amount').val(), true);
            updateAmount(destination_select.val().split('/')[2],
                $('#id_amount').val(), false);
        }
        btn_add[0].setAttribute("disabled", false);
        fade.remove();
        step_1.remove();

        add_transaction_container.append(span, btn_add);

    }

    console.log(res)
});

const date = new Date();
const datepicker = $('.datepicker');
datepicker.datepicker({
    autoClose: true,
    format: 'd.m.yyyy',
    defaultDate: date,
    setDefaultDate: true,
});

fade.remove();
step_1.remove();

const span = $('#add-transaction_placeholder');


add_transaction_container.on('click', (event) => {
    if (add_transaction_container.children()[0] === span[0]) {
        wrapper.append(fade, wrapper.children()[0]);
        span.remove();
        add_transaction_container.append(step_1, btn_add);
        btn_add.removeAttr('disabled');
        source_select.on('click', (event) => {
            getTransactionDestination(event.target.value.split('/')[1]);
            compareCur();
        });
    }
    destination_select.on('click', (event) => {
        compareCur();
    });
});


window.onclick = function (event) {
    if (event.target == fade) {
        $('#add')[0].setAttribute("disabled", false);
        fade.remove();
        step_1.remove();
        add_transaction_container.append(span, btn_add);
        compareCur();
    }
};

$(document).ready(function () {
    add_transaction_container.append(span, btn_add);
    getTransactionDestination('1');
});