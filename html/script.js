var websocket = new WebSocket("ws://127.0.0.1:6789/");
// websocket send
var seats = document.getElementsByClassName('seat'),
    game_round = document.getElementById('game_round'),
    action_round = document.getElementById('action_round'),
    start_seat = document.getElementById('start_seat'),
    active_seat = document.getElementById('active_seat'),
    seat_order = document.getElementById('seat_order'),
    pass_order = document.getElementById('pass_order'),
    status1 = document.getElementsByClassName('status1'),
    status2 = document.getElementsByClassName('status2'),
    seats = document.getElementsByClassName('seat'),
    sp_fr = document.getElementsByClassName('sp_fr'),
    sp_cr = document.getElementsByClassName('sp_cr'),
    gr_fto = document.getElementsByClassName('gr_fto'),
    gr_ec = document.getElementsByClassName('gr_ec'),
    gr_ec_nr = document.getElementById('gr_ec_nr'),
    gr_cto = document.getElementsByClassName('gr_cto'),
    users = document.getElementById('users');
function ws_send(action) {
    return function (event) { websocket.send(JSON.stringify({action: action, value1: '', value2: ''})); }
}
function ws_send_value(obj) {
    return function (event) { websocket.send(JSON.stringify({action: obj.name, value1: obj.value, value2: ''})); }
}
function ws_send_index(obj, index) {
    return function (event) { websocket.send(JSON.stringify({action: obj.name, value1: index, value2: ''})); }
}
function set_on_click(objects, function_to_add) {
    for (o of objects) {
        o.onclick = function_to_add
    }
}
function set_send_value_on_click(objects, function_to_add) {
    for (o of objects) {
        o.onclick = ws_send_value(o)
    }
}
function set_send_index_on_click(objects, function_to_add) {
    var i;
    for (i = 0; i < objects.length; i++) {
        objects[i].onclick = ws_send_index(objects[i], i)
    }
}
set_on_click(document.getElementsByClassName('play'), ws_send('play'))
set_on_click(document.getElementsByClassName('pause'), ws_send('pause'))
set_on_click(document.getElementsByClassName('stop'), ws_send('stop'))
set_on_click(document.getElementsByClassName('shutdown'), ws_send('shutdown'))
set_send_value_on_click(seats)
set_send_index_on_click(sp_fr)
set_send_index_on_click(sp_cr)
set_send_index_on_click(gr_fto)
set_send_index_on_click(gr_ec)
gr_ec_nr.onchange = ws_send_value(gr_ec_nr)
set_send_index_on_click(gr_cto)
// websocket receive
var class_status1_checked = "w3-black",
    class_status2_checked = "w3-indigo",
    class_state_checked = "w3-indigo";
function select(items, selected) {
    var i;
    for (i = 0; i < items.length; i++) {
        if (selected[i]) {
            items[i].classList.add(class_state_checked);
        } else {
            items[i].classList.remove(class_state_checked);
        }
    }
}
function select_item(items, index, class_name) {
    for (item of items) {
        item.classList.remove(class_name);
    }
    items[Math.min(index, items.length-1)].classList.add(class_name);
}
function select_state_item(items, index) {
    select_item(items, index, class_state_checked);
}
websocket.onmessage = function (event) {
    data = JSON.parse(event.data);
    switch (data.type) {
        case 'state':
            select_item(status1, data.status, class_status1_checked)
            select_item(status2, data.status, class_status2_checked)
            game_round.textContent = data.game_round
            action_round.textContent = data.action_round
            start_seat.textContent = data.start_seat
            active_seat.textContent = data.active_seat
            seat_order.textContent = data.seat_order
            pass_order.textContent = data.pass_order
            select(seats, data.used_seats)
            select_state_item(sp_fr, data.starting_player_first_round)
            select_state_item(sp_cr, data.starting_player_consecutive_rounds)
            select_state_item(gr_fto, data.game_round_first_turn_order)
            select_state_item(gr_ec, data.game_round_end_condition)
            gr_ec_nr.value = data.game_round_end_condition
            select_state_item(gr_cto, data.game_round_consecutive_turn_order)
            break;
        case 'users':
            users.textContent = (data.count.toString() + " user" + (data.count == 1 ? "" : "s"));
            break;
        default:
            console.error("unsupported event", data);
    }
};