/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   42_link.js                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: lflandri <lflandri@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2023/11/23 15:27:08 by lflandri          #+#    #+#             */
/*   Updated: 2024/01/23 20:33:24 by lflandri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

//TODO all

let status_link = document.getElementById("42_link_status_profil");
status_link.textContent = "Linked";
status_link.style.color = "green";

function changeLinkInterface(linked) {
	
}

function checkislinked() {
	const form = document.getElementById('data-request-relation');
	const data = new FormData(form);

	fetch("https://" + window.location.hostname + ":4200/checkislinked",
	{
		method: 'POST',
		body: data,
		cache: "default"
	})
			.then(response => response.json())
			.then (jsonData => {
				console.log("received from checkislinked : ")
				console.log(jsonData)
				changeRelationButton(jsonData["success"]);
			})
			.catch(error => {
				console.log("erreur from checkislinked : ")
				console.error(error)
			})
}