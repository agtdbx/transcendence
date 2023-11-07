/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   game.js                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: lflandri <lflandri@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2023/11/07 13:20:01 by lflandri          #+#    #+#             */
/*   Updated: 2023/11/07 13:23:26 by lflandri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

function remove_pop()
{
	const popup = document.getElementById("contentSuccessBlock");
	console.log("popup : ");
	console.log(popup);
	console.log("\n");
	while (document.getElementById("contentSuccessBlock") != null)
		document.getElementById("contentSuccessBlock").remove();
	const body = document.getElementById("body");
	body.onclick = null;
}

function casePup(content, before, title, img, description, grade)
{
	
	const image = document.createElement("img");
	const container = document.createElement("div");
	const divText = document.createElement("div");
	const titleText = document.createElement("h5");
	const text = document.createElement("p");

	image.style.width = "30%";
	image.style.display = "inline-block";
	image.src = img;

	container.style.marginLeft = "1.5%";
	container.style.marginRight = "1.5%";
	container.style.width = "30%";
	container.style.display = "inline-block";
	container.style.backgroundColor = "#000000";
	container.style.border = "1px solid #FF9C00";
	container.style.marginBottom = "15px";

	divText.style.width = "70%";
	divText.style.position = "relative";
	divText.style.left = "30%";
	divText.style.height = "30px";
	divText.style.marginBottom = "-30px";
	divText.style.fontSize = "1vw";


	titleText.style.color = "white";
	titleText.textContent = title;
	titleText.style.textAlign = "center";
	titleText.style.marginTop = "1px";
	titleText.style.marginBottom = "0px";
	titleText.style.fontSize = "2vw";

	text.style.color = "white";
	text.textContent = description;
	text.style.marginTop = "1px";
	



	content.insertBefore(container, before);
	container.insertBefore(divText, null);
	container.insertBefore(image, null);
	divText.insertBefore(titleText, null);
	divText.insertBefore(text, null);

	if (grade > 0 )
	{
		const gradeContainer = document.createElement("div");
		const gradeImage = document.createElement("img");

		gradeImage.style.height = "30px";
		gradeImage.style.marginBottom = "-30px";
		gradeImage.style.marginTop = "0px";
		gradeImage.style.position = "relative";
		gradeImage.style.left = "40%";
		gradeImage.style.top = "-15px";
		gradeImage.style.width = "20%"
		
		switch (grade) {
			case 1:
				gradeImage.src = "https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/5/5e/Icons_complexity_1.png/revision/latest/scale-to-width-down/60?cb=20190210235110";
				break;
		
			case 2:
				gradeImage.src = "https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/e/e3/Icons_complexity_2.png/revision/latest/scale-to-width-down/60?cb=20190210235125";
				break;
			case 3:
				gradeImage.src = "https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/1/1f/Icons_complexity_3.png/revision/latest/scale-to-width-down/60?cb=20190210235136";
				break;
		}
		container.insertBefore(gradeContainer, null);
		gradeContainer.insertBefore(gradeImage, null);

	}

}


function titlePup(content, before, title)
{
	
	const boscoLeft = document.createElement("img");
	const titleImg = document.createElement("img");
	const boscoRight = document.createElement("img");
	const titlePop = document.createElement("div");
	const titleText = document.createElement("h4");
	const separator = document.createElement("div");

	titleImg.style.width = "100%";
	titleImg.style.marginTop = "-40%";
	titleImg.src = "https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/c/c6/Icon_Forge_Mastery.png/revision/latest/scale-to-width-down/200?cb=20190926110523";
	
	titlePop.style.display = "inline-block";
	titlePop.style.width = "10%";
	titlePop.style.marginLeft = "1%";
	titlePop.style.marginRight = "1%";

	titleText.textContent = title;
	titleText.style.fontSize = "1vw"
	titleText.style.position = "relative";
	titleText.style.left = "25%";
	titleText.style.top = "0%";
	titleText.style.width = "50%";
	titleText.style.paddingTop = "40%";
	titleText.style.textAlign = "center";
	titleText.style.color = "white";
	titleText.style.height = "30px";
	titleText.style.marginBottom = "-30px";
	titleText.style.marginTop = "0px";

	boscoLeft.style.marginLeft = "39%";
	boscoLeft.style.display = "inline-block";
	boscoLeft.src = "https://cdn.discordapp.com/attachments/1166317817595969697/1166332408874946620/bosco_taunt.gif?ex=65535533&is=6540e033&hm=e7e769432fbbe26b8a7630b0e1a49b48d90b56b4df3b5721f4208cf9f3e8b0b4&";
	boscoLeft.style.width = "5%";
	boscoRight.style.display = "inline-block";
	boscoRight.style.width = "5%";
	boscoRight.src = "https://cdn.discordapp.com/attachments/1166317817595969697/1166332408874946620/bosco_taunt.gif?ex=65535533&is=6540e033&hm=e7e769432fbbe26b8a7630b0e1a49b48d90b56b4df3b5721f4208cf9f3e8b0b4&";

	separator.style.marginBottom = "20px";
		/* transformation css
		-webkit-transform:rotate(180deg); //Safari 3.1+/Chrome
		-o-transform:rotate(180deg);  //Opera 10.5+
		-moz-transform: rotate(180deg); //Firefox 3.5+
		*/
	
	content.insertBefore(boscoLeft, before);
	titlePop.insertBefore(titleText, null);
	titlePop.insertBefore(titleImg, null);
	content.insertBefore(titlePop, before);
	content.insertBefore(boscoRight, before);
	content.insertBefore(separator, before);
}


function createSuccess()
{
	//remove_pop();
	console.log("create success panel");
	const body = document.getElementById("body");
	const contentSuccesBlock = document.createElement("div");
	const succesBlock = document.createElement("div");
	const gameDiv = document.getElementById("game_div");

	body.insertBefore(contentSuccesBlock, game_div);
	contentSuccesBlock.insertBefore(succesBlock, null);

	contentSuccesBlock.id = "contentSuccessBlock";
	contentSuccesBlock.style.position = "absolute";
	contentSuccesBlock.style.width = window.innerWidth;
	succesBlock.id = "successBlock";
	succesBlock.style.position = "sticky";
	succesBlock.style.left = "15%";
	succesBlock.style.backgroundColor = "rgba(40, 35, 23, 0.75)" ; /*"#282317"*/
	succesBlock.style.height = "500px";
	succesBlock.style.width = "70%";
	succesBlock.style.zIndex = "1000";
	titlePup(succesBlock, null, "Success");

	for (let index = 0; index < 9; index++) {


		if (index === 4)
		{
			casePup(succesBlock,
				null,
				"ERR://23¤Y%/ ",
				"https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/1/14/Unknown_artifact_icon.png/revision/latest/scale-to-width-down/250?cb=20180519140040",
				"You don't have the success",
				2);
		}
		else 
		{
			casePup(succesBlock,
				null,
				"ERR://23¤Y%/ ",
				"https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/1/14/Unknown_artifact_icon.png/revision/latest/scale-to-width-down/250?cb=20180519140040",
				"You don't have the success",
				-1);
		}

	}
}



/*CODE Ball*/

var x_to_go = 1;
var rotate = 0;
var y_to_go = 1;
var speed = 5;

/*
setTimeout(lol, 5000);
function lol(){
	document.location.href="https://youtu.be/dQw4w9WgXcQ";
};*/

function createBall()
{
	const gameDiv = document.getElementById("game_div");
	const paddle = document.getElementById("paddle");
	const image = document.createElement("img");

	gameDiv.insertBefore(image, paddle);
	image.src = "https://png.pngtree.com/png-clipart/20190705/original/pngtree-3d-beach-ball-png-transparent-background-image-png-image_4360706.jpg";
	image.style.position = "relative";
	image.style.width = "20px";
	image.style.height = "20px";
	image.style.top = "250px";
	image.style.left = "250px";
	image.id = "ball";
	console.log("ball created");

	

};

function addPX(str , nb)
{
	nb = parseInt(str) + nb;
	str = nb + "px";

	return str;
};

function moveBall()
{
	const gameDiv = document.getElementById("game_div");
	const ball = document.getElementById("ball");

	/*image.style.top = "250px";
	image.style.left = "250px";*/
	rotate = (rotate + 6) % 360;
	ball.style.webkitTransform = "rotate(" + rotate+  "deg)";
	var new_y = addPX(ball.style.top, speed * y_to_go);
	var new_x = addPX(ball.style.left, speed * x_to_go);
	if (parseInt(new_y) <= 0)
	{
		y_to_go = 1;
		ball.style.top = "0px";
	}
	else if (parseInt(addPX(new_y, 20)) >= parseInt(gameDiv.style.height))
	{
		y_to_go = -1;
		ball.style.top = addPX(gameDiv.style.height, -20);
	}
	else
		ball.style.top = new_y;
	if (parseInt(addPX(new_x, 20)) >= parseInt(gameDiv.style.width))
	{
		x_to_go = -1;
		ball.style.left = addPX(gameDiv.style.width, -20);
	}
	else if (parseInt(new_x) <= 0)
	{
		x_to_go = 1;
		ball.style.left = "0px";
	}
	else
		ball.style.left = new_x;
	//speed += 0.1;

	// console.log("Mouvement :   ");
	// console.log(ball.style.top);
	// console.log(ball.style.left);
	// console.log("   ");

};

function createpup(type)
{
	//remove_pop();
	if (type === "sucess")
	{
		createSuccess()
	}
	setTimeout(function(){
		const body = document.getElementById("body");
		body.onclick = remove_pop;
	}, 500);
	
	//console.log(body.onclick);

}

createBall();
//createSuccess();
setInterval(moveBall, 20);
document.addEventListener("keypress", function(event)
	{
		const paddle = document.getElementById("paddle");
		   if (event.code === 'KeyS')
		{
			paddle.style.top = addPX(paddle.style.top, 5)
		}
		else if (event.code === 'KeyW')
		{
			paddle.style.top = addPX(paddle.style.top, -5)
		}
	});

  