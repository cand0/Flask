function challenge_choice_on(challenge, challenge_category){
	challenge_name = challenge + "name";
	challenge_value = challenge + "value";
	challenge_message = challenge + "message";

	/*개행, html <, > 사용*/
	challenge_name = document.getElementById(challenge_name).innerHTML;
        challenge_value = document.getElementById(challenge_value).innerHTML;
	challenge_message = document.getElementById(challenge_message).innerHTML;

	challenge_value = challenge_value.replace("VALUE : ", "")	//real value extraction

	challenge_name = challenge_name.replace(/(?:\r\n|\r|\n)/g, '<br />');
	challenge_name = challenge_name.replace(/&lt;/gi, '<');
	challenge_name = challenge_name.replace(/&gt;/gi, '>');

	challenge_message = challenge_message.replace(/(?:\r\n|\r|\n)/g, '<br />');
	challenge_message = challenge_message.replace(/&lt;/gi, '<');
	challenge_message = challenge_message.replace(/&gt;/gi, '>');

	document.getElementById("admin_challenge_name").value = challenge_name;
	document.getElementById("admin_challenge_value").value = challenge_value;
	document.getElementById("admin_challenge_category").value = challenge_category;
	document.getElementById("admin_challenge_message").value = challenge_message;

	document.getElementById("challenge-choice-wrapper").style.zIndex = "1";
	document.getElementById("challenge-choice-body").style.zIndex = "2";
}
function challenge_choice_off(){
        document.getElementById("challenge-choice-wrapper").style.zIndex = "-2";
	document.getElementById("challenge-choice-body").style.zIndex = "-2";
}
