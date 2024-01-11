function sendMessage(data, input)
{
	// console.log("Try to send the message");
	// fetch("sendMessage",
	// 	{
	// 		method: 'POST',
	// 		body: data,
	// 		cache: "default"
	// 	})
	// 	.then(response => response.json())
	// 	.then (jsonData => {
	// 		if (jsonData['success'])
	// 		{
	// 			console.log("Message send succefully");
	// 			input.value = "";
	// 		}
	// 		else
	// 			console.log("Send message error :", jsonData["error"])
	// 	})
	// 	.catch(error => console.log("Fetch send message error :", error))

	console.log("Create ChatSocket");
	const chatSocket = new WebSocket("ws://" + window.location.hostname + ":8765");

	chatSocket.onmessage = function(e) {
		const data = JSON.parse(e.data);
		const message = data['message'];
		// Handle incoming message
	};

	chatSocket.onclose = function(e) {
		console.error('Chat socket closed unexpectedly');
	};

	// Send message to server
	function sendMessage(message) {
		chatSocket.send(JSON.stringify({
			'message': message
		}));
	}
}
