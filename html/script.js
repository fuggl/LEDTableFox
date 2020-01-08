var game_round = document.getElementById('game_round'),
    action_round = document.getElementById('action_round'),
    start_seat = document.getElementById('start_seat'),
    active_seat = document.getElementById('active_seat'),
    play = document.getElementsByClassName('play'),
    play1 = document.getElementById('play1'),
    play2 = document.getElementById('play2'),
    pause1 = document.getElementById('pause1'),
    pause2 = document.getElementById('pause2'),
    stop1 = document.getElementById('stop1'),
    stop2 = document.getElementById('stop2'),
    shutdown1 = document.getElementById('shutdown1'),
    shutdown2 = document.getElementById('shutdown2'),
    seat1 = document.getElementById('seat1'),
    seat2 = document.getElementById('seat2'),
    seat3 = document.getElementById('seat3'),
    seat4 = document.getElementById('seat4'),
    seat5 = document.getElementById('seat5'),
    seat6 = document.getElementById('seat6'),
    users = document.getElementById('users'),
    websocket = new WebSocket("ws://127.0.0.1:6789/");
// websocket send
// -- create function that returns a function that sends a message?
var play_fct = function (event) { websocket.send(JSON.stringify({action: 'play', value1: 'pl', value2: ''})); }
play[0].onclick = play_fct
play[1].onclick = play_fct
// play1.onclick = function (event) { websocket.send(JSON.stringify({action: 'play', value1: 'pl', value2: ''})); }
// play2.onclick = function (event) { websocket.send(JSON.stringify({action: 'play', value1: 'pl', value2: ''})); }
pause1.onclick = function (event) { websocket.send(JSON.stringify({action: 'pause', value1: 'pa', value2: ''})); }
pause2.onclick = function (event) { websocket.send(JSON.stringify({action: 'pause', value1: 'pa', value2: ''})); }
stop1.onclick = function (event) { websocket.send(JSON.stringify({action: 'stop', value1: 'st', value2: ''})); }
stop2.onclick = function (event) { websocket.send(JSON.stringify({action: 'stop', value1: 'st', value2: ''})); }
shutdown1.onclick = function (event) { websocket.send(JSON.stringify({action: 'shutdown', value1: 'sd', value2: ''})); }
shutdown2.onclick = function (event) { websocket.send(JSON.stringify({action: 'shutdown', value1: 'sd', value2: ''})); }
seat1.onclick = function (event) { websocket.send(JSON.stringify({action: 'seat', value1: seat1.value, value2: seat1.checked})); }
seat2.onclick = function (event) { websocket.send(JSON.stringify({action: 'seat', value1: seat2.value, value2: seat2.checked})); }
seat3.onclick = function (event) { websocket.send(JSON.stringify({action: 'seat', value1: seat3.value, value2: seat3.checked})); }
seat4.onclick = function (event) { websocket.send(JSON.stringify({action: 'seat', value1: seat4.value, value2: seat4.checked})); }
seat5.onclick = function (event) { websocket.send(JSON.stringify({action: 'seat', value1: seat5.value, value2: seat5.checked})); }
seat6.onclick = function (event) { websocket.send(JSON.stringify({action: 'seat', value1: seat6.value, value2: seat6.checked})); }
// websocket receive
websocket.onmessage = function (event) {
    data = JSON.parse(event.data);
    switch (data.type) {
        case 'state':
            game_round.textContent = data.game_round
            action_round.textContent = data.action_round
            start_seat.textContent = data.start_seat
            active_seat.textContent = data.active_seat
            break;
        case 'users':
            users.textContent = (data.count.toString() + " user" + (data.count == 1 ? "" : "s"));
            break;
        default:
            console.error("unsupported event", data);
    }
};