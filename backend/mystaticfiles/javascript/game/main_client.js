import "./define.js"
import {runGameClient} from "./tcp_client.js"


document.onreadystatechange = () => {
	if (document.readyState === 'complete') {
	  // document ready			
	console.log("launching game")
	runGameClient();
	console.log("exit document_waiting state")
	}
  };