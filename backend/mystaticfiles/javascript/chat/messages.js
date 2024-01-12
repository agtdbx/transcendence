console.log("Create ChatSocket");
const chatSocket = new WebSocket("ws://" + window.location.hostname + ":8765");

chatSocket.onmessage = function(e) {
	const data = JSON.parse(e.data);
	const message = data['message'];
	// Handle incoming message
};

chatSocket.onclose = function(e) {
	console.error('Chat socket closed unexpectedly');
};

function getToken()
{
	let cookies = document.cookie.split("; ");

	let i = 0;
	while (i < cookies.length)
	{
		let key = cookies[i].substring(0, 5);
		// console.log("key :", key);
		if (key == "token")
			// console.log("TOKEN :", cookies[i].substring(6));
			return cookies[i].substring(6);
		i++;
	}
	return null;
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
	console.log("Try to send the message");
	sendMessageToServer(input.value, "general");
	input.value = "";
}

