function createMessage(message, username, pp, date)
{
	let messageDiv = document.createElement('tr');
	let nameCase = document.createElement('td');
	let nameTXT = document.createElement('p');
	let dateTXT = document.createElement('p');
	let imgCase = document.createElement('td');
	let img = document.createElement('img');
	let messageCase = document.createElement('td');
	let messageTXT = document.createElement('p');

	nameCase.style.width = "10%";
	nameCase.style.textAlign = "center";
	nameCase.style.verticalAlign = "top";
	nameCase.onclick = function (){
		changePage("profil/" + username);
	}
	nameTXT.style.marginTop = "5px";
	nameTXT.style.marginBottom = "2px";
	nameTXT.style.color = "white";
	nameTXT.textContent = username;
	nameTXT.style.fontSize = "0.9em";
	dateTXT.style.marginTop = "0px";
	dateTXT.style.marginBottom = "0px";
	dateTXT.style.color = "white";
	dateTXT.textContent = date;
	dateTXT.style.fontSize = "0.7em";
	imgCase.style.verticalAlign = "top";
	imgCase.style.width = "10%";
	imgCase.onclick = function (){
		changePage("profil/" + username);
	}
	img.style.width = "3em";
	img.style.height = "3em";
	img.style.borderRadius = "50%";
	img.src = pp
	messageCase.style.width = "85%";
	messageCase.style.paddingLeft = "0%";
	messageCase.style.verticalAlign = "top";
	messageTXT.style.marginTop = "5px";
	messageTXT.style.color = "white";
	messageTXT.style.fontSize = "1em";
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
	let msg = createMessage(message, username, pp, date);
	chatElement.insertBefore(msg, chatElement.firstChild);
	return msg.offsetHeight;
}


function addNewMessage(message, username, pp, date)
{
	chatElement.insertBefore(createMessage(message, username, pp, date), null);
}


function getMessageInDB()
{
	let data = new FormData();
	data.append('lastMessagesLoad', lastMessagesLoad);
	data.append('channel', channelTarget);

	console.log("Load message form db of channel", channelTarget);

	fetch('/getMessages',
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
				return ;

			lastMessagesLoad = data["lastMessagesLoad"];
			let size = 0;
			for (let i = messages.length - 1; i >= 0; i--)
			{
				const data = messages[i][4];
				const username = messages[i][1];
				const pp = messages[i][2];
				const date = messages[i][3].substring(0, 8);

				size += addOldMessage(data, username, pp, date);
			}

			if (chatScrollAtBottom)
				chatElement.scrollTop = chatElement.scrollHeight;
			else
				chatElement.scrollTop = size;
		});
}
