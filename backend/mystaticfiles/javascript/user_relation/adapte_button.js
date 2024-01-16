/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   adapte_button.js                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: lflandri <lflandri@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2024/01/16 21:21:05 by lflandri          #+#    #+#             */
/*   Updated: 2024/01/16 21:52:35 by lflandri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

const form = document.getElementById('data-request-relation');
const data = new FormData(form);

fetch("https://" + window.location.hostname + ":4200/getrelation",
{
	method: 'POST',
	body: data,
	cache: "default"
})
		.then(response => response.json())
		.then (jsonData => {
			console.log("received from getrelation : ")
			console.log(jsonData)
			if (! jsonData["success"])
			{
				console.error(jsonData["content"])
				return ;
			}
			changeRelationButton(jsonData["value"]);
		})
		.catch(error => {
			console.log("erreur from getrelation : ")
			console.error(error)
		})