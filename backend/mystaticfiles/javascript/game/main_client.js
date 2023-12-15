import "./define.js"
import {runGameClient} from "./tcp_client.js"


document.onreadystatechange = () => {
	if (document.readyState === 'complete') {
	  // document ready			
	console.log("test4")
	runGameClient();
	console.log("test3")
	}
  };