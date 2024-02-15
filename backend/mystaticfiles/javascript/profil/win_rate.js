/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   win_rate.js                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: lflandri <lflandri@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2023/11/23 15:24:57 by lflandri          #+#    #+#             */
/*   Updated: 2024/02/15 17:24:07 by lflandri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

//TODO all

function win_rate_calcul(win_rate) {
	if (win_rate === null)
	{
		document.getElementById("progg_bar_win_rate").style.width = "100%";
		document.getElementById("progg_bar_win_rate").style.backgroundColor = "#ff9c00";
		document.getElementById("progg_bar_win_rate").textContent = "No Match done"
		document.getElementById("progg_bar_win_rate").style.textAlign = "center"

		let win_rate_indicator = document.getElementById("win_rate_indicator");
		win_rate_indicator.textContent = "???" ;
	}
	else
	{
		document.getElementById("progg_bar_win_rate").style.width = "" +  (win_rate * 100) +  "%"; 
		let win_rate_indicator = document.getElementById("win_rate_indicator");
		win_rate_indicator.textContent = "" + parseInt(win_rate * 100) ;
	}
}

function launchWinRate()
{
	const formWinRate = document.getElementById('data-request-relation');
	const data = new FormData(formWinRate);

	fetch("https://" + window.location.hostname + ":4200/getwinrate",
	{
		method: 'POST',
		body: data,
		cache: "default"
	})
			.then(response => response.json())
			.then (jsonData => {
				console.log("received from getwinrate : ")
				console.log(jsonData)
				if (! jsonData["success"])
				{
					console.error(jsonData["content"])
					return ;
				}
				console.log("Win Rate Calcul");
				win_rate_calcul(jsonData["content"]);
			})
			.catch(error => {
				console.log("erreur from getwinrate : ")
				console.error(error)
			})
}

launchWinRate();