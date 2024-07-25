function gwcalc_load_values() {

    function getCookie(cname) {
        let doc_cookie = document.cookie;
        let name = cname + "=";
        let decodedCookie = decodeURIComponent(doc_cookie);
        let ca = decodedCookie.split(';');
        for(let i = 0; i <ca.length; i++) {
            let c = ca[i];
            while (c.charAt(0) == ' ') {
                c = c.substring(1);
            }
            if (c.indexOf(name) == 0) {
                return c.substring(name.length, c.length);
            }
        }
        return "";
    }

    function load_value(name) {
        let id = document.getElementById(name);
        id.value = getCookie(name);
    }

    load_value('gc_from_date');
    load_value('gc_to_date');
    load_value('gc_calc_date');
    load_value('gc_tc_code');
    load_value('gc_code_code');
    load_value('gc_cc_exclude');
}

document.addEventListener('DOMContentLoaded', function() {
    const divIds = ['code1', 'code2', 'code3'];

    divIds.forEach(divId => {
        const div = document.getElementById(divId);
        const input = div.querySelector('input');
        const small = div.querySelector('small');

        if (input && small) {
            small.classList.add('hidden');

            input.addEventListener('focus', () => {
                small.classList.remove('hidden');
            });

            input.addEventListener('blur', () => {
                small.classList.add('hidden');
            });
        }
    });
});


gwcalc_load_values();

