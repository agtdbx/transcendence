let pageForTournamentStatus = null;

function getTournamentStatus()
{
	webSocket.send(JSON.stringify({
		'type' : 'tournament',
		'cmd' : 'getInfo'
	}));
}
