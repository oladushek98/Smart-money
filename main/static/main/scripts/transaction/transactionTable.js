let date_from = $('#date_from');
let date_to = $('#date_to');
let s = $('#update');
const start = parseInt('{{ request|get_date_start }}');
const cur_count = parseInt('{{ request|get_date_count }}');

let jump = (start, end, val) => {
    if (cur_count != val) {
        let href = '{% url '
        transactions
        ' %}?from=' + date_from.val() + '&to=' + date_to.val() + '&start=' + start + '&end=' + end;
        goToPage(href)
    }
};

if (start === 0) {
    $('#prev')[0].setAttribute('disabled', 'false')
}
if (parseInt('{{ amount }}') === parseInt('{{ request|get_date_tail:count }}')) {
    $('#next')[0].setAttribute('disabled', 'false')
}

$('#prev').on('click', (event) => {
    jump(start - cur_count, start, 0)
});

$('#next').on('click', (event) => {
    jump(start + cur_count, start + cur_count + cur_count, 0)
});

$('#click5').on('click', (event) => {
    jump(start, start + 5, 5)
});
$('#click10').on('click', (event) => {
    jump(start, start + 10, 10)
});

date_from[0].oninput = (val) => {
    let spl = s[0].getAttribute('href').split('&');
    let f = spl[0].split('=');
    f[1] = val.target.value;
    spl[0] = f.join('=');
    s[0].setAttribute('href', spl.join('&'));
};
date_to[0].oninput = (val) => {
    let spl = s[0].getAttribute('href').split('&');
    let f = spl[1].split('=');
    f[1] = val.target.value;
    spl[1] = f.join('=');
    s[0].setAttribute('href', spl.join('&'));
};

let handlerIn = () => {
    $('#choice').addClass('hidden');
    $('#make-choice').removeClass('hidden');
};

let handlerOut = () => {
    $('#make-choice').addClass('hidden');
    $('#choice').removeClass('hidden');
};

$('#choice').mouseenter(handlerIn).mouseleave();
$('#make-choice').mouseenter().mouseleave(handlerOut);