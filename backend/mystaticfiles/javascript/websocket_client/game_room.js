function createGameRoom()
{
	createListInvite();
}

function createInviteContact(invite_list_container, invite_user)
{
	console.log("invite_user :", invite_user)

	let pp = document.createElement("img");
	pp.src = invite_user["pp"];
	pp.style.width = "3em";
	pp.style.height = "3em";

	let username = document.createElement("p");
	username.textContent = invite_user["name"];
	username.style.color = "white";
	username.style.width = "8em";
	username.style.margin = "0.7em";


	let div = document.createElement("div");
	div.style.display = "flex";
	div.style.flexDirection = "row";
	div.style.backgroundColor = "rgba(18, 16, 11, 0.8)";
	div.appendChild(pp);
	div.appendChild(username);

	invite_list_container.appendChild(div);
}

function createListInvite()
{
	if (popOpened)
		return ;

	fetch("/getcanbeinvited",
	{
		method: 'POST',
		cache: "default"
	})
		.then(response => response.json())
		.then (jsonData => {
			console.log("received from getcanbeinvited : ")
			console.log(jsonData)
			if (! jsonData["success"])
			{
				console.error(jsonData["content"])
				return ;
			}

			let list_invite = jsonData["listcontact"];
			let invite_list_container = document.getElementById("invite_list_container");

			for (let i = 0; i < list_invite.length; i++)
			{
				createInviteContact(invite_list_container, list_invite[i]);
			}
		})
		.catch(error => {
			console.log("erreur from getcanbeinvited :", error)
		});
}
