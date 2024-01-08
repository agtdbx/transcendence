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
				document.querySelector('#Header').innerHTML = jsonData['html']
			else
				console.log("ERROR HEADER", jsonData)
		})
	}
}


function removeHeader()
{
	let header = document.getElementById("header");
	if (header === null)
		return ;
	document.getElementById("header").remove()
}


function manageHeader(num)
{
	if (num >= 3 && num != 6)
		addHeader()
	else
		removeHeader()
}


function changePage(num)
{
	fetch(`${num}`,
	{
		cache: "default"
	})
	.then(response => response.text())
	.then (htmlText => {
		changeBackground(num);

		manageHeader(num);

		document.getElementById("Page").remove()
		document.querySelector('#content').innerHTML = htmlText;

		/* this is an advertissement : don't try to understand, i know, you don't*/
		var scripts = document.querySelector('#content').querySelectorAll("script");
		for (var i = 0; i < scripts.length; i++) {
			// console.log("SCRIPT : " + scripts[i])
			// console.log("len : " + scripts.length)
			if (scripts[i].innerText) {
				eval(scripts[i].innerText);
			} else {
				// console.log("src : " + scripts[i].src)
				fetch(scripts[i].src).then(function (data) {
					data.text().then(function (r) {
						eval(r);
					})
				});

			}
		}

		// If load page without connection, clear the token
		if (num < 3)
		{
			data.set("token", null)
		}

		// Set the new page in the browser history
		// history.pushState({section: num}, '', num)
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
				console.log("ERROR :", jsonData["error"])
				alert(jsonData["error"])
				return
			}

			document.cookie = "token=" + jsonData['token']
			data.set("token", jsonData['token'])

			changePage("3")
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
				console.log("ERROR :", jsonData["error"])
				alert(jsonData["error"])
				return
			}

			document.cookie = "token=" + jsonData['token']
			data.set("token", jsonData['token'])

			changePage("3")
		})
		.catch(error => console.log("checkSignin error :", error))
}
