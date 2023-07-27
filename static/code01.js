
function input_search() {
    let search = document.getElementById("searchvalue");
    let search_term = search.value;
    setCookie('search_term', search_term, 30, "/");
    save_search_value(search_term);
}

function save_search_value(srch_val) {
    let session = getCookie("id");
    let key_name = "search_term";
    if (srch_val == "") {
        srch_val = "X-RESET-X";
    }
    let url = "/params/set/" + session + "/" + key_name + "/" + srch_val;
    fetch(url)
        .then(response => response.json())
        .then(data => { });
}

function load_search_value() {
    let session = getCookie("id");
    let key_name = "search_term";
    let url = "/params/get/" + session + "/" + key_name;
    fetch(url)
        .then(response => response.json())
        .then(data => {
            let search = document.getElementById("searchvalue");
            if ( data.code == 200 ) {
                search.value = data.result;
            } else {
                search.value = "";
            }
        });
}

function reset_sort_search() {
    setCookie('search_term', '', -1, "/");
}

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

function setCookie(cname, cvalue, exdays, path) {
    let d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    let expires = "expires="+ d.toUTCString();
    // if ( path == undefined ) {
    //     path = "/";
    // }
    let cpath = "path=/";
    document.cookie = cname + "=" + cvalue + ";" + expires + ";" + cpath;
}


// Save value to session storage
function saveToSessionStorage(key, value) {
    const sessionId = getSessionId();
    if (sessionId) {
        sessionStorage.setItem(`${sessionId}-${key}`, value);
    }
}

// Load value from session storage
function loadFromSessionStorage(key) {
    const sessionId = getSessionId();
    if (sessionId) {
        return sessionStorage.getItem(`${sessionId}-${key}`);
    }
    return null;
}

function display_session_id() {
    const cookieid = getCookie("id")
    const id = document.getElementById("session_id_label");
    id.innerText = cookieid;
}

// <link rel="stylesheet" href="{% static 'theme-day.css' %}">"/>


function click_night_day() {
    // determine current setting
    ndset = getCookie('night_mode');
    if ( ndset == "" ) {
        ndset = "off";
    }
    if ( ndset == "on" ) {
        setCookie('night_mode', 'off', 30, "/");
    } else {
        setCookie('night_mode', 'on', 30, "/");
    }
    // reload page
    location.reload();
}

function set_theme() {

    // determine current setting
    let dark_mode = getCookie('night_mode');
    if ( dark_mode == "" ) {
        dark_mode = "off";
    }

    const htmltag = document.getElementById("htmltag");
    if ( dark_mode == "on" ) {
        htmltag.setAttribute("data-bs-theme", "dark");
    } else {
        htmltag.removeAttribute("data-bs-theme");
    }

    // const othertag = document.getElementById("icon-image");
    // if ( dark_mode == "on" ) {
    //     othertag.classList.add("invert");
    // } else {
    //     othertag.classList.remove("invert");
    // }
}

// obtain database name from api, and display the value in footer element.
function load_dbinfo_string() {
    let url = "/misc/dbinfo";
    fetch(url)
        .then(response => response.json())
        .then(data => {
            let element = document.getElementById("dbinfotext");
            if ( data.message == 'success' ) {
                element.innerText = data.data;
            } else {
                element.innerText = "?";
            }
        });
}

// execute load_search_value() when the page is loaded
window.onload = function() {
    load_search_value();
    if ( typeof load_details === 'function' ) {
        load_details();
    }
    display_session_id();
    set_theme();
    //
    load_dbinfo_string();
}

