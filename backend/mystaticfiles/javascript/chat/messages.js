function sendMessage(data, input)
{
	console.log("Try to send the message");
	fetch("sendMessage",
		{
			method: 'POST',
			body: data,
			cache: "default"
		})
		.then(response => response.json())
		.then (jsonData => {
			if (jsonData['success'])
			{
				console.log("Message send succefully");
				input.value = "";
			}
			else
				console.log("Send message error :", jsonData["error"])
		})
		.catch(error => console.log("Fetch send message error :", error))
}
