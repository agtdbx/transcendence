/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   friend_request.js                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: lflandri <lflandri@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2024/01/16 22:32:37 by lflandri          #+#    #+#             */
/*   Updated: 2024/01/16 23:17:17 by lflandri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */


const form = document.getElementById('data-request-relation');
const data = new FormData(form);

fetch("https://" + window.location.hostname + ":4200/getlistefriendrequest",
{
	method: 'POST',
	body: data,
	cache: "default"
})
		.then(response => response.json())
		.then (jsonData => {
			console.log("received from getlistefriendrequest : ")
			console.log(jsonData)
			if (! jsonData["success"])
			{
				console.error(jsonData["content"])
				return ;
			}
			for (const user of jsonData["listRequest"])
			{
				document.getElementById("data-request-relation-input").value = user;
				const form = document.getElementById('data-request-relation');
				const data = new FormData(form);
				let url = ""
				if (confirm("You have a friend request of " + user + ".\n\nDo you accept it ?"))
					url = "https://" + window.location.hostname + ":4200/acceptfriends"
				else
					url = "https://" + window.location.hostname + ":4200/refusefriends"
				fetch(url,
				{
					method: 'POST',
					body: data,
					cache: "default"
				})
						.then(response => response.json())
						.then (jsonData => {
							if (! jsonData["success"])
							{
								console.error(jsonData["content"])
								return ;
							}
							else
							{
								console.log("received from friendresponse : ")
								console.log(jsonData)
							}
							
						})
						.catch(error => {
							console.log("erreur from getlistefriendrequest : ")
							console.error(error)
						})
			}
			
		})
		.catch(error => {
			console.log("erreur from getlistefriendrequest : ")
			console.error(error)
		})