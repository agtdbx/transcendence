/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   contact.js                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: aderouba <aderouba@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2023/11/23 15:27:08 by lflandri          #+#    #+#             */
/*   Updated: 2024/02/19 15:58:01 by aderouba         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

function removeContactPop()
{
	const popup = document.getElementById("containerContentSuccesBlock");
	console.log("popup : ");
	console.log(popup);
	console.log("\n");
	while (document.getElementById("containerContentSuccesBlock") != null)
		document.getElementById("containerContentSuccesBlock").remove();
	const body = document.getElementById("body");
	body.onclick = null;
}


function contactCreate(content, before, name, img,status)
{
	const container = document.createElement("div");
	const image = document.createElement("img");
	const box = document.createElement("div");
	const divText = document.createElement("div");
	const titleText = document.createElement("h5");
	container.style.padding = "2%";
	container.style.paddingBottom = "0%";
	image.style.width = "20%";
	image.style.marginLeft = "0%";
	image.style.maxWidth = "45px";
	image.style.display = "inline-block";
	image.src = img;
	image.style.border = "3px solid #000000";
	image.style.borderRadius = "600px";
	if (status)
		image.style.borderColor = "green";
	else
		image.style.borderColor = "red";
	box.style.borderRadius = "600px";
	box.style.display = "inline-block";
	box.style.backgroundColor = "#000000";
	box.style.border = "2px solid #FF9C00";
	box.style.textAlign = "left";
	box.style.width = "100%";
	box.style.verticalAlign = "center";
	box.style.maxHeight = "50px";
	box.style.height = "11vw";
	divText.style.verticalAlign = "center";
	divText.style.width = "70%";
	divText.style.position = "relative";
	divText.style.left = "30%";
	divText.style.height = "30px";
	divText.style.marginBottom = "-30px";
	divText.style.fontSize = "10px";
	titleText.style.color = "white";
	titleText.textContent = name;
	titleText.style.textAlign = "left";
	titleText.style.marginTop = "0%";
	titleText.style.marginBottom = "2%";
	titleText.style.fontSize = "30px";
	container.onclick = function (){
		changePage("profil/" + name);
	}
	// container.style.textOverflow = "nowrap";

	content.insertBefore(container, before);
	container.insertBefore(box, before);
	box.insertBefore(divText, null);
	box.insertBefore(image, null);
	divText.insertBefore(titleText, null);
}


function contactPop(type, listContact)
{
	console.log("create contact panel");
	const body = document.getElementById("body");
	const containerContentSuccesBlock = document.createElement("div");
	const contentSuccesBlock = document.createElement("div");
	const succesBlock = document.createElement("div");
	const gameDiv = document.getElementById("content");
	const title = document.createElement("h4");
	body.insertBefore(containerContentSuccesBlock, gameDiv);
	containerContentSuccesBlock.insertBefore(contentSuccesBlock, null);
	contentSuccesBlock.insertBefore(succesBlock, null);
	succesBlock.insertBefore(title, null);
	containerContentSuccesBlock.id = "containerContentSuccesBlock";
	containerContentSuccesBlock.style.position = "absolute";
	containerContentSuccesBlock.style.width = window.innerWidth;
	containerContentSuccesBlock.style.width = "100%";
	contentSuccesBlock.id = "contentSuccessBlock";
	contentSuccesBlock.style.margin = "auto";
	succesBlock.id = "successBlock";
	succesBlock.style.margin = "auto";
	succesBlock.style.backgroundColor = "rgba(18, 16, 11, 0.9)" ;
	succesBlock.style.borderRadius= "30px";
	succesBlock.style.border= "solid #ff9c00";
	containerContentSuccesBlock.style.top = "15%";
	succesBlock.style.borderCollapse = "separate";
	succesBlock.style.textAlign = "center";
	succesBlock.style.padding = "0%"
	succesBlock.style.width = "50%";
	succesBlock.style.maxWidth = "500px";
	succesBlock.style.height = "500px";
	succesBlock.style.overflowY = "auto";
	containerContentSuccesBlock.style.zIndex = "1000";
	title.textContent = type;
	title.style.backgroundColor = "black";
	title.style.color = "white";
	title.style.maxHeight = "50px";
	title.style.padding = "2%";
	title.style.verticalAlign = "center";
	console.log("enter bl contact")
	for (let index = 0; index < listContact.length; index++)
	{
		console.log("create : " + listContact[index]["name"])
		contactCreate(succesBlock,
				null,
				listContact[index]["name"],
				listContact[index]["pp"],
				listContact[index]["status"]);
	}
}




function ContactList(type)
{
	if (popOpened)
		return ;
	const form = document.getElementById('data-request-relation');
	const data = new FormData(form);
	url = "https://" + window.location.hostname + ":4200/getlisteblocked"
	if (type === "friends")
	{
		url = "https://" + window.location.hostname + ":4200/getlistefriend"
	}

	fetch(url,
	{
		method: 'POST',
		body: data,
		cache: "default"
	})
			.then(response => response.json())
			.then (jsonData => {
				console.log("received from getlistecontact : ")
				console.log(jsonData)
				if (! jsonData["success"])
				{
					console.error(jsonData["content"])
					return ;
				}

				popOpened = true;
				document.getElementById("Page").classList.add("blur");
				contactPop(type, jsonData["listcontact"])
				setTimeout(function(){
					const body = document.getElementById("body");
					body.onclick = remove_pop; //removeContactPop
				}, 10);
			})
			.catch(error => {
				console.log("erreur from getlistecontact : ")
				console.error(error)
			})

}
