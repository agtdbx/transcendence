/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   42_link.js                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: lflandri <lflandri@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2023/11/23 15:27:08 by lflandri          #+#    #+#             */
/*   Updated: 2024/01/26 17:05:42 by lflandri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

//TODO all

function changeLinkInterface(linked)
{
	let status_link = document.getElementById("42_link_status_profil");
	let link_btn = document.getElementById("link-42-profil");
	let unlink_btn = document.getElementById("unlink-42-profil");
	if (linked)
	{
		status_link.textContent = "Linked";
		status_link.style.color = "green";
		unlink_btn.style.display = "block"
		link_btn.style.display = "none"

	}
	else
	{
		status_link.textContent = "Unlinked";
		status_link.style.color = "red";
		link_btn.style.display = "block"
		unlink_btn.style.display = "none"

	}
	
}

function checkislinked()
{
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
				changeLinkInterface(jsonData["success"]);
			})
			.catch(error => {
				console.log("erreur from checkislinked : ")
				console.error(error)
			})
}

function checkislinked()
{
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
				changeLinkInterface(jsonData["success"]);
			})
			.catch(error => {
				console.log("erreur from checkislinked : ")
				console.error(error)
			})
}

function removeLink()
{
	const form = document.getElementById('data-request-relation');
	const data = new FormData(form);

	fetch("https://" + window.location.hostname + ":4200/removelink",
	{
		method: 'POST',
		body: data,
		cache: "default"
	})
			.then(response => response.json())
			.then (jsonData => {
				console.log("received from removelink : ")
				console.log(jsonData)
				if (jsonData["success"])
				{
					changeLinkInterface(false);
				}
				else
				{
					alert(jsonData["error"])
					console.error(jsonData["error"])
				}
			})
			.catch(error => {
				console.log("erreur from removelink : ")
				console.error(error)
			})
}