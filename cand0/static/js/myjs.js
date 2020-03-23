function challenge_choice_on(challenge_name, challenge_message, challenge_value){
	document.getElementById("challenge_name").innerHTML = challenge_name;
	document.getElementById("challenge_message").innerHTML = challenge_message;

	document.getElementById("challenge-choice-wrapper").style.zIndex = "1";
	document.getElementById("challenge-choice-body").style.zIndex = "2";
}
function challenge_choice_off(){
        document.getElementById("challenge-choice-wrapper").style.zIndex = "-1";
	document.getElementById("challenge-choice-body").style.zIndex = "-1";
}
