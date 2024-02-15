/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   friend_request.js                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: lflandri <lflandri@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2024/01/16 22:32:37 by lflandri          #+#    #+#             */
/*   Updated: 2024/02/15 15:32:58 by lflandri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */


var popupCreatedCount = 0;

function comfirmFriendRequest(user, first_value)
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
	container.style.height = "1080px";
	container.style.top = "0px";
	popup.style.position = "relative";
	popup.style.boxShadow = "26px 21px 27px 5px #000000";
	popup.style.left = "35%";
	popup.style.top = "400px";
	popup.style.height = "200px";
	popup.style.backgroundColor = "rgba(18,16,11, 0.75)";
	popup.style.padding = "2%";
	popup.style.width = "30%";
	popup.style.borderRadius = "40px 0px 40px 0px";
	text.style.color = "white";
	text.textContent = "You have a friend request of " + user + ".\n\nDo you accept it ?";
	acceptBtn.classList.add("btn-drg")
	refusedBtn.classList.add("btn-drg")
	acceptBtn.textContent = "Accept"
	refusedBtn.textContent = "Refuse"
	acceptBtn.style.width = "20%"
	acceptBtn.style.margin = "15%"
	refusedBtn.style.width = "20%"
	refusedBtn.style.margin = "15%"
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
		document.getElementById("data-request-relation-input").value = first_value;
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
		document.getElementById("data-request-relation-input").value = first_value;
	};
	body.appendChild(container);
	container.appendChild(popup);
	popup.appendChild(text);
	popup.appendChild(acceptBtn);
	popup.appendChild(refusedBtn);
}

async function sendRequestToClient(jsonData)
{
	let first_value = document.getElementById("data-request-relation-input").value;
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
					comfirmFriendRequest(user, first_value);
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