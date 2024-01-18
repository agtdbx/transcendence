function onRecieveMessage(event)
{
	let data = null;
	try
	{
		data = JSON.parse(event.data);
	}
	catch
	{
		console.log(event.data)
	}

	const channel = data['channel'];
	const message = data['message'];
	const username = data['username'];
	const pp = data['pp'];
	const date = data['date'].substring(11, 19);
	if (channel == channelTarget)
	{
		addNewMessage(message, username, pp, date);

		if (chatScrollAtBottom)
			chatElement.scrollTop = chatElement.scrollHeight;
	}
}



// Send message to server
function sendMessageToServer(message, channel) {
	chatSocket.send(JSON.stringify({
		'sender': getToken(),
		'channel' : channel,
		'message': message
	}));
}


function sendMessage(input)
{
	if (input.value == "")
		return ;
	chatScrollAtBottom = true;
	sendMessageToServer(input.value, channelTarget);
	input.value = "";
}
