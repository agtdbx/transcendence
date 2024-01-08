var app_href = window.location.href

// function openPopupLog()
// {
// 	let popup = document.getElementById("popupLogin");
// 	popup.classList.add("open-Popup");
// 	document.getElementById("btn-log").style.display= "none";
// 	document.getElementById("btn-sign").style.display= "none";
// 	document.getElementById("btn-log").style.visibility= "hidden";
// 	document.getElementById("btn-sign").style.visibility= "hidden";
// }

// function openPopupSign()
// {
// 	let popup2 = document.getElementById("popupSign");
// 	popup2.classList.add("open-Popup");
// 	document.getElementById("btn-log").style.display= "none";
// 	document.getElementById("btn-sign").style.display= "none";
// 	document.getElementById("btn-log").style.visibility= "hidden";
// 	document.getElementById("btn-sign").style.visibility= "hidden";
// }

// function swapToSign()
// {
// 	let popup = document.getElementById("popupLogin");
// 	let popup2 = document.getElementById("popupSign");
// 	popup.classList.remove("open-Popup");
// 	popup2.classList.add("open-Popup");
// }

// function swapToLog()
// {
// 	let popup2 = document.getElementById("popupSign");
// 	let popup = document.getElementById("popupLogin");
// 	popup.classList.add("open-Popup");
// 	popup2.classList.remove("open-Popup");
// }

function addHeader(data){
	let header = document.getElementById("header");
	if (header === null)
	{
		fetch(`0`, {method: 'POST', body: data, cache: "default"})
		.then(response => response.json())
		.then (jsonData => {
			if (jsonData['success'])
				document.querySelector('#Header').innerHTML = jsonData['html']
			else
				console.log("ERROR HEADER", jsonData)
		}
		)
	}
}

function removeHeader()
{
	let header = document.getElementById("header");
	if (header === null)
		return ;
	document.getElementById("header").remove()
}

function changePage(num, data)
{
	fetch(`${num}`,
	{
		cache: "default"
	})
	.then(response => response.json())
	.then (jsonData => {

		if (jsonData["success"] != true)
		{
			console.log("ERROR :", jsonData["error"])
			alert(jsonData["error"])
			return
		}

		document.getElementById("Page").remove()
		let body = document.getElementById('body');
		document.querySelector('#content').innerHTML = jsonData['html'];

		switch (num) {
			case "1":
			case "2":
			case "3":
				body.style.backgroundImage = 'url(/static/image/background/mainpage.png)';
				addHeader(data);
				break;
			case "4":
				body.style.backgroundImage = 'url(/static/image/background/waitpage.png)';
				addHeader(data);
				break;
			case "5":
				body.style.backgroundImage = 'url(/static/image/background/waitpage.png)';
				addHeader(data);
				break;
			case "6":
				body.style.backgroundImage = 'url(https://images.squarespace-cdn.com/content/v1/5925832e03596efb6d4b502a/1547827451369-JX3S8JTAWQMWHYFYDVNK/Magma.jpg?format=2500w)';
				addHeader(data);
				break;
			case "7":
				body.style.backgroundImage = 'url(/static/image/background/DRG_Wallpaper_CrystalCaves.jpg)';
				addHeader(data);
				break;
			case "8":
				body.style.backgroundImage = 'url(/static/image/background/Background.png)';
				removeHeader();
				break;
			default:
				break;
		}

		/* this is an advertissement : don't try to understand, i know, you don't*/
		var scripts = document.querySelector('#content').querySelectorAll("script");
		for (var i = 0; i < scripts.length; i++) {
			console.log("SCRIPT : " + scripts[i])
			console.log("len : " + scripts.length)
			if (scripts[i].innerText) {
				eval(scripts[i].innerText);
			} else {
				console.log("src : " + scripts[i].src)
				fetch(scripts[i].src).then(function (data) {
					data.text().then(function (r) {
						eval(r);
					})
				});

			}
			// To not repeat the element
			//scripts[i].parentNode.removeChild(scripts[i]);
		}
		console.log(app_href + num)
		history.pushState({section: num}, '', num)
	})
	.catch(error => console.log("ERROR FETCH :", error, '\n', data))
}


function showcontent(num, data)
{
	// When login
	if (num == 1)
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

			changePage(num, data)
		})
		.catch(error => console.log("checkLogin error :", error))
	}
	// When signin
	else if (num == 2)
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

			changePage(num, data)
		})
		.catch(error => console.log("checkSignin error :", error))
	}
	else
	{
		changePage(num, data)
	}
}

window.onpopstate = function(event)
{
	try
	{
		console.log("Change to", event.state.section)
		showcontent(event.state.section, null)
	}
	catch
	{
		console.log("Change to main")
		window.location.href = app_href
	}
}
