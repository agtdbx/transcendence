let chatSocket = null;
let channelTarget = null;

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

	if (chatSocket != null)
	{
		console.log("Close last co bro");
		endChatConnection();
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
		const channel = data['channel'];
		const message = data['message'];
		console.log("Message recieved :", message);
		console.log("Channel target :", channelTarget);
		if (channel == channelTarget)
		{
			console.log("displayMessage");
		}
		else
			console.log("Not message display");
	};

	chatSocket.onclose = function(e) {
		console.error('Chat socket closed unexpectedly');
	};
}


function endChatConnection()
{
	if (chatSocket != null)
	{
		chatSocket.onclose = {};
		chatSocket.close();
		chatSocket = null;
		console.log("Close chat socket");
	}
}


function setChannelTarget(channel)
{
	channelTarget = channel;
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
