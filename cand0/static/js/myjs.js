function challenge_choice_on(){
	document.getElementById("challenge-choice-wrapper").style.zIndex = "1";
	document.getElementById("challenge-choice-body").style.zIndex = "2";
}
function challenge_choice_off(){
        document.getElementById("challenge-choice-wrapper").style.zIndex = "-1";
	document.getElementById("challenge-choice-body").style.zIndex = "-1";
}
