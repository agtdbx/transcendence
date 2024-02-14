/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   friend_request.js                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: hde-min <hde-min@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2024/01/16 22:32:37 by lflandri          #+#    #+#             */
/*   Updated: 2024/02/14 14:12:38 by hde-min          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */


var popupCreatedCount = 0;

function comfirmFriendRequest(user)
{
	let body = document.getElementById('body');
	document.getElementById("Page").classList.add("blur");
	let container = document.createElement('div');
	let popup = document.createElement('div');
	let text = document.createElement('p');
	let acceptBtn = document.createElement('button');
	let refusedBtn = document.createElement('button');

	container.style.position = "absolute";
	container.style.width = "100%";
	container.style.height = "600px";
	container.style.top = "0px";
	popup.style.position = "relative";
	popup.style.boxShadow = "26px 21px 27px 5px #000000";
	popup.style.left = "35%";
	popup.style.top = "400px";
	popup.style.height = "200px";
	popup.style.backgroundColor = "rgba(18, 16, 11, 0.9)";
	popup.style.padding = "2%";
	popup.style.width = "30%";
	popup.style.borderRadius = "40px 0px 40px 0px";
	popup.style.border= "solid #ff9c00";
	popup.style.textAlign= "center";
	text.style.color = "white";
	text.textContent = "Dwarf " + user + " wants to be friend with you !";
	acceptBtn.classList.add("btn-drg")
	refusedBtn.classList.add("btn-drg")
	acceptBtn.textContent = "Accept"
	refusedBtn.textContent = "Refuse"
	acceptBtn.style.width = "25%"
	acceptBtn.style.margin = "2%"
	acceptBtn.style.marginTop = "5%"
	acceptBtn.style.marginLeft = "0%"
	refusedBtn.style.width = "25%"
	refusedBtn.style.margin = "0%"
	acceptBtn.onclick = function ()
	{
		document.getElementById("Page").classList.remove("blur");
		popupCreatedCount--;
		container.remove()
		document.getElementById("data-request-relation-input").value = user;
		const form = document.getElementById('data-request-relation');
		const data = new FormData(form);
		fetch("https://" + window.location.hostname + ":4200/acceptfriends",
		{
			method: 'POST',
			body: data,
			cache: "default"
		})
				.then(response => response.json())
				.then (jsonData => {
					if (! jsonData["success"])
					{
						console.error(jsonData["content"])
						return ;
					}
					console.log("received from friendresponse : ")
					console.log(jsonData)
					
				})
				.catch(error => {
					console.log("erreur from getlistefriendrequest : ")
					console.error(error)
				})
	};
	refusedBtn.onclick = function ()
	{
		document.getElementById("Page").classList.remove("blur");
		popupCreatedCount--;
		container.remove()
		document.getElementById("data-request-relation-input").value = user;
		const form = document.getElementById('data-request-relation');
		const data = new FormData(form);
		fetch("https://" + window.location.hostname + ":4200/refusefriends",
			{
				method: 'POST',
				body: data,
				cache: "default"
			})
					.then(response => response.json())
					.then (jsonData => {
						if (! jsonData["success"])
						{
							console.error(jsonData["content"])
							return ;
						}
						console.log("received from friendresponse : ")
						console.log(jsonData)
						
					})
					.catch(error => {
						console.log("erreur from getlistefriendrequest : ")
						console.error(error)
					})
	};
	body.appendChild(container);
	container.appendChild(popup);
	popup.appendChild(text);
	popup.appendChild(acceptBtn);
	popup.appendChild(refusedBtn);
}

async function sendRequestToClient(jsonData)
{
	for (const user of jsonData["listRequest"])
	{
		document.getElementById("data-request-relation-input").value = user;
		const form = document.getElementById('data-request-relation');
		const data = new FormData(form);
		console.log("request to : " + user)
		let popupInterval = setInterval(
			function ()
			{	if (popupCreatedCount === 0)
				{
					popupCreatedCount++;
					comfirmFriendRequest(user);
					clearInterval(popupInterval);
				}
			},
			100);

	}
	
}

const form = document.getElementById('data-request-relation');
const data = new FormData(form);

fetch("https://" + window.location.hostname + ":4200/getlistefriendrequest",
{
	method: 'POST',
	body: data,
	cache: "default"
})
		.then(response => response.json())
		.then (jsonData => {
			console.log("received from getlistefriendrequest : ")
			console.log(jsonData)
			if (! jsonData["success"])
			{
				console.error(jsonData["content"])
				return ;
			}
			sendRequestToClient(jsonData);
			
		})
		.catch(error => {
			console.log("erreur from getlistefriendrequest : ")
			console.error(error)
		})
