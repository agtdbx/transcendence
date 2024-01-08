function changeBackground(num)
{
	let body = document.getElementById('body');

	if (num == "3")
		body.style.backgroundImage = 'url(/static/image/background/mainpage.png)';
	else if (num == "4")
		body.style.backgroundImage = 'url(/static/image/background/waitpage.png)';
	else if (num == "5")
		body.style.backgroundImage = 'url(/static/image/background/waitpage.png)';
	else if (num == "6")
		body.style.backgroundImage = 'url(/static/image/background/game.png)';
	else if (num == "7")
		body.style.backgroundImage = 'url(/static/image/background/tournament.jpg)';
	else if (num == "8")
		body.style.backgroundImage = 'url(/static/image/background/create_tournament.png)';
	else if (num == "9")
		body.style.backgroundImage = 'url(/static/image/background/profile.jpg)';
	else if (num == "10")
		body.style.backgroundImage = 'url(/static/image/background/ladder.png)';
	else
		body.style.backgroundImage = 'url(/static/image/background/index.png)';
}


function addHeader(){
	let header = document.getElementById("header");
	if (header === null)
	{
		fetch("getHeader", {method: 'POST', cache: "default"})
		.then(response => response.json())
		.then (jsonData => {
			if (jsonData['success'])
				document.querySelector('#Header').innerHTML = jsonData['html'];
			else
				console.log("Header error :", jsonData["error"])
		})
	}
}


function removeHeader()
{
	let header = document.getElementById("header");
	if (header === null)
		return ;
	document.getElementById("header").remove();
}


function manageHeader(num)
{
	if (num >= 3 && num != 6)
		addHeader();
	else
		removeHeader();
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
			});
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
	fetch(`${num}`,
	{
		cache: "default"
	})
	.then(response => response.text())
	.then (htmlText => {
		// Update the content of the page
		document.querySelector('#content').innerHTML = htmlText;

		changeBackground(num);
		manageHeader(num);

		// Run the script tag if they is one in the html load
		runScript();

		// Set the new page in the browser history if the page isn't load by arrow, or not the wait and game page.
		if (!byArrow && num != 4 && num != 6)
			history.pushState({section: num}, '', num);
	})
	.catch(error => console.log("CHANGE PAGE ERROR FETCH :", error, '\n'))
}


function checkLogin(data)
{
	fetch("checkLogin",
		{
			method: 'POST',
			body: data,
			cache: "default"
		})
		.then(response => response.json())
		.then(jsonData => {

			if (jsonData["success"] != true)
			{
				alert(jsonData["error"]);
				return ;
			}

			document.cookie = "token=" + jsonData['token'];
			data.set("token", jsonData['token']);

			changePage("3");
		})
		.catch(error => console.log("checkLogin error :", error))
}


function checkSignin(data)
{
	fetch("checkSignin",
		{
			method: 'POST',
			body: data,
			cache: "default"
		})
		.then(response => response.json())
		.then(jsonData => {

			if (jsonData["success"] != true)
			{
				alert(jsonData["error"]);
				return ;
			}

			document.cookie = "token=" + jsonData['token'];
			data.set("token", jsonData['token']);

			changePage("3");
		})
		.catch(error => console.log("checkSignin error :", error))
}


function disconnection()
{
	document.cookie = "token=";
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
