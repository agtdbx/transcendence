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
				{
					butJoinTournament.textContent = "View";
					butJoinTournament.onclick = function () {
						changePage("71");
					}
				}
				else if (listPlayers.length == 8)
				{
					butJoinTournament.textContent = "Spectate";
					butJoinTournament.onclick = function () {
						changePage("72");
					}
				}
				else
				{
					butJoinTournament.textContent = "Register";
					butJoinTournament.onclick = function () {
						changePage("7");
					}
				}
			}
			else if (status == 2)
				if (youInTournament == "true")
				{
					butJoinTournament.textContent = "View";
					butJoinTournament.onclick = function () {
						changePage("71");
					}
				}
				else
				{
					butJoinTournament.textContent = "Spectate";
					butJoinTournament.onclick = function () {
						changePage("72");
					}
				}
			else
			{
				butJoinTournament.textContent = "Result";
				butJoinTournament.onclick = function () {
					changePage("73");
				}
			}

			let butCreateTournament = document.getElementById("mainBtnAdmin");

			if (butCreateTournament == null)
				return ;

			butCreateTournament.hidden = false;
			if (status == 0 || status == 3)
				butCreateTournament.textContent = "Create tournament";
			else if (status == 1)
				butCreateTournament.textContent = "Modify tournament";
			else
				butCreateTournament.hidden = true;
		}
		else
			console.log("wait");
	}, 10);
}


function joinTournament(data)
{

}
