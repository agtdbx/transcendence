function getFriendsElement()
{
	let friendElement = document.getElementById("SwitchChannel");

	if (friendElement == null)
		friendElement = document.getElementById("wait-page-global");
	if (friendElement == null)
		friendElement = document.getElementById("createGameTopLeft");
	if (friendElement == null)
		friendElement = document.getElementById("tournamentChangeChat");
	if (friendElement == null)
		return null;

	return friendElement;
}


function selectChannel(channel)
{
	if (channel == channelTarget)
		return ;

	const friendElement = getFriendsElement();

	for (let i = 0; i < friendElement.children.length; i++)
	{
		let elem = friendElement.children[i];

		elem.classList = "channel channel-unactive";
	}

	document.getElementById("channel-" + channel).classList = "channel channel-active";
	setChannelTarget(channel);
}


function addChannelFriend(friendElement, friend)
{
	let pp = document.createElement("img");
	pp.src = friend["pp"];
	if (friend["status"] == 0)
		pp.className = "friendPP status-offline";
	else if (friend["status"] == 1)
		pp.className = "friendPP status-online";
	else if (friend["status"] == 2)
		pp.className = "friendPP status-ingame";

	let username = document.createElement("p");
	username.textContent = friend["name"];

	let friendDiv = document.createElement("div");
	friendDiv.classList = "channel channel-unactive";
	friendDiv.id = "channel-" + friend["id"];
	friendDiv.onclick = function () {
		selectChannel(friend["id"]);
	};

	friendDiv.appendChild(pp);
	friendDiv.appendChild(username);

	friendElement.appendChild(friendDiv);
}


function displayFiends()
{
	const friendElement = getFriendsElement();

	fetch("/getlistefriend", {method: 'POST', cache: "default"})
		.then(response => response.json())
		.then (jsonData => {
			if (jsonData['success'])
			{
				let listcontact = jsonData["listcontact"];
				// console.log(jsonData["listcontact"]);
				for (let i = 0; i < listcontact.length; i++)
				{
					console.log(listcontact[i]);
					addChannelFriend(friendElement, listcontact[i]);
				}
			}
			else
			{
				console.log("friendChannel error :", jsonData["error"])
			}
		})
		.catch(error => console.log("error friendChannel fetch :", error));
}
