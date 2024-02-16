/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   match_history_creator.js                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: lflandri <liam.flandrinck.58@gmail.com>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2023/11/23 15:10:25 by lflandri          #+#    #+#             */
/*   Updated: 2024/02/16 04:48:01 by lflandri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

//TODO link to db

const Match_list =
[
	{
		"playerR1" :
		{
			"name" : "Enginer",
			"pp" : "https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/4/46/Engineer_portrait.png/revision/latest/scale-to-width-down/35?cb=20180519150041",
			"goalList":
			[
				{"time" : 0.50, "bounce" : 0, "speed": 0.15},
				{"time" : 1.5, "bounce" : 1, "speed": 0.15},
				{"time" : 2.35689, "bounce" : 15, "speed": 0.15},
				{"time" : 4.50, "bounce" : 6, "speed": 0.15},
				{"time" : 4.70, "bounce" : 999, "speed": 10},  
				{"time" : 6.56, "bounce" : 2, "speed": 0.15},
				{"time" : 7, "bounce" : 3, "speed": 0.15},
				{"time" : 9, "bounce" : 6, "speed": 1},
				{"time" : 12, "bounce" : 8, "speed": 0.15},
				{"time" : 13, "bounce" : 5, "speed": 0.15},
				{"time" : 18.95, "bounce" : 3, "speed": 0.15}
			]
		},
		"playerL1" :
		{
			"name" : "Gunner",
			"pp" : "https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/c/c2/Gunner_portrait.png/revision/latest/scale-to-width-down/35?cb=20180519150058",
			"goalList":
			[
				{"time" : 1, "bounce" : 1, "speed": 0.15},
				{"time" : 2, "bounce" : 2, "speed": 55} ,
				{"time" : 3, "bounce" : 5, "speed": 0.15} ,
				{"time" : 4, "bounce" : 4, "speed": 65} ,
				{"time" : 5.5, "bounce" : 8, "speed": 0.15},
				{"time" : 6.01, "bounce" : 4, "speed": 0.15},
				{"time" : 8, "bounce" : 9, "speed": 89},
				{"time" : 10, "bounce" : 7, "speed": 0.15},
				{"time" : 11, "bounce" : 5, "speed": 0.15},
				{"time" : 15.26, "bounce" : 602, "speed": 3840}
			]
		},
		"map" : "Classic",
		"power_up" : true
	},
	{
		"playerR1" :
		{
			"name" : "Enginer",
			"pp" : "https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/4/46/Engineer_portrait.png/revision/latest/scale-to-width-down/35?cb=20180519150041",
			"goalList":
			[
				{"time" : 0.50, "bounce" : 0, "speed": 0.15},
				{"time" : 1.5, "bounce" : 1, "speed": 0.15},
			]
		},
		"playerL1" :
		{
			"name" : "Gunner",
			"pp" : "https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/c/c2/Gunner_portrait.png/revision/latest/scale-to-width-down/35?cb=20180519150058",
			"goalList":
			[
				{"time" : 1, "bounce" : 1, "speed": 0.15},
				{"time" : 2, "bounce" : 2, "speed": 55} ,
				{"time" : 2.055555, "bounce" : 2, "speed": 55} ,
			]
		},
		"map" : "Classic",
		"power_up" : false
	},
	{
		"playerR1" :
		{
			"name" : "Enginer",
			"pp" : "https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/4/46/Engineer_portrait.png/revision/latest/scale-to-width-down/35?cb=20180519150041",
			"goalList":
			[
				{"time" : 0.750, "bounce" : 6, "speed": 0.15},
				{"time" : 1.5, "bounce" : 1, "speed": 0.15},
				{"time" : 6.9, "bounce" : 6, "speed": 0.15},
				{"time" : 7.5, "bounce" : 1, "speed": 0.15}
			]
		},
		"playerL1" :
		{
			"name" : "Gunner",
			"pp" : "https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/c/c2/Gunner_portrait.png/revision/latest/scale-to-width-down/35?cb=20180519150058",
			"goalList":
			[
				{"time" : 1, "bounce" : 1, "speed": 0.15},
				{"time" : 1.75, "bounce" : 2, "speed": 55} ,
				{"time" : 2.055555, "bounce" : 2, "speed": 55} 
				
			]
		},
		"map" : "Classic",
		"power_up" : false
	}
];

function hideGraphic(id)
{
	if (!popOpened)
		return ;
	popOpened = false;
	document.getElementById("Page").classList.remove("blur");
	document.getElementById(id).style.display = "none";
	const body = document.getElementById("body");
	body.onclick = null;
	}

function showGraphic(id)
{
	if (popOpened)
		return ;
	popOpened = true;
	document.getElementById("Page").classList.add("blur");
	document.getElementById(id).style.display = "block";
	setTimeout(function(){
		const body = document.getElementById("body");
		body.onclick = function(){ hideGraphic(id) }; //"hideGraphic("+id+")";
	}, 10);
}

function createPoints(svgBlock,content, color, list, maxx, maxy)
{
	let newPath = document.createElementNS('http://www.w3.org/2000/svg', 'path');
	newPath.style.stroke = color;

	content.insertBefore(newPath, null);
	let d = "M 0 300 ";
	if (0 < list.length)
	{
		d +=  " L " + (list[0]["time"] * 800 / maxx) + " " + (300 - (300 / maxy)) +" ";
		newPath.setAttribute('d', d);
	}
	else
		return ;

	for (let index = 0; index < list.length ; index++)
	{
		let newPoint = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
		let newPath = document.createElementNS('http://www.w3.org/2000/svg', 'path');
		let newInfo = document.createElementNS('http://www.w3.org/2000/svg', 'path');
		let	newDiv = document.createElementNS('http://www.w3.org/2000/svg', 'g');
		let newText1 = document.createElementNS('http://www.w3.org/2000/svg', 'text');
		let newText2 = document.createElementNS('http://www.w3.org/2000/svg', 'text');
		//newPath.setAttribute('fill', color);
		let di = "M" + (list[index ]["time"] * 800 / maxx) + " " + ( 300 - ((index + 1) * 300 / maxy)) + " l -5 -7 h -20 v -30 h 50 v 30 h -20 l -5 7 Z";
		//let di = "M" + 0 + " " + 0 + " L 0 50 L 50 50 Z";
		newInfo.setAttribute('d', di);
		newInfo.setAttribute('fill', color);
		let d = "M" + (list[index ]["time"] * 800 / maxx) + " " + ( 300 - ((index + 1) * 300 / maxy));
		newPoint.setAttribute('cx', "" + (list[index ]["time"] * 800 / maxx));
		newPoint.setAttribute('cy', "" + ( 300 - ((index + 1) * 300 / maxy)));
		newPoint.setAttribute('r', "5");
		newPoint.setAttribute('fill', color);
		newDiv.classList.add("goal_point")

		if (index + 1 < list.length)
		{
			d +=  " L " + (list[index + 1]["time"] * 800 / maxx) + " " + (300 - ((index + 2) * 300 / maxy)) +" ";
		}
		else
		{
			d +=  " L " + 800 + " " + (300 - ((index + 1) * 300 / maxy)) +" ";
		}
			newInfo.style.stroke = "#000000";
		newPath.style.stroke = color;
		newText1.setAttribute('x', "" + (list[index ]["time"] * 800 / maxx) - 24);
		newText1.setAttribute('y', "" + ( 300 - ((index + 1) * 300 / maxy)) - 27);
		newText1.setAttribute('fill', "black");
		newText1.textContent = "bounce : " + list[index ]["bounce"];
		newText1.style.fontSize = "0.50em";
		newText2.setAttribute('x', "" + (list[index ]["time"] * 800 / maxx) - 24);
		newText2.setAttribute('y', "" + ( 300 - ((index + 1) * 300 / maxy)) - 17);
		newText2.setAttribute('fill', "black");
		newText2.textContent = "speed : " + list[index ]["speed"];
		newText2.style.fontSize = "0.50em";
		newPath.setAttribute('d', d);
		content.insertBefore(newPath, null);
		svgBlock.insertBefore(newDiv, null)
		newDiv.insertBefore(newPoint, null);
		newDiv.insertBefore(newInfo, null);
		newDiv.insertBefore(newText1, null);
		newDiv.insertBefore(newText2, null);
	}
}

function createNumberGrahic(content, maxx, maxy)
{
for (let index = 1; index < maxx; index++)
{
let newPath = document.createElementNS('http://www.w3.org/2000/svg', 'path');
let d = "M" + (index * 800 / maxx) +" 300 ";
d +=  " L " + (index * 800 / maxx) + " 0 ";
newPath.style.stroke = "black";
newPath.style.strokeWidth = "0.5px";
newPath.setAttribute('d', d);
content.insertBefore(newPath, null);

let newPoint = document.createElementNS('http://www.w3.org/2000/svg', 'text');
newPoint.setAttribute('x', "" + (index * 800 / maxx));
newPoint.setAttribute('y', "" + 295);
newPoint.setAttribute('fill', "black");
newPoint.textContent = "" + index + " min";
newPoint.style.fontSize = "0.75em";
content.insertBefore(newPoint, null);
}
for (let index = 1; index < maxy; index++)
{
let newPath = document.createElementNS('http://www.w3.org/2000/svg', 'path');
let d = "M0 " + (300 - (index * 300 / maxy));
d +=  " L 800 " + (300 - (index * 300 / maxy));
newPath.style.stroke = "black";
newPath.style.strokeWidth = "0.5px";
newPath.setAttribute('d', d);
content.insertBefore(newPath, null);

let newPoint = document.createElementNS('http://www.w3.org/2000/svg', 'text');
newPoint.setAttribute('x', "0");
newPoint.setAttribute('y', "" + (300 - (index * 300 / maxy)));
newPoint.setAttribute('fill', "black");
newPoint.textContent = "" + index;
newPoint.style.fontSize = "0.75em";
content.insertBefore(newPoint, null);	
}
}

function createGraphic(svgBlock, content, match, duration)
{
// let indJ1 = 0;
// let indJ2 = 0;
//list_j1.sort()
//list_j2.sort()
// let maxx = list_j1[list_j1.length - 1]["time"] > list_j2[list_j2.length - 1]["time"] ? list_j1[list_j1.length - 1]["time"] : list_j2[list_j2.length - 1]["time"];
// let maxy = list_j1.length > list_j2.length ? list_j1.length : list_j2.length
let maxx = duration
let maxy = 11
// console.log(list_j1);
// console.log(maxx);
// console.log(maxy);
maxx += 0.75;
maxy += 2;
 
createNumberGrahic(content, maxx, maxy);
createPoints(svgBlock, content, "#FF0000", match["playerR1"]["goalList"], maxx, maxy);
createPoints(svgBlock, content, "#0000FF", match["playerL1"]["goalList"], maxx, maxy);
if (match["playerL2"] != undefined)
{
	createPoints(svgBlock, content, "#AA0000", match["playerL2"]["goalList"], maxx, maxy);
}
if (match["playerR2"] != undefined)
{
	createPoints(svgBlock, content, "#0000AA", match["playerR2"]["goalList"], maxx, maxy);
}

}


function  createHistory(listMatch)
{
	let matchHistory = document.getElementById("match_history");
	for (let index = 0; index < listMatch.length; index++) {
		const match = listMatch[index];
		let scoreP1 = match["playerR1"]["goalList"].length;
		let scoreP2 = match["playerL1"]["goalList"].length;
		if (match["playerR2"] != undefined && match["playerR2"]["name"] != match["playerR1"]["name"] )
			scoreP1+=match["playerR2"]["goalList"].length
		if (match["playerL2"] != undefined && match["playerL2"]["name"] != match["playerL1"]["name"])
			scoreP2+=match["playerL2"]["goalList"].length
		let matchDiv = document.createElement('tr');
		let playerDiv = document.createElement('td');
		let infoDiv = document.createElement('td');
		let P1content = document.createElement('div');
		let P2content = document.createElement('div');
		let score = document.createElement('h5');
		let result = document.createElement('h4');
		let P1name = document.createElement('h5');
		let P3name = document.createElement('h5');
		let P2name = document.createElement('h5');
		let P4name = document.createElement('h5');
		let P1img = document.createElement('img');
		let P3img = document.createElement('img');
		let P2img = document.createElement('img');
		let P4img = document.createElement('img');
		let mapType = document.createElement('h5');
		let PowerUpTxt = document.createElement('h5');
		let PowerUpBool = document.createElement('span');
		let graphe = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
		let ingraphe = document.createElementNS('http://www.w3.org/2000/svg', 'g');
		matchDiv.style.clear = "both";
		infoDiv.style.width = "18%";
		infoDiv.classList.add("black_grey_div");
		// infoDiv.style.backgroundColor = "rgba(40, 35, 23, 0.75)";
		//infoDiv.style.width = "100%";
		playerDiv.classList.add("black_grey_div");
		// playerDiv.style.backgroundColor = "rgba(40, 35, 23, 0.75)";
		playerDiv.style.textAlign = "center";
		playerDiv.style.width = "80%";
		P1content.style.display = "inline-block";
		P2content.style.display = "inline-block";
		P1content.style.verticalAlign = "middle";
		P2content.style.verticalAlign = "middle";
		P1content.style.width = "38%";
		P2content.style.width = "38%";
		score.textContent = "" + scoreP1 + " VS " + scoreP2;
		score.style.display = "inline-block";
		score.style.width = "20%";
		score.style.color = "white";
		score.style.marginRight = "2%";
		score.style.marginLeft = "2%";
		score.style.textAlign = "center";
		result.style.textAlign = "center";
		if (scoreP1 > scoreP2)
		{
			result.textContent = "WIN";
			result.style.color = "green";
		} 
		else
		{
			result.textContent = "LOSE";
			result.style.color = "red";
		}
		P1name.textContent = match["playerR1"]["name"];
		if (match["playerR2"] != undefined)
		{
			P3name.textContent = match["playerR2"]["name"];
			P3img.src = match["playerR2"]["pp"];
		}
		P2name.textContent = match["playerL1"]["name"];
		if (match["playerL2"] != undefined)
		{
			P4name.textContent = match["playerL2"]["name"];
			P4img.src = match["playerL2"]["pp"];
		}
		P1name.style.color = "white";
		P3name.style.color = "white";
		P1name.style.width = "75%";
		P3name.style.width = "75%";
		P1name.style.display = "inline-block";
		P3name.style.display = "inline-block";
		P2name.style.display = "inline-block";
		P4name.style.display = "inline-block";
		P2name.style.width = "75%";
		P4name.style.width = "75%";
		P2name.style.color = "white";
		P4name.style.color = "white";
		P1name.style.fontSize = "200%";
		P3name.style.fontSize = "200%";
		P1name.style.marginTop = "0%";
		P3name.style.marginTop = "0%";
		P1name.style.marginBottom = "0%";
		P3name.style.marginBottom = "0%";
		P1name.style.textAlign = "left"
		P3name.style.textAlign = "left"
		P2name.style.fontSize = "200%";
		P4name.style.fontSize = "200%";
		P2name.style.marginTop = "0%";
		P4name.style.marginTop = "0%";
		P2name.style.marginBottom = "0%";
		P4name.style.marginBottom = "0%";
		P2name.style.textAlign = "right";
		P4name.style.textAlign = "right";
		P1name.style.verticalAlign = "middle";
		P3name.style.verticalAlign = "middle";
		P2name.style.verticalAlign = "middle";
		P4name.style.verticalAlign = "middle";
		P1img.style.verticalAlign = "middle";
		P3img.style.verticalAlign = "middle";
		P2img.style.verticalAlign = "middle";
		P4img.style.verticalAlign = "middle";
		P1img.src = match["playerR1"]["pp"];	
		P2img.src = match["playerL1"]["pp"];
		P1img.style.width = "25%";
		P3img.style.width = "25%";
		P2img.style.width = "25%";
		P4img.style.width = "25%";
		P1img.style.display = "inline-block";
		P3img.style.display = "inline-block";
		P2img.style.display = "inline-block";
		P4img.style.display = "inline-block";
		mapType.textContent = "Map : " + match["map"];
		mapType.style.color = "white";
		mapType.style.padding = "3%";
		PowerUpTxt.style.padding = "3%";
		PowerUpTxt.style.color = "white";
		PowerUpTxt.textContent = "Power Up : ";
		if (match["powerUp"])
		{
			PowerUpBool.textContent = "ON";
			PowerUpBool.style.color = "green";
		} 
		else
		{
			PowerUpBool.textContent = "OFF";
			PowerUpBool.style.color = "red";
		}
		matchHistory.insertBefore(matchDiv, null);
		matchDiv.insertBefore(playerDiv, null);
		matchDiv.insertBefore(infoDiv, null);
		playerDiv.insertBefore(result, null);
		playerDiv.insertBefore(P1content, null);
		playerDiv.insertBefore(score, null);
		playerDiv.insertBefore(P2content, null);
		P1content.insertBefore(P1img, null);
		P1content.insertBefore(P1name, null);
		if (match["playerR2"] != undefined)
		{
			P1content.insertBefore(P3img, null);
			P1content.insertBefore(P3name, null);
		}
		P2content.insertBefore(P2name, null);
		P2content.insertBefore(P2img, null);
		if (match["playerL2"] != undefined)
		{
			P2content.insertBefore(P4name, null);
			P2content.insertBefore(P4img, null);
		}
		infoDiv.insertBefore(mapType, null);
		infoDiv.insertBefore(PowerUpTxt, null);
		PowerUpTxt.insertBefore(PowerUpBool, null);

		graphe.setAttribute("viewBox", "0, 0, 800, 300");
		graphe.style.borderLeft = "solid black 1px";
		graphe.style.borderBottom = "solid black 1px";
		graphe.style.position = "absolute";
		graphe.style.left = "25%";
		graphe.style.top = "200px";
		graphe.style.width = "50%";
		graphe.style.backgroundColor = "rgba(40, 35, 23, 0.75)";
		//graphe.classList.add("goalGraph")
		graphe.id = "grapheMatch" + index
		document.getElementById("body").insertBefore(graphe, null);
		// matchDiv.insertBefore(graphe, null);
		ingraphe.style.fill = "none";
		graphe.style.display = "none";
		ingraphe.strokeWidth = "4px";
		graphe.insertBefore(ingraphe, null);
		// graphe.style.filter = "blur(0px)";
		// graphe.style.webkitFilter = "blur(0px)";
		matchDiv.onclick = function(){ showGraphic(graphe.id) } ;
		createGraphic(graphe, ingraphe,  match, match["duration"]);
	}

}
// createHistory(Match_list);

function getMatchHistory() {
	const formmatchHistory = document.getElementById('data-request-relation');
	const data = new FormData(formmatchHistory);
	
	fetch("https://" + window.location.hostname + ":4200/getusermatchhistory",
	{
		method: 'POST',
		body: data,
		cache: "default"
	})
			.then(response => response.json())
			.then (jsonData => {
				console.log("received from getusermatchhistory : ")
				console.log(jsonData)
				if (! jsonData["success"])
				{
					console.error(jsonData["content"])
					return ;
				}
				createHistory(jsonData["content"])
			})
			.catch(error => {
				console.log("erreur from getusermatchhistory : ")
				console.error(error)
			})
}
getMatchHistory()