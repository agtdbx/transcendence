function join_request_quick_game()
{
	console.log("SEND QUICK JOIN REQUEST TO SERVER");
	webSocket.send(JSON.stringify({
		'type' : 'quickRoom',
		'cmd' : 'askForRoom'
	}));
}


function leave_request_quick_game()
{
	console.log("SEND QUICK LEAVE REQUEST TO SERVER");
	webSocket.send(JSON.stringify({
		'type' : 'quickRoom',
		'cmd' : 'quitRoom'
	}));
}
