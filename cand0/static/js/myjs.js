function challenge_choice_on(challenge){
	challenge_name = challenge + "name";
	challenge_message = challenge + "message";

	challenge_name = document.getElementById(challenge_name).innerHTML;
	challenge_message = document.getElementById(challenge_message).innerHTML;

	challenge_name = challenge_name.replace(/(?:\r\n|\r|\n)/g, '<br />');
	document.getElementById("challenge_name").innerHTML = challenge_name;

	challenge_message = challenge_message.replace(/(?:\r\n|\r|\n)/g, '<br />');
	document.getElementById("challenge_message").innerHTML = challenge_message;
	document.getElementById("challenge-choice-wrapper").style.zIndex = "1";
	document.getElementById("challenge-choice-body").style.zIndex = "2";
}
function challenge_choice_off(){
        document.getElementById("challenge-choice-wrapper").style.zIndex = "-1";
	document.getElementById("challenge-choice-body").style.zIndex = "-1";
}
