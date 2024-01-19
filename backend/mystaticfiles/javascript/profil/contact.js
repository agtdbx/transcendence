/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   contact.js                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: lflandri <lflandri@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2023/11/23 15:27:08 by lflandri          #+#    #+#             */
/*   Updated: 2023/12/07 14:49:05 by lflandri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

//TODO all

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
	succesBlock.style.backgroundColor = "rgba(40, 35, 23, 0.75)" ;
	succesBlock.style.borderCollapse = "separate";
	succesBlock.style.textAlign = "center";
	succesBlock.style.padding = "0%"
	succesBlock.style.width = "50%";
	succesBlock.style.maxWidth = "400px";
	succesBlock.style.height = "500px";
	succesBlock.style.overflowY = "scroll";
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
	listContact =
		[

			{
				"name" : "Enginer",
				"pp" : "https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/4/46/Engineer_portrait.png/revision/latest/scale-to-width-down/35?cb=20180519150041",
				"status" : 0
			},
			{
				"name" : "Gunner",
				"pp" : "https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/c/c2/Gunner_portrait.png/revision/latest/scale-to-width-down/35?cb=20180519150058",
				"status" : 1
			},
			{
				"name" : "Gunner",
				"pp" : "https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/c/c2/Gunner_portrait.png/revision/latest/scale-to-width-down/35?cb=20180519150058",
				"status" : 1
			},
			{
				"name" : "Gunner",
				"pp" : "https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/c/c2/Gunner_portrait.png/revision/latest/scale-to-width-down/35?cb=20180519150058",
				"status" : 1
			},
			{
				"name" : "Gunner",
				"pp" : "https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/c/c2/Gunner_portrait.png/revision/latest/scale-to-width-down/35?cb=20180519150058",
				"status" : 1
			},
			{
				"name" : "Gunner",
				"pp" : "https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/c/c2/Gunner_portrait.png/revision/latest/scale-to-width-down/35?cb=20180519150058",
				"status" : 1
			},
			{
				"name" : "Gunner",
				"pp" : "https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/c/c2/Gunner_portrait.png/revision/latest/scale-to-width-down/35?cb=20180519150058",
				"status" : 1
			},
			{
				"name" : "Gunner",
				"pp" : "https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/c/c2/Gunner_portrait.png/revision/latest/scale-to-width-down/35?cb=20180519150058",
				"status" : 1
			},
			{
				"name" : "Gunner",
				"pp" : "https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/c/c2/Gunner_portrait.png/revision/latest/scale-to-width-down/35?cb=20180519150058",
				"status" : 1
			},
			{
				"name" : "Gunner",
				"pp" : "https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/c/c2/Gunner_portrait.png/revision/latest/scale-to-width-down/35?cb=20180519150058",
				"status" : 1
			},
			{
				"name" : "Gunner",
				"pp" : "https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/c/c2/Gunner_portrait.png/revision/latest/scale-to-width-down/35?cb=20180519150058",
				"status" : 1
			},
			{
				"name" : "Gunner",
				"pp" : "https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/c/c2/Gunner_portrait.png/revision/latest/scale-to-width-down/35?cb=20180519150058",
				"status" : 1
			},
			{
				"name" : "Gunner",
				"pp" : "https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/c/c2/Gunner_portrait.png/revision/latest/scale-to-width-down/35?cb=20180519150058",
				"status" : 1
			},
			{
				"name" : "Gunner",
				"pp" : "https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/c/c2/Gunner_portrait.png/revision/latest/scale-to-width-down/35?cb=20180519150058",
				"status" : 1
			},
			{
				"name" : "Gunner",
				"pp" : "https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/c/c2/Gunner_portrait.png/revision/latest/scale-to-width-down/35?cb=20180519150058",
				"status" : 1
			},
			{
				"name" : "Gunner",
				"pp" : "https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/c/c2/Gunner_portrait.png/revision/latest/scale-to-width-down/35?cb=20180519150058",
				"status" : 1
			},
			{
				"name" : "Gunner",
				"pp" : "https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/c/c2/Gunner_portrait.png/revision/latest/scale-to-width-down/35?cb=20180519150058",
				"status" : 1
			},
			{
				"name" : "Gunner",
				"pp" : "https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/c/c2/Gunner_portrait.png/revision/latest/scale-to-width-down/35?cb=20180519150058",
				"status" : 1
			},
			{
				"name" : "Gunner",
				"pp" : "https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/c/c2/Gunner_portrait.png/revision/latest/scale-to-width-down/35?cb=20180519150058",
				"status" : 1
			},
			{
				"name" : "Gunner",
				"pp" : "https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/c/c2/Gunner_portrait.png/revision/latest/scale-to-width-down/35?cb=20180519150058",
				"status" : 1
			},
			{
				"name" : "Gunner",
				"pp" : "https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/c/c2/Gunner_portrait.png/revision/latest/scale-to-width-down/35?cb=20180519150058",
				"status" : 1
			},
			{
				"name" : "Gunner",
				"pp" : "https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/c/c2/Gunner_portrait.png/revision/latest/scale-to-width-down/35?cb=20180519150058",
				"status" : 1
			}
		]
	contactPop(type, listContact)
	setTimeout(function(){
		const body = document.getElementById("body");
		body.onclick = removeContactPop;
	}, 500);
}