/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   achievement_and_stat.js                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: hde-min <hde-min@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2023/11/23 15:24:40 by lflandri          #+#    #+#             */
/*   Updated: 2024/02/06 15:24:51 by hde-min          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

//TODO connection to db

var popOpened = false;

function remove_pop()
{
	if (!popOpened)
		return ;
	popOpened = false;
	document.getElementById("Page").classList.remove("blur");
	const popup = document.getElementById("containerContentSuccesBlock");
	console.log("popup : ");
	console.log(popup);
	console.log("\n");
	while (document.getElementById("containerContentSuccesBlock") != null)
		document.getElementById("containerContentSuccesBlock").remove();
	const body = document.getElementById("body");
	body.onclick = null;
}

function casePup(content, before, title, img, description, grade)
{
	const container = document.createElement("div");
	const image = document.createElement("img");
	const box = document.createElement("div");
	const divText = document.createElement("div");
	const titleText = document.createElement("h5");
	const text = document.createElement("p");
	image.style.width = "30%";
	image.style.display = "inline-block";
	image.src = img;
	// container.style.width = "100%";
	container.classList.add("col-sm-12");
	container.classList.add("col-md-6");
	container.classList.add("col-lg-6");
	container.classList.add("col-xl-4");
	// box.style.display = "inline-block";
	box.style.height = "90px"
	box.style.backgroundColor = "#000000";
	box.style.border = "1px solid #FF9C00";
	box.style.marginBottom = "15px";
	box.style.textAlign = "left";
	box.classList.add("mx-1");
	divText.style.width = "70%";
	divText.style.position = "relative";
	divText.style.left = "30%";
	divText.style.height = "30px";
	divText.style.marginBottom = "-30px";
	divText.style.fontSize = "10px";
	titleText.style.color = "white";
	titleText.textContent = title;
	titleText.style.textAlign = "center";
	titleText.style.marginTop = "1px";
	titleText.style.marginBottom = "0px";
	titleText.style.fontSize = "15px";
	text.style.color = "white";
	text.textContent = description;
	text.style.marginTop = "5px";
	content.insertBefore(container, before);
	container.insertBefore(box, before);
	box.insertBefore(divText, null);
	box.insertBefore(image, null);
	divText.insertBefore(titleText, null);
	divText.insertBefore(text, null);

	if (grade > 0 && grade < 4 )
	{
		const gradeContainer = document.createElement("div");
		const gradeImage = document.createElement("img");
		gradeImage.style.height = "30px";
		gradeImage.style.marginBottom = "-30px";
		gradeImage.style.marginTop = "0px";
		gradeImage.style.position = "relative";
		gradeImage.style.left = "0%";
		gradeImage.style.top = "-50px";
		gradeImage.style.width = "25%"
		gradeContainer.style.height = "30px";
		gradeContainer.style.marginBottom = "-30px";
		gradeImage.src = "/static/image/achievement/Achievement_level_" + grade + ".webp";
		// switch (grade)
		// {
		// 	case 1:
		// 		gradeImage.src = "https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/5/5e/Icons_complexity_1.png/revision/latest/scale-to-width-down/60?cb=20190210235110";
		// 		break;
		
		// 	case 2:
		// 		gradeImage.src = "https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/e/e3/Icons_complexity_2.png/revision/latest/scale-to-width-down/60?cb=20190210235125";
		// 		break;
		// 	case 3:
		// 		gradeImage.src = "https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/1/1f/Icons_complexity_3.png/revision/latest/scale-to-width-down/60?cb=20190210235136";
		// 		break;
		// }
		container.insertBefore(gradeContainer, null);
		gradeContainer.insertBefore(gradeImage, null);
	}
}

function createSuccess(listeAchievement)
{
	console.log("create success panel");
	const body = document.getElementById("body");
	const containerContentSuccesBlock = document.createElement("div");
	const contentSuccesBlock = document.createElement("div");
	const succesBlock = document.createElement("div");
	const gameDiv = document.getElementById("content");
	body.insertBefore(containerContentSuccesBlock, gameDiv);
	containerContentSuccesBlock.insertBefore(contentSuccesBlock, null);
	contentSuccesBlock.insertBefore(succesBlock, null);
	containerContentSuccesBlock.id = "containerContentSuccesBlock";
	containerContentSuccesBlock.style.position = "absolute";
	containerContentSuccesBlock.style.width = window.innerWidth;
	containerContentSuccesBlock.style.width = "100%";
	contentSuccesBlock.classList.add("container");
	contentSuccesBlock.id = "contentSuccessBlock";
	contentSuccesBlock.style.margin = "auto";
	succesBlock.id = "successBlock";
	succesBlock.style.margin = "auto";
	succesBlock.style.backgroundColor = "rgba(40, 35, 23, 0.75)" ;
	succesBlock.classList.add("row");
	succesBlock.style.borderCollapse = "separate";
	succesBlock.style.textAlign = "center";
	succesBlock.style.padding = "4%"
	succesBlock.style.width = "70%";
	containerContentSuccesBlock.style.zIndex = "1000";
	titlePup(succesBlock, null, "Success");
	console.log(listeAchievement)
	for (const achievement of listeAchievement) {
		console.log("create case : " + achievement["title"])
		casePup(succesBlock, null, achievement["title"], achievement["img"], achievement["description"], achievement["grade"])
		// if (index === 4)
		// {
		// 	casePup(succesBlock,
		// 		null,
		// 		"ERR://23¤Y%/ ",
		// 		"https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/1/14/Unknown_artifact_icon.png/revision/latest/scale-to-width-down/250?cb=20180519140040",
		// 		"You don't have the achievement",
		// 		2);
		// }
		// else 
		// {
		// 	casePup(succesBlock,
		// 		null,
		// 		"ERR://23¤Y%/ ",
		// 		"https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/1/14/Unknown_artifact_icon.png/revision/latest/scale-to-width-down/250?cb=20180519140040",
		// 		"You don't have the achievement",
		// 		-1);
		// }

	}
}

function titlePup(content, before, title)
{
	const container = document.createElement("div");
	const boscoLeft = document.createElement("img");
	const titleImg = document.createElement("img");
	const boscoRight = document.createElement("img");
	const titlePop = document.createElement("div");
	const separator = document.createElement("div");
	titleImg.style.width = "100%";
	if (title === "Success")
		titleImg.src = "/static/image/other/Icon_Forge_Mastery_achievement.webp";
	if (title === "Stats")
		titleImg.src = "/static/image/other/Statistique_title.png";
	titlePop.style.display = "inline-block";
	titlePop.style.width = "50%";
	titlePop.style.marginLeft = "1%";
	titlePop.style.marginRight = "1%";
	boscoLeft.style.display = "inline-block";
	boscoLeft.src = "/static/image/other/bosco_taunt.gif";
	boscoLeft.style.width = "24%";
	boscoRight.style.display = "inline-block";
	boscoRight.style.width = "24%";
	boscoRight.src = "/static/image/other/bosco_taunt.gif";
	separator.style.marginBottom = "20px";
	container.classList.add("col-md-8");
	container.classList.add("col-lg-6");
	container.classList.add("col-xl-4");
	container.style.margin = "auto";
	container.style.zIndex = "1";
	content.insertBefore(container, before);
	container.insertBefore(boscoLeft, before);
	titlePop.insertBefore(titleImg, null);
	container.insertBefore(titlePop, before);
	container.insertBefore(boscoRight, before);
	content.insertBefore(separator, before);
	
}


function createStats()
{
	console.log("create stats panel");
	const body = document.getElementById("body");
	const containerContentSuccesBlock = document.createElement("div");
	const contentSuccesBlock = document.createElement("div");
	const succesBlock = document.createElement("div");
	const gameDiv = document.getElementById("content");
	body.insertBefore(containerContentSuccesBlock, gameDiv);
	containerContentSuccesBlock.insertBefore(contentSuccesBlock, null);
	contentSuccesBlock.insertBefore(succesBlock, null);
	containerContentSuccesBlock.id = "containerContentSuccesBlock";
	containerContentSuccesBlock.style.position = "absolute";
	containerContentSuccesBlock.style.width = window.innerWidth;
	containerContentSuccesBlock.style.width = "100%";
	contentSuccesBlock.classList.add("container");
	contentSuccesBlock.id = "contentSuccessBlock";
	contentSuccesBlock.style.margin = "auto";
	succesBlock.id = "successBlock";
	succesBlock.style.margin = "auto";
	succesBlock.style.backgroundColor = "rgba(40, 35, 23, 0.75)" ;
	succesBlock.classList.add("row");
	succesBlock.style.borderCollapse = "separate";
	succesBlock.style.textAlign = "center";
	succesBlock.style.padding = "4%"
	succesBlock.style.width = "70%";
	containerContentSuccesBlock.style.zIndex = "1000";
	titlePup(succesBlock, null, "Stats");
	for (let index = 0; index < 9; index++)
	{
			casePup(succesBlock,
				null,
				"Stats Name",
				"https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/1/14/Unknown_artifact_icon.png/revision/latest/scale-to-width-down/250?cb=20180519140040",
				"Stats description",
				-1);
	}
}

function createpupself(type)
{
	if (popOpened)
		return ;
	popOpened = true;
	document.getElementById("Page").classList.add("blur");
	//remove_pop();
	if (type === "sucess")
	{
		const form = document.getElementById('data-request-achievement');
		const data = new FormData(form);
		fetch("https://" + window.location.hostname + ":4200/getselfachievement",
		{
			method: 'POST',
			body: data,
			cache: "default"
		})
				.then(response => response.json())
				.then (jsonData => {
					console.log("received from getselfachievement : ")
					console.log(jsonData)
					if (! jsonData["success"])
					{
						console.error(jsonData["content"])
						return ;
					}
					createSuccess(jsonData["listeAchievement"])
				})
				.catch(error => {
					console.log("erreur from getselfachievement : ")
					console.error(error)
				})
	}
	if (type === "stats")
	{
		createStats()
	}
	setTimeout(function(){
		const body = document.getElementById("body");
		body.onclick = remove_pop;
	}, 10);
}

function createPass()
{
	console.log("create success panel");
	const body = document.getElementById("body");
	const containerContentSuccesBlock = document.createElement("div");
	const contentSuccesBlock = document.createElement("div");
	const succesBlock = document.createElement("div");
	const gameDiv = document.getElementById("content");
	body.insertBefore(containerContentSuccesBlock, gameDiv);
	containerContentSuccesBlock.insertBefore(contentSuccesBlock, null);
	contentSuccesBlock.insertBefore(succesBlock, null);
	containerContentSuccesBlock.id = "containerContentSuccesBlock";
	containerContentSuccesBlock.style.position = "absolute";
	containerContentSuccesBlock.style.width = window.innerWidth;
	containerContentSuccesBlock.style.width = "100%";
	contentSuccesBlock.classList.add("container");
	contentSuccesBlock.id = "contentSuccessBlock";
	contentSuccesBlock.style.margin = "auto";
	succesBlock.id = "successBlock";
	succesBlock.style.margin = "auto";
	succesBlock.style.backgroundColor = "rgba(40, 35, 23, 1)" ;
	succesBlock.classList.add("row");
	succesBlock.style.borderCollapse = "separate";
	succesBlock.style.textAlign = "center";
	succesBlock.style.padding = "4%"
	succesBlock.style.width = "70%";
	containerContentSuccesBlock.style.zIndex = "1000";
	succesBlock.innerHTML = '<form id="form_newPass" method="post">\
	<p id="passPopCurrent">Current password <input type="password" id="currentPass" name="currentPass" required></p><br>\
	<p id="passPopNew">New password <input type="password" id="newPass" name="newPass" required></p><br>\
	<p id="passPopConfirm">Confirm new password <input type="password" id="newPassConfirm" name="newPassConfirm" required></p><br>\
	<button type="submit" class ="btn-drg" id="btnNewPass">Change Password</button>\
	</form>\
	<p id="errorPopPassword" style="color:red;"></p>\
	<br><br><br><br><br><br><br><br><br><br><br>\
	<button class ="btn-drg" style="width:15%; margin:auto;" id="btnQuitPop" onclick="remove_pop()">Go Back</button>';
	const form = document.getElementById('form_newPass');
					form.addEventListener('submit', async event => {
					event.preventDefault();

					const data = new FormData(form);
					changePassword(data)
				});
}

function createName()
{
	console.log("create success panel");
	const body = document.getElementById("body");
	const containerContentSuccesBlock = document.createElement("div");
	const contentSuccesBlock = document.createElement("div");
	const succesBlock = document.createElement("div");
	const gameDiv = document.getElementById("content");
	body.insertBefore(containerContentSuccesBlock, gameDiv);
	containerContentSuccesBlock.insertBefore(contentSuccesBlock, null);
	contentSuccesBlock.insertBefore(succesBlock, null);
	containerContentSuccesBlock.id = "containerContentSuccesBlock";
	containerContentSuccesBlock.style.position = "absolute";
	containerContentSuccesBlock.style.width = window.innerWidth;
	containerContentSuccesBlock.style.width = "100%";
	contentSuccesBlock.classList.add("container");
	contentSuccesBlock.id = "contentSuccessBlock";
	contentSuccesBlock.style.margin = "auto";
	succesBlock.id = "successBlock";
	succesBlock.style.margin = "auto";
	succesBlock.classList.add("row");
	succesBlock.style.borderCollapse = "separate";
	succesBlock.style.textAlign = "center";
	succesBlock.style.padding = "4%"
	succesBlock.style.width = "70%";
	containerContentSuccesBlock.style.zIndex = "1000";


	succesBlock.style.backgroundImage="url(/static/image/background/ecran.png)";
	succesBlock.style.backgroundAttachment= "fixed";
	succesBlock.style.backgroundRepeat="no-repeat";
	succesBlock.style.backgroundSize="contain";

	succesBlock.innerHTML = '<form id="form_newName" method="post">\
	<p id="passPopNew">New Username <input type="text" id="newName" name="newName" required></p><br>\
	<button type="submit" class ="btn-drg" id="btnNewName">Change Username</button>\
	</form>\
	<p id="errorPopUsername" style="color:red;"></p>\
	<br><br><br><br><br><br><br><br><br><br><br>\
	<button class ="btn-drg" style="width:15%; margin:auto;" id="btnQuitPop" onclick="remove_pop()">Go Back</button>';
	const form = document.getElementById('form_newName');
					form.addEventListener('submit', async event => {
					event.preventDefault();

					const data = new FormData(form);
					changeUsername(data)
				});
}


function createpup(type)
{
	//remove_pop();
	if (popOpened)
		return ;
	popOpened = true;
	document.getElementById("Page").classList.add("blur");
	if (type === "sucess")
	{
		const form = document.getElementById('data-request-relation');
		const data = new FormData(form);
	
		fetch("https://" + window.location.hostname + ":4200/getotherachievement",
		{
			method: 'POST',
			body: data,
			cache: "default"
		})
				.then(response => response.json())
				.then (jsonData => {
					console.log("received from getotherachievement : ")
					console.log(jsonData)
					if (! jsonData["success"])
					{
						console.error(jsonData["content"])
						return ;
					}
					createSuccess(jsonData["listeAchievement"])
				})
				.catch(error => {
					console.log("erreur from getotherachievement : ")
					console.error(error)
				})
	}
	if (type === "stats")
	{
		createStats()
	}
	if (type === "pass")
	{
		createPass()
		return
	}
	if (type === "name")
    {
        createName()
        return
    }
	setTimeout(function(){
		const body = document.getElementById("body");
		body.onclick = remove_pop;
	}, 10);
}
  