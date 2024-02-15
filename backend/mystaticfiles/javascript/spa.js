let current_page = null;
let pageInLoad = false;

function changeBackground(num)
{
	current_page = num;
	let body = document.getElementById('body');

	if (num == "3")
		body.style.backgroundImage = 'url(/static/image/background/mainpage.png)';
	else if (num == "4")
		body.style.backgroundImage = 'url(/static/image/background/waitpage.png)';
	else if (num == "5" || num == "51")
		body.style.backgroundImage = 'url(/static/image/background/waitpage.png)';
	else if (num == "6")
		body.style.backgroundImage = 'url(/static/image/background/game.png)';
	else if (num == "7" || num == "71" || num == "72" || num == "73")
		body.style.backgroundImage = 'url(/static/image/background/tournament.jpg)';
	else if (num == "8")
		body.style.backgroundImage = 'url(/static/image/background/create_tournament.png)';
	else if (num == "9")
		body.style.backgroundImage = 'url(/static/image/background/profile.jpg)';
	else if (num == "10")
		body.style.backgroundImage = 'url(/static/image/background/ladder.png)';
	else if (num == "11")
		body.style.backgroundImage = 'url(/static/image/background/abyss.png)';
	else if (num == "12")
		body.style.backgroundImage = 'url(/static/image/background/abyss.png)'
	else
	{
		if (num.length >= 6 && String(num).substring(0, 6) == "profil")
			body.style.backgroundImage = 'url(/static/image/background/profile.jpg)';
		else
			body.style.backgroundImage = 'url(/static/image/background/index.png)';
	}
	current_page = num;
}

function addHeader(){
	let header = document.getElementById("NavHeader");
	if (header === null)
	{
		try
		{
			fetch("/getHeader", {method: 'POST', cache: "default"})
			.then(response => response.json())
			.then (jsonData => {
				if (jsonData['success'])
				{
					document.querySelector('#Header').innerHTML = jsonData['html'];
					addBosco();
				}
				else
					console.log("Header error :", jsonData["error"])
			})
			.catch(error => {
				console.log("erreur addHeader fetch : ")
				console.error(error)
			})
		}
		catch (error) {
			console.log("erreur addHeader : ")
			console.error(error)
		}

	}
}


function removeHeader()
{
	let header = document.getElementById("NavHeader");
	if (header === null)
		return ;
	document.getElementById("NavHeader").remove();
}


function manageHeader(num)
{
	if (num < 3 || num == 6)
		removeHeader();
	else
		addHeader();
}


function manageChat(num)
{
	if (num == 3 || num == 4 || num == 5 || num == 51 || num == 71 || num == 72 || num == 8)
	{
		setChannelTarget("general");
		displayFiends();
	}
	else
		setChannelTarget(null);
}


function manageAPI(num)
{
	if (current_page == 4)
	{
		leave_request_quick_game();
	}
	else if (current_page == 5 || current_page == 51)
	{
		quitGameRoom();
	}

	if (num == 3)
	{
		pageForTournamentStatus = "mainpage";
		getTournamentStatus();
	}
	else if (num == 4)
	{
		join_request_quick_game();
	}
	else if (num == 5)
	{
		createGameRoom();
	}
	else if (num == 71 || num == 72)
	{
		getTournamentStatus();
		getTournamentTree();
		getTournamentNextMatch();
		getTournamentMyNextMatch();
	}
	else if (num == 73)
	{
		getTournamentTree();
		getTournamentResult();
	}
}


function runScript()
{
	/* this is an advertissement : don't try to understand, i know, you don't*/
	var scripts = document.querySelector('#content').querySelectorAll("script");
	for (var i = 0; i < scripts.length; i++) {
		if (scripts[i].innerText) {
			eval(scripts[i].innerText);
		} else {
			fetch(scripts[i].src).then(function (data) {
				data.text().then(function (r) {
					eval(r);
				})
			}).catch(error => console.log("error :", error))
		}
	}
}


function getCookieValue(name)
{
	const regex = new RegExp(`(^| )${name}=([^;]+)`)
	const match = document.cookie.match(regex)
	if (match) {
	return match[2]
	}
}


function changePage(num, byArrow=false)
{
	if (num == current_page)
		return ;
		try
		{
			remove_pop();
			let id = 0;
			while (document.getElementById("grapheMatch" + id))
			{
				document.getElementById("grapheMatch" + id).remove();
				id++;
			}

		}
		catch (error)
		{
			console.error(error)
		}

	pageInLoad = true;
	fetch("/" + `${num}`,
	{
		method: 'POST',
		cache: "default"
	})
	.then(response => response.text())
	.then (htmlText => {
		// Update the content of the page
		document.querySelector('#content').innerHTML = htmlText;

		manageHeader(num);
		manageChat(num);
		manageAPI(num);
		changeBackground(num);

		current_page = num;

		// Run the script tag if they is one in the html load
		runScript();
		// Set the new page in the browser history if the page isn't load by arrow, or not the wait and game page.
		if (!byArrow && num != 4 && num != 5 && num != 51 && num != 6)
			history.pushState({section: num}, "", "/" + num);
		pageInLoad = false;
	})
	.catch(error => console.log("CHANGE PAGE ERROR FETCH :", error, '\n'))
}


function checkLogin(data)
{
	fetch("/checkLogin",
		{
			method: 'POST',
			body: data,
			cache: "default"
		})
		.then(response => response.json())
		.then(jsonData => {

			if (jsonData["success"] != true)
			{
				//alert(jsonData["error"]);
				error = document.getElementById("LoginError")
				error.innerHTML=jsonData["error"]
				toCLear = document.getElementById("LoginPassword")
				toCLear.value = ""
				return ;
			}

			document.cookie = "token=" + jsonData['token'];
			data.set("token", jsonData['token']);

			enableChatConnection();

			changePage("3");
		})
		.catch(error => console.log("checkLogin error :", error))
}


function checkSignin(data)
{
	fetch("/checkSignin",
	{
		method: 'POST',
		body: data,
		cache: "default"
	})
	.then(response => response.json())
	.then(jsonData => {

		if (jsonData["success"] != true)
		{
			errorSign = document.getElementById("SignError")
			errorSign.innerHTML=jsonData["error"]
			toCLear = document.getElementById("SignUsername")
			toCLear.value = ""
			toCLear = document.getElementById("SignPassword")
			toCLear.value = ""
			toCLear = document.getElementById("SignConfirm")
			toCLear.value = ""
			return ;
		}

		document.cookie = "token=" + jsonData['token'];
		data.set("token", jsonData['token']);

		enableChatConnection();

			changePage("3");
		})
		.catch(error => console.log("checkSignin error :", error))
	}

function changePassword(data)
{
	fetch("changePassword",
	{
		method: 'POST',
		body: data,
		cache: "default"
	})
	.then(response => response.json())
	.then(jsonData => {

		if (jsonData["success"] != true)
		{
			errorSign = document.getElementById("errorPopPassword")
			errorSign.innerHTML=jsonData["error"]
			return ;
		}
		remove_pop()
	})
	.catch(error => console.log("checkSignin error :", error))
}

function changeUsername(data)
{
	fetch("changeUsername",
	{
		method: 'POST',
		body: data,
		cache: "default"
	})
	.then(response => response.json())
	.then(jsonData => {

		if (jsonData["success"] != true)
		{
			errorSign = document.getElementById("errorPopUsername")
			errorSign.innerHTML=jsonData["error"]
			return ;
		}
		let name = document.getElementById("pseudo_profil_page");
		name.textContent = document.getElementById("newName").value;

		let name2 = document.getElementById("NavUserName");
		name2.textContent = document.getElementById("newName").value;
		remove_pop()
	})
	.catch(error => console.log("changeUsername error :", error))
}

function disconnection()
{
	document.cookie = "token=";
	console.log("test");
	endChatConnection();
	changePage("0");
}


window.onpopstate = function(event)
{
	try
	{
		console.log("Back", event.state.section)
		changePage(event.state.section, true);
	}
	catch
	{
		changePage(0, true);
	}
}
