import "./define.js"
import {runGameClient} from "./tcp_client.js"

console.log("game : " + gameStart)
let intervalGameStart = setInterval
(
	function ()
	{
		if (gameStart && document.getElementById("GameBox") != null && websockGame != null)
		{
			gameStart = false;
			runGameClient();
		}
	}
)

