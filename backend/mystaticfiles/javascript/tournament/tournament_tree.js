/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   tournament_tree.js                                 :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: lflandri <lflandri@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2023/12/07 14:56:17 by lflandri          #+#    #+#             */
/*   Updated: 2023/12/07 16:53:06 by lflandri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

let graphe = document.getElementById("graphe");


const playerList = [
					{
						"grade":0,
						"img": "https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/c/c5/Mining_expedition_icon.png/revision/latest/scale-to-width-down/40?cb=20220313105613"
					},
					{
						"grade":1,
						"img": "https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/8/89/Unknown_lightgray.png/revision/latest/scale-to-width-down/250?cb=20210416205542"
					},
					{
						"grade":3,
						"img": "https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/8/89/Unknown_lightgray.png/revision/latest/scale-to-width-down/250?cb=20210416205542"
					},
					{
						"grade":0,
						"img": "https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/8/89/Unknown_lightgray.png/revision/latest/scale-to-width-down/250?cb=20210416205542"
					},
					{
						"grade":1,
						"img": "https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/8/89/Unknown_lightgray.png/revision/latest/scale-to-width-down/250?cb=20210416205542"
					},
					{
						"grade":0,
						"img": "https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/8/89/Unknown_lightgray.png/revision/latest/scale-to-width-down/250?cb=20210416205542"
					},
					{
						"grade":0,
						"img": "https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/8/89/Unknown_lightgray.png/revision/latest/scale-to-width-down/250?cb=20210416205542"
					},
					{
						"grade":2,
						"img": "https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/8/89/Unknown_lightgray.png/revision/latest/scale-to-width-down/250?cb=20210416205542"
					},
					// {
					// 	"grade":0,
					// 	"img": "https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/8/89/Unknown_lightgray.png/revision/latest/scale-to-width-down/250?cb=20210416205542"
					// },


				]

function drawTree(content, mapPoint)
{
	for (let floor = 0; floor < mapPoint.length - 1; floor++)
	{
		console.log(mapPoint[floor]);
		for (let index = 0; index < mapPoint[floor + 1].length; index+=2)
		{
			let newPath1 = document.createElementNS('http://www.w3.org/2000/svg', 'path');
			let d1 = "M" + mapPoint[floor][index / 2] + " " + ((floor) * 300 / (mapPoint.length + 1));
			d1 +=  " V " + ((floor + 1) * 300 / (mapPoint.length + 1));
			d1 +=  " H " + mapPoint[floor + 1][index];
			newPath1.style.stroke = "white";
			newPath1.style.strokeWidth = "2px";
			console.log(mapPoint[floor][index / 2]);
			newPath1.setAttribute('d', d1);
			content.insertBefore(newPath1, null);
			
			let newPath2 = document.createElementNS('http://www.w3.org/2000/svg', 'path');
			let d2 = "M" + mapPoint[floor][index / 2] + " " + ((floor) * 300 / (mapPoint.length + 1));
			d2 +=  " V " + ((floor + 1) * 300 / (mapPoint.length + 1));
			d2 +=  " H " + mapPoint[floor + 1][index + 1];
			newPath2.style.stroke = "white";
			newPath2.style.strokeWidth = "2px";
			newPath2.setAttribute('d', d2);
			content.insertBefore(newPath2, null);

		}
		
	}
	for (let index = 0; index < mapPoint[mapPoint.length - 1].length; index+=2)
	{
			let newPath1 = document.createElementNS('http://www.w3.org/2000/svg', 'path');
			let d1 = "M" + mapPoint[mapPoint.length - 1][index] + " " + ((mapPoint.length - 1) * 300 / (mapPoint.length + 1));
			d1 +=  " V " + ((mapPoint.length) * 300 / (mapPoint.length + 1));
			newPath1.style.stroke = "white";
			newPath1.style.strokeWidth = "2px";
			console.log(mapPoint[mapPoint.length - 1][index]);
			newPath1.setAttribute('d', d1);
			content.insertBefore(newPath1, null);
			
			let newPath2 = document.createElementNS('http://www.w3.org/2000/svg', 'path');
			let d2 = "M" + mapPoint[mapPoint.length - 1][index + 1] + " " + ((mapPoint.length - 1) * 300 / (mapPoint.length + 1));
			d2 +=  " V " + ((mapPoint.length) * 300 / (mapPoint.length + 1));
			newPath2.style.stroke = "white";
			newPath2.style.strokeWidth = "2px";
			newPath2.setAttribute('d', d2);
			content.insertBefore(newPath2, null);

	}
}

function addPlayerTournamentTree(content, mapPoint, listPlayer, nb_player_max)
{
	for (let index = 0; index < listPlayer.length; index++) {
		const element = listPlayer[index];
		let grade = mapPoint.length - 1 - element["grade"];

		console.log("grade : " + grade);
		let mod = 2**(element["grade"]);
		if (mod === 0)
		{
			mod++;
		}
		console.log("mod :" + mod);
		console.log("index :" + index);

		let newPoint = document.createElementNS('http://www.w3.org/2000/svg', 'image');
		if (grade === 0)
		{
			newPoint.setAttribute('y', "" + ((grade) * 300 / (mapPoint.length + 1)));
		}
		else if (grade != mapPoint.length - 1)
		{
			newPoint.setAttribute('y', "" + ((grade) * 300 / (mapPoint.length + 1) - 15))
		}
		else
		{
			newPoint.setAttribute('y', "" + ((grade + 1) * 300 / (mapPoint.length + 1) - 15));
		}
		newPoint.setAttribute('x', "" + mapPoint[grade][ Math.floor(index / mod)] - 15);
		newPoint.setAttribute('width', "30");
		newPoint.setAttribute('height', "30");
		newPoint.setAttributeNS('http://www.w3.org/1999/xlink','href', listPlayer[index]["img"]);
		content.insertBefore(newPoint, null);
	}
}


function createTournamentTree(content, list)
{
	floorNb = 0;
	nb_player_max = 1;
	listFloor = [];

	while (nb_player_max < list.length)
	{
		nb_player_max+=nb_player_max;
	}
	
	console.log(nb_player_max);

	for (let nb_player = 1; nb_player < nb_player_max + 1 ; nb_player+=nb_player)
	{
		if (nb_player === 1)
		{
			listFloor[floorNb] = [400];
		}
		else
		{
			listPoint = [];
			for (let index = 0; index < nb_player; index+=2)
			{
				listPoint[index] = listFloor[floorNb - 1][index / 2] - ((nb_player_max - (floorNb * floorNb * 0.5)) / floorNb) * 10;
				listPoint[index + 1] = listFloor[floorNb - 1][index / 2] + ((nb_player_max - (floorNb * floorNb * 0.5)) / floorNb) * 10;
			}
			listFloor[floorNb] = listPoint;
		}
		floorNb++;
		
	}
	drawTree(content, listFloor);
	addPlayerTournamentTree(content, listFloor, list, nb_player_max);
}

createTournamentTree(graphe, playerList);