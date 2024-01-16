/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   relation_request.js                                :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: lflandri <lflandri@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2024/01/16 18:53:21 by lflandri          #+#    #+#             */
/*   Updated: 2024/01/16 19:32:49 by lflandri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

function addFriend()
{
	var requete = new XMLHttpRequest();
	// requete.open("POST", ("https://" + window.location.hostname + ":4200/addfriends"));
	// requete.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

	
	// toSend = JSON.stringify(toSend)
	// console.log("test send : ")
	// console.log(toSend)
	// requete.send(toSend);
	// requete.onload = function() {
	// //La variable à passer est alors contenue dans l'objet response et l'attribut responseText.
	// var variableARecuperee = this.responseText;
	// console.log("received : ")
	// console.log(variableARecuperee)
	// /*continue here the script when reponse received*/
	// };
	// /let toSend = {"friend": document.getElementById("pseudo_profil_page").textContent}
	const form = document.getElementById('data-request-relation');
	const data = new FormData(form);

	fetch("https://" + window.location.hostname + ":4200/addfriends",
	{
		method: 'POST',
		body: data,
		cache: "default"
	})
			.then(response => response.json())
			.then (jsonData => {
				console.log("received : ")
				console.log(jsonData)
			})
			.catch(error => {
				console.log("erreur adding friend : ")
				console.error(error)
			})
	
}

function removedFriend()
{
	
}

function blockUser()
{
	
}

function unBlockUser()
{
	
}