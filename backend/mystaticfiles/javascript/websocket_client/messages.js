function createMessage(message, username, pp, date)
{
	// Name of the user
	let nameTXT = document.createElement('p');
	nameTXT.textContent = username;
	nameTXT.style.marginTop = "5px";
	nameTXT.style.marginBottom = "2px";
	nameTXT.style.color = "white";
	nameTXT.style.fontSize = "0.9em";

	// Date of message
	let dateTXT = document.createElement('p');
	dateTXT.textContent = date;
	dateTXT.style.marginTop = "0px";
	dateTXT.style.marginBottom = "0px";
	dateTXT.style.color = "white";
	dateTXT.style.fontSize = "0.7em";

	// Container of name and date
	let nameCase = document.createElement('td');
	nameCase.style.width = "10%";
	nameCase.style.textAlign = "center";
	nameCase.style.verticalAlign = "top";
	nameCase.style.animation = "animate 0.40s infinite";
	nameCase.appendChild(nameTXT);
	nameCase.appendChild(dateTXT);
	nameCase.onclick = function (){
		changePage("profil/" + username);
	}

	// PP of the user
	let img = document.createElement('img');
	img.src = pp;
	img.style.width = "3em";
	img.style.height = "3em";
	img.style.borderRadius = "50%";

	// Container of pp
	let imgCase = document.createElement('td');
	imgCase.style.verticalAlign = "top";
	imgCase.style.width = "10%";
	imgCase.style.animation = "animate 0.40s infinite";
	imgCase.appendChild(img);
	imgCase.onclick = function (){
		changePage("profil/" + username);
	}

	// The data of the message
	let messageTXT = document.createElement('p');
	messageTXT.textContent = message;
	messageTXT.style.marginTop = "5px";
	messageTXT.style.color = "white";
	messageTXT.style.fontSize = "1em";

	// Container of message content
	let messageCase = document.createElement('td');
	messageCase.style.width = "85%";
	messageCase.style.paddingLeft = "0%";
	messageCase.style.verticalAlign = "top";
	messageCase.appendChild(messageTXT);

	// Message div
	let messageDiv = document.createElement('tr');
	messageDiv.appendChild(nameCase);
	messageDiv.appendChild(imgCase);
	messageDiv.appendChild(messageCase);

	return messageDiv;
}


function addOldMessage(message, username, pp, date)
{
	let msg = createMessage(message, username, pp, date);
	if (chatElement != null)
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
