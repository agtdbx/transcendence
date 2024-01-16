let chatSocket = null;
let channelTarget = null;
let lastMessagesLoad = -1;

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
		const username = data['username'];
		// const pp = data['pp'];
		const pp = "https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/c/c2/Gunner_portrait.png/revision/latest/scale-to-width-down/35?cb=20180519150058";
		let date = data['date'];
		date = date.substring(11, 19);
		if (channel == channelTarget)
		{
			console.log("displayMessage");
			addNewMessage(message, username, pp, date);
		}
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
	if (channel == null)
		messagesLoad = null;
	else
	{
		messagesLoad = -1;
		getMessageInDB();
	}
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
	if (input.value == "")
		return ;
	sendMessageToServer(input.value, "general");
	input.value = "";
}


function createMessage(message, username, pp, date)
{
	let messageDiv = document.createElement('tr');
	let nameCase = document.createElement('td');
	let nameTXT = document.createElement('h5');
	let dateTXT = document.createElement('p');
	let imgCase = document.createElement('td');
	let img = document.createElement('img');
	let messageCase = document.createElement('td');
	let messageTXT = document.createElement('p');

	nameCase.style.width = "10%";
	nameCase.style.textAlign = "center";
	nameCase.style.verticalAlign = "top";
	nameTXT.style.marginTop = "5px";
	nameTXT.style.marginBottom = "2px";
	nameTXT.style.color = "white";
	nameTXT.textContent = username;
	nameTXT.style.fontSize = "0.9vw";
	dateTXT.style.marginTop = "0px";
	dateTXT.style.marginBottom = "0px";
	dateTXT.style.color = "white";
	dateTXT.textContent = date;
	dateTXT.style.fontSize = "0.7vw";
	imgCase.style.verticalAlign = "top";
	imgCase.style.width = "10%";
	img.style.width = "100%";
	img.src = pp
	messageCase.style.width = "85%";
	messageCase.style.paddingLeft = "5%";
	messageCase.style.verticalAlign = "top";
	messageTXT.style.marginTop = "5px";
	messageTXT.style.color = "white";
	messageTXT.style.fontSize = "1vw";
	messageTXT.textContent = message;

	messageDiv.insertBefore(nameCase, null);
	messageDiv.insertBefore(imgCase, null);
	messageDiv.insertBefore(messageCase, null);
	nameCase.insertBefore(nameTXT, null);
	nameCase.insertBefore(dateTXT, null);
	imgCase.insertBefore(img, null);
	messageCase.insertBefore(messageTXT, null);

	return messageDiv;
}


function addOldMessage(message, username, pp, date)
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

	chat.appendChild(createMessage(message, username, pp, date));
}


function addNewMessage(message, username, pp, date)
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

	chat.insertBefore(createMessage(message, username, pp, date), null);
}


function getMessageInDB()
{
	let data = new FormData();
	data['lastMessagesLoad'] = lastMessagesLoad;

	fetch('getMessages',
		{
			method: 'POST',
			body: data,
			cache: "default"
		})
		.then(response => response.json())
		.then(data => {
			if (data["success"] == false)
			{
				console.log("Error on load messages :", data['error']);
				return ;
			}
			const messages = data['messages'];
			if (messages.length == 0)
				return
			lastMessagesLoad = messages[0][0];

			for (let i = 0; i < messages.length; i++)
			{
				const data = messages[i][4];
				const username = messages[i][1];
				// const pp = messages[i][2];
				const pp = "https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/c/c2/Gunner_portrait.png/revision/latest/scale-to-width-down/35?cb=20180519150058";
				const date = messages[i][3].substring(0, 8);

				addOldMessage(data, username, pp, date);
			}
		})
}
