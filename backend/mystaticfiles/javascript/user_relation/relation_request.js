/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   relation_request.js                                :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: lflandri <lflandri@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2024/01/16 18:53:21 by lflandri          #+#    #+#             */
/*   Updated: 2024/01/16 22:03:01 by lflandri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

function changeRelationButton(value)
{
	btnSendFriendRequest = document.getElementById("btn-send-friend-request");
	btnRemoveFriend = document.getElementById("btn-remove-friend");
	btnBlockUser = document.getElementById("btn-block-user");
	btnUnBlockUser = document.getElementById("btn-unblock-user");
	pFriendRequestSend = document.getElementById("p-friend-request");
	switch (value) {
		case 1:
			pFriendRequestSend.style.display = "inline-block";
			btnBlockUser.style.display = "inline-block";
			btnSendFriendRequest.style.display = "none";
			btnRemoveFriend.style.display = "none";
			btnUnBlockUser.style.display = "none";
			break;
		case 2:
			btnRemoveFriend.style.display = "inline-block";
			btnBlockUser.style.display = "inline-block";
			btnUnBlockUser.style.display = "none";
			pFriendRequestSend.style.display = "none";
			btnSendFriendRequest.style.display = "none";
			break;
		case 3:
			btnSendFriendRequest.style.display = "inline-block";
			btnUnBlockUser.style.display = "inline-block";
			btnBlockUser.style.display = "none";
			btnRemoveFriend.style.display = "none";
			pFriendRequestSend.style.display = "none";
			break;
	
		default:
			btnSendFriendRequest.style.display = "inline-block";
			btnBlockUser.style.display = "inline-block";
			btnUnBlockUser.style.display = "none";
			btnRemoveFriend.style.display = "none";
			pFriendRequestSend.style.display = "none";
			break;
	}
}

function addFriend()
{
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
				if (! jsonData["success"])
				{
					console.error(jsonData["content"])
					alert(jsonData["content"])
					return ;
				}
				changeRelationButton(1);
			})
			.catch(error => {
				console.log("erreur adding friend : ")
				console.error(error)
			})
	
}

function removedFriend()
{
	const form = document.getElementById('data-request-relation');
	const data = new FormData(form);

	fetch("https://" + window.location.hostname + ":4200/removefriends",
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
					alert(jsonData["content"])
					return ;
				}
				changeRelationButton(0);
			})
			.catch(error => {
				console.log("erreur removing friend : ")
				console.error(error)
			})
}

function blockUser()
{
	const form = document.getElementById('data-request-relation');
	const data = new FormData(form);

	fetch("https://" + window.location.hostname + ":4200/block",
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
					alert(jsonData["content"])
					return ;
				}
				changeRelationButton(3);
			})
			.catch(error => {
				console.log("erreur adding friend : ")
				console.error(error)
			})
}

function unBlockUser()
{
	const form = document.getElementById('data-request-relation');
	const data = new FormData(form);

	fetch("https://" + window.location.hostname + ":4200/unblock",
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
					alert(jsonData["content"])
					return ;
				}
				changeRelationButton(0);
			})
			.catch(error => {
				console.log("erreur adding friend : ")
				console.error(error)
			})
}