function challenge_choice_on(challenge_name, challenge_message, challenge_value, challenge_category){
	document.getElementById("admin_challenge_name").value = challenge_name;
	document.getElementById("admin_challenge_message").value = challenge_message;
	document.getElementById("admin_challenge_value").value = challenge_value;
	document.getElementById("admin_challenge_category").value = challenge_category;

	document.getElementById("challenge-choice-wrapper").style.zIndex = "1";
	document.getElementById("challenge-choice-body").style.zIndex = "2";
}
function challenge_choice_off(){
        document.getElementById("challenge-choice-wrapper").style.zIndex = "-1";
	document.getElementById("challenge-choice-body").style.zIndex = "-1";
}
