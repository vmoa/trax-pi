//
// Javascript for T-Rax
//

var black        = 'black';
var yellow       = 'yellow';
var green        = '#08FF08';
var light_green  = '#C0FFC0';
var red          = '#FF0808';
var light_red    = '#FF8000';

// event:innerHTML { id: 'notice', data: 'msg' }
function set_innerHTML(e) {
    var o = JSON.parse(e.data);
    //console.log("document.getElementById("+o.id+").innerHTML = "+o.data);
    document.getElementById(o.id).innerHTML = o.data;
}

// event:bgcolor: { id: 'indicatorX', data: '#FF0800' }
function set_bgcolor(e) {
    var o = JSON.parse(e.data);
    //console.log("document.getElementById("+o.id+").style.backgroundColor = "+o.data);
    document.getElementById(o.id).style.backgroundColor = o.data;
}

// event:fgcolor { id: 'indicatorX', data: '#FF0800' }
function set_fgcolor(e) {
    var o = JSON.parse(e.data);
    //console.log("document.getElementById("+o.id+").style.color = "+o.data);
    document.getElementById(o.id).style.color = o.data;
}

// event:indicator { id: 'indicator_y', status: 'on|off|open|midway|closed|parked|notparked' }
function update_indicator(e) {
    var o = JSON.parse(e.data);
    //console.log("update_indicator() set "+o.id+" to "+o.status);
    element = document.getElementById(o.id);
    if (o.id == "roof_position" && o.status == 'open') {
        element.style.backgroundColor = green;
        element.style.color = black;
        element.innerHTML = 'OPEN';
    } else if (o.id == "roof_position" && o.status == 'midway') {
        element.style.backgroundColor = yellow;
        element.style.color = black;
        element.innerHTML = 'MIDWAY';
    } else if (o.id == "roof_position" && o.status == 'closed') {
        element.style.backgroundColor = red;
        element.style.color = yellow;
        element.innerHTML = 'CLOSED';

    } else if (o.id == "mount_position" && o.status == 'parked') {
        element.style.backgroundColor = green;
        element.style.color = black;
        element.innerHTML = 'PARKED';
    } else if (o.id == "mount_position" && o.status == 'notparked') {
        element.style.backgroundColor = red;
        element.style.color = yellow;
        element.innerHTML = 'NOT PARKED';
    } else if (o.id == "mount_position" && o.status == 'parked_probably') {
        element.style.backgroundColor = light_green;
        element.style.color = black;
        element.innerHTML = 'PARKED';
    } else if (o.id == "mount_position" && o.status == 'notparked_probably') {
        element.style.backgroundColor = light_red;
        element.style.color = yellow;
        element.innerHTML = 'NOT PARKED';
    } else if (o.id == "mount_position") {
        element.style.backgroundColor = yellow;
        element.style.color = black;
        element.innerHTML = 'UNKNOWN';

    } else if (o.status == 'on') {
        element.style.backgroundColor = green;
        element.style.color = black;
        element.innerHTML = 'ON';
    } else if (o.status == 'off') {
        element.style.backgroundColor = red;
        element.style.color = yellow;
        element.innerHTML = 'OFF';
    } else {
        console.log("update_indicator(): unknown event id:"+o.id+" status:"+o.status);
    }
}

// Connect to SSE source and register event handlers (listeners)
if (typeof(EventSource) !== "undefined") {
        // Create an SSE EventSource and connect to URL
        var eSource = new EventSource("connect");
        // Register message handlers
        eSource.addEventListener("innerHTML", set_innerHTML);
        eSource.addEventListener("bgcolor", set_bgcolor);
        eSource.addEventListener("fgcolor", set_fgcolor);
        eSource.addEventListener("indicator", update_indicator);
}
else {
        document.getElementById("notice").innerHTML="Whoops! Your browser does<br/>not receive server-sent events.";
}

function doSend(url) {
    console.log("doSend(" + url + ")")
    var xhr = new XMLHttpRequest();
    xhr.open("GET", url, true);
    xhr.send(null);
}

