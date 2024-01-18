/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   request_achievement.js                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: lflandri <lflandri@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2024/01/17 15:42:07 by lflandri          #+#    #+#             */
/*   Updated: 2024/01/18 17:38:00 by lflandri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

function boscoClick()
{
	document.getElementById("input-form-head-achievement").value = "boscoFriend";
			const form = document.getElementById('data-request-achievement');
			const data = new FormData(form);

			fetch("https://" + window.location.hostname + ":4200/setachievement",
			{
				method: 'POST',
				body: data,
				cache: "default"
			})
					.then(response => response.json())
					.then (jsonData => {
						console.log("received from setachievement : ")
						console.log(jsonData)
						if (! jsonData["success"])
						{
							console.error(jsonData["content"])
							return ;
						}
						document.getElementById("bosco-achievement-img").remove();
						

					})
					.catch(error => {
						console.log("erreur from setachievement : ")
						console.error(error)
					})
}

function addBosco() {
	try
	{
		if (getRandomInt(100) < 1)
		{
		let navbar = document.getElementById("header");
		let boscocheck = document.getElementById("bosco-pop-balise");
		let bosco = document.createElement("img");
		bosco.style.position = "absolute";
		bosco.style.left = "70%";
		bosco.style.top = "10px";
		bosco.id = "bosco-achievement-img"
		bosco.style.display = "block";
		bosco.style.width = "60px";
		bosco.src = "/static/image/achievement/bosco_move.gif";
		navbar.insertBefore(bosco, boscocheck);
		bosco.onclick = boscoClick;
		}


	} catch (error) {
		console.error(error)
	}

}