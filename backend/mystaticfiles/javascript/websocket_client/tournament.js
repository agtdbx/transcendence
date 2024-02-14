let pageForTournamentStatus = null;

function getTournamentStatus()
{
	let inter = setInterval(function () {
		if (webSocket.readyState != WebSocket.CONNECTING)
		{
			webSocket.send(JSON.stringify({
				'type' : 'tournament',
				'cmd' : 'getInfo'
			}));
			clearInterval(inter);
		}
		else
			console.log("wait");
	}, 10);


}


function manageMainpageButton(status, listPlayers, youInTournament)
{
	let inter = setInterval(function () {
		if (pageInLoad == false)
		{
			clearInterval(inter);

			let butJoinTournament = document.getElementById("mainBtnJoin");

			butJoinTournament.hidden = false;
			if (status == 0)
				butJoinTournament.hidden = true;
			else if (status == 1)
			{
				if (youInTournament == "true")
					butJoinTournament.textContent = "View";
				else if (listPlayers.length == 8)
					butJoinTournament.textContent = "Spectate";
				else
					butJoinTournament.textContent = "Register";
			}
			else if (status == 2)
				if (youInTournament == "true")
					butJoinTournament.textContent = "View";
				else
					butJoinTournament.textContent = "Spectate";
			else
				butJoinTournament.textContent = "Result";

			let butCreateTournament = document.getElementById("mainBtnAdmin");

			if (butCreateTournament == null)
				return ;

			butCreateTournament.hidden = false;
			if (status == 0 || status == 3)
				butJoinTournament.textContent = "Create tournament";
			else if (status == 1)
				butJoinTournament.textContent = "Modify tournament";
			else
				butCreateTournament.hidden = true;
		}
		else
			console.log("wait");
	}, 10);
}


