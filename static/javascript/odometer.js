var cur_el = document.getElementById('cur');
var tot_el = document.getElementById('tot');
var tot = parseFloat(tot_el.innerHTML);
var donations = [];

function loaddonations () {
    donations = JSON.parse(this.responseText);
}

var req = new XMLHttpRequest();
req.addEventListener("load", loaddonations);
req.overrideMimeType("text/json");
req.open("GET", "/static/data/donations.json", false);
req.send();

var gross = 0, fees = 0, html = "";
for (var i = 0; i < donations.length; ++ i) {
    gross += parseFloat(donations[i].gross);
    fees += parseFloat(donations[i].fee);
    html += '<li class="doner"><span class="message">' + donations[i].message + '</span>: <span class="donation">' + donations[i].gross + '</span></li>'
}
cur = gross - fees;

document.getElementById('donationList').innerHTML = html;

var amt_left = cur >= tot ? 0 : (tot - cur);

cur_el.innerHTML = tot;

var delay = 0;
var ival = setInterval(roll_body, delay);
var iter = tot;

function roll_body () {
    if (iter <= amt_left) {
        clearInterval(ival);
        return;
    }

    clearInterval(ival);
    delay += 4;
    ival = setInterval(roll_body, delay);
    iter -= 1;
    cur_el.innerHTML = iter;
}

