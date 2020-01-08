var round_nr = document.querySelector('#round'),
    play = document.getElementsByClassName('play'),
    play1 = document.querySelector('#play1'),
    play2 = document.querySelector('#play2'),
    pause1 = document.querySelector('#pause1'),
    pause2 = document.querySelector('#pause2'),
    stop1 = document.querySelector('#stop1'),
    stop2 = document.querySelector('#stop2'),
    shutdown1 = document.querySelector('#shutdown1'),
    shutdown2 = document.querySelector('#shutdown2'),
    seat1 = document.querySelector('#seat1'),
    seat2 = document.querySelector('#seat2'),
    seat3 = document.querySelector('#seat3'),
    seat4 = document.querySelector('#seat4'),
    seat5 = document.querySelector('#seat5'),
    seat6 = document.querySelector('#seat6'),
    users = document.querySelector('.users'),
    websocket = new WebSocket("ws://192.168.0.3/:6789/");
// websocket send
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
    round_nr.textContent = data.round_nr
    break;
  case 'users':
    users.textContent = (data.count.toString() + " user" + (data.count == 1 ? "" : "s"));
    break;
  default:
    console.error("unsupported event", data);
}
};