//
// Javascript for T-Rax
//

var black        = 'black';
var yellow       = 'yellow';
var green        = '#08FF08';
var light_green  = '#C0FFC0';
var red          = '#FF0808';
var light_red    = '#FF8000';

var override_mode = 0;  // Used to determine which modal to display
var override_background_color = 'orange';
var original_background_color = '';   // Will be set first time we override

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
    } else if (o.id == "roof_position" && o.status == 'confused') {
        element.style.backgroundColor = light_red;
        element.style.color = yellow;
        element.innerHTML = 'CONFUSED';

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

// event:override { mode: 'on|off' }
function set_override_mode(e) {
    var o = JSON.parse(e.data);
    console.log("set_override_mode " + o.mode)
    if (o.mode == "on") {
        // Stash our original background color in a global (exactly once) so we can restore
        if (original_background_color.length == 0) {
            original_background_color = window.getComputedStyle(document.getElementById("container")).backgroundColor;
        }
        document.getElementById("container").style.backgroundColor = override_background_color;
        override_mode = 1
    } else if (o.mode == "off") {
        document.getElementById("container").style.backgroundColor = original_background_color;
        override_mode = 0
    }
}

function doSend(url) {
    console.log("doSend(" + url + ")");
    var xhr = new XMLHttpRequest();
    xhr.open("GET", url, true);
    xhr.send(null);
}

//
// Handle our emergency override modal
//

// Expose password modal when ticker clicked
var first_time_through = 1;
function doOverride() {

    // Initialize our modal actions (exactly once)
    if (first_time_through) {
        var passwordModal = document.getElementById("passwordModal");
        var exitModal = document.getElementById("exitModal");
        first_time_through = 0;

        // Watch password for <ENTER> --> submit, <ESC> --> cancel
        document.getElementById("password").addEventListener("keyup", function(event) {
            if (event.keyCode === 13) {  // <ENTER> keycode
                document.getElementById("pwsubmit").click();
            } else if (event.keyCode === 27) {  // <ESC> keycode
                passwordModal.style.display = "none";
            }
        });

        // Register the numerous modal close actions
        Array.from(document.getElementsByClassName("close")).forEach(closer => 
            closer.onclick = function() {  // each of the close "X"s
                passwordModal.style.display = "none";
                exitModal.style.display = "none";
            }
        );
        document.getElementById("nope").onclick = function() {  // exitOverride "Nope" button
            exitModal.style.display = "none";
        }
        window.onclick = function(event) {  // anywhere outside the modal
            if (event.target == passwordModal || event.target == exitModal) {
                event.target.style.display = "none";
            }
        }
    }

    // Expose appropriate modal based on current mode
    if (override_mode) {
        document.getElementById("exitModal").style.display = "block";
    } else {
        document.getElementById("password").value = "";  // Clear last password first
        document.getElementById("passwordModal").style.display = "block";
        document.getElementById("password").focus();
    }

    // Expose the modal
    //modal.style.display = "block";

}

// Action when user clicks password "submit"
function overrideOn() {
    if (document.getElementById("password").value.length > 0) {
        doSend("/override?on&password=" + document.getElementById("password").value);
    }
    document.getElementById("passwordModal").style.display = "none";
}

// Action when user cliks "yep" to exit override mode
function overrideOff() {
    doSend("/override?off");
    document.getElementById("exitModal").style.display = "none";
}


//
// Connect to SSE source and register event handlers (listeners)
//
if (typeof(EventSource) !== "undefined") {
        // Create an SSE EventSource and connect to URL
        var eSource = new EventSource("connect");
        // Register message handlers
        eSource.addEventListener("innerHTML", set_innerHTML);
        eSource.addEventListener("bgcolor", set_bgcolor);
        eSource.addEventListener("fgcolor", set_fgcolor);
        eSource.addEventListener("indicator", update_indicator);
        eSource.addEventListener("override", set_override_mode);
}
else {
        document.getElementById("notice").innerHTML="Whoops! Your browser does<br/>not receive server-sent events.";
}
