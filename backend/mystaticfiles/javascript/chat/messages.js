let chatSocket = null;

function getToken()
{
	let cookies = document.cookie.split("; ");

	let i = 0;
	while (i < cookies.length)
	{
		let key = cookies[i].substring(0, 5);
		if (key == "token")
			return cookies[i].substring(6);
		i++;
	}
	return null;
}


function enableChatConnection()
{
	const token = getToken();

	if (token == null)
	{
		console.log("Nope bro");
		return ;
	}

	console.log("Create ChatSocket");
	chatSocket = new WebSocket("ws://" + window.location.hostname + ":8765");

	chatSocket.onopen = function(e)
	{
		console.log("Send who I am to server");
		chatSocket.send(JSON.stringify({
			'whoiam': token
		}));
	}

	chatSocket.onmessage = function(e) {
		console.log("Data recieved :", e.data);
		const data = JSON.parse(e.data);
		console.log("Data parse :", data);
		const message = data['message'];

		console.log("Message recieved :", message);
	};

	chatSocket.onclose = function(e) {
		console.error('Chat socket closed unexpectedly');
	};
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
