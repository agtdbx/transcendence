let webSocket = null;
let channelTarget = null;
let lastMessagesLoad = -1;
let chatElement;
let chatScrollAtBottom = true;

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

	if (webSocket != null)
	{
		console.log("Close last co bro");
		endChatConnection();
	}

	console.log("Try create webSocket at ws://" + window.location.hostname + ":8765");
	try {
		webSocket = new WebSocket("ws://" + window.location.hostname + ":8765/")
	}
	catch (error)
	{
		console.error("ERROR :", error);
		return
	}

	webSocket.onopen = function(e)
	{
		webSocket.send(JSON.stringify({
			'type' : 'connect',
			'cmd' : 'by_token',
			'token': token
		}));
	}

	webSocket.onmessage = onRecieveData;

	webSocket.onerror = function(e) {console.error("ERROR :", e)};
}


function endChatConnection()
{
	if (webSocket != null)
	{
		webSocket.onclose = {};
		webSocket.close();
		webSocket = null;
		console.log("Close chat socket");
	}
}


function getChatElement()
{
	let chat = document.getElementById("main-page-chat-write");

	if (chat == null)
		chat = document.getElementById("createGameChat");
	if (chat == null)
		chat = document.getElementById("tournamentrect1");
	if (chat == null)
		chat = document.getElementById("wait-page-chat-write");
	if (chat == null)
		return ;
	return chat;
}


function setChannelTarget(channel)
{
	console.log("switch to", channel, "channel");
	channelTarget = channel;
	if (channel == null)
	{
		lastMessagesLoad = null;
		chatElement = null;
	}
	else
	{
		lastMessagesLoad = -1;
		chatElement = getChatElement();
		chatElement.innerHTML = "";
		chatScrollAtBottom = true;
		getMessageInDB();
		chatElement.onscroll = function() {
			chatScrollAtBottom = false;
			if (chatElement.offsetHeight + chatElement.scrollTop >= chatElement.scrollHeight)
				chatScrollAtBottom = true;
			else if (chatElement.scrollTop == 0)
				getMessageInDB();
		};
	}
}
