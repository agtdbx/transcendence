var sound_counter = 0;

function getRandomInt(max)
{
	  return Math.floor(Math.random() * max);
}

function soundCountdown()
{
	if (sound_counter != 0)
		sound_counter--;
}

function playsound()
{
	if (sound_counter != 0)
		return ;
	let audio;
	switch (getRandomInt(12))
	{
		case 0:
			audio = new Audio("https://deeprockgalactic.wiki.gg/images/e/e3/Saluting2_6.ogg");
			break;
		case 1:
			audio = new Audio("https://deeprockgalactic.wiki.gg/images/3/3e/NEW_Saluting_5.ogg");
			break;
		case 2:
			audio = new Audio("https://deeprockgalactic.wiki.gg/images/1/10/RockAndStoneSalute_02.ogg");
			break;
		case 3:
			audio = new Audio("https://deeprockgalactic.wiki.gg/images/1/1e/RockAndStoneSalute_10.ogg");
			break;
		case 4:
			audio = new Audio("https://deeprockgalactic.wiki.gg/images/d/d6/NEW_Saluting_6.ogg");
			break;
		case 5:
			audio = new Audio("https://deeprockgalactic.wiki.gg/images/c/cb/RockAndStoneSalute3rdPickup_08.ogg");
			break;
		case 6:
			audio = new Audio("https://deeprockgalactic.wiki.gg/images/9/91/BarCheering_when_drinking_15.ogg");
			// insert here sucess pray for the fallen
			break;
		case 7:
			audio = new Audio("https://deeprockgalactic.wiki.gg/images/e/eb/RockAndStoneSalute3rdPickup_13.ogg");
			break;
		case 8:
			audio = new Audio("https://deeprockgalactic.wiki.gg/images/2/28/RockAndStoneSalute_07.ogg");
			break;
		case 9:
			audio = new Audio("https://deeprockgalactic.wiki.gg/images/a/a6/RockAndStoneSalute_01.ogg");
			break;
		case 10:
			audio = new Audio("https://deeprockgalactic.wiki.gg/images/1/19/Saluting2_19.ogg");
			break;
		case 11:
			audio = new Audio("https://deeprockgalactic.wiki.gg/images/8/83/Saluting2_4.ogg");
			break;
	
		
	}
	audio.play();
	sound_counter = 200;
}

setInterval(soundCountdown, 20);
document.addEventListener("keypress", function(event)
	{
		   if (event.code === 'KeyV')
		{
			playsound()
		}
	});