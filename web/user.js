function getCookie(cname) {
	var name = cname + "=";
	var ca = document.cookie.split(';');
	for(var i = 0; i < ca.length; i++) {
		var c = ca[i];
		while (c.charAt(0) == ' ') {
			c = c.substring(1);
		}
		if (c.indexOf(name) == 0) {
			return c.substring(name.length, c.length);
		}
	}
	return "";
}

function login_prompt(){
	var inner ="";
	var user = getCookie("auth");
	var name = getCookie("username");
	if ( user == ""){
	r =  "<form>"
			+"<h3>User Account</h3>"
			+"Username<br>"
			+"<input type=\"text\" id=\"username_entry\" name=\"username\" maxlength=20>"
			+"<br>Password<br>"
			+"<input type=\"password\" id=\"password_entry\" name=\"password\" maxlength=20><br>"
			+"<input type=\"button\" onclick=\"login()\" value=\"Log in\">"
			+"<input type=\"button\" onclick=\"create_user()\" value=\"Create Account\">"
		  +"</form><br>";
	} else {
		inner = "<p>Hello, " + name + "<p/>";
	}
	document.getElementById("login").innerHTML = inner;
}

function login_header(){
	var inner ="";
	var user = getCookie("auth");
	var name = getCookie("username");
	if ( user == ""){
		inner = "<form>"
			+"Username:"
			+"<input type=\"text\" id=\"username_entry\" name=\"username\" maxlength=20>"
			+" Password:"
			+"<input type=\"password\" id=\"password_entry\" name=\"password\" maxlength=20>"
			+"<input type=\"button\" onclick=\"login()\" value=\"Log in\">"
			+"<input type=\"button\" onclick=\"create_user()\" value=\"Create Account\">"
		+"</form><br>";
		document.getElementById("login_header").innerHTML = inner;
	} else {
		inner = "Hello, " + name
		+" <input type=\"button\" onclick=\"logout()\" value=\"Logout\">";
		document.getElementById("login_header").innerHTML = inner;
	}
}

function logout(){
		document.cookie="auth=; expires=Thu, 01 Jan 1970 00:00:00 UTC;"
		document.cookie="username=; expires=Thu, 01 Jan 1970 00:00:00 UTC;"
		window.location.reload(true);
}

function user_comment_prompt(){
	var user = getCookie("auth");
	var name = getCookie("username");
	var inner ="";
	if (user == ""){
		document.getElementById("user_comment").innerHTML = "<p><a href=\"\/\">Login</a> to comment and rate this bathroom!"
	} else {
		inner = "<form>"
		+"<h3>Add a Comment</h3>"
		+"<input type=\"text\" id=\"comment_body\" name=\"username\" maxlength=140>"
		+"<select id=\"comment_stars\" name='stars'>"
		+"<option value=\"\" selected disabled hidden>-</option>"
		+"<option value='1'>1</option>"
		+"<option value='2'>2</option>"
		+"<option value='3'>3</option>"
		+"<option value='4'>4</option>"
		+"<option value='5'>5</option>"
		+"</select>"
		+"<input type=\"button\" onclick=\"publish_comment()\" value=\"Post Comment as "+ name +"\">"
		+"</form><br>";
		document.getElementById("user_comment").innerHTML = inner;
	}
}

function get_br_id(){
	args = window.location.href.split('id=')
	if ( args.length == 1 ){
		return null;
	} else {
		return args[1];
	}
}

function publish_comment(){
	var request = new XMLHttpRequest();
	var stars = document.getElementById("comment_stars").value;
	var name = getCookie("username");
	var comment_body =document.getElementById("comment_body").value;
	request.open('PUT', '/bathroom/'+ get_br_id()+'/comments/', true);
	request.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	request.onload = function(){
		console.log(request.responseText);
		r = JSON.parse(request.responseText);
		// Whether the comment was successfully posted is handled serverside
		if (r.response == true){
			//window.location.reload(true);
			window.location.href = window.location.href;
		} else {
			document.getElementById("comment_body").value = "Error. Could not verify login credentials.";
		}
	}
	args= "body="+comment_body+"&user="+name+"&stars="+stars;
	request.send(args);
}

function create_user(){
	var usern = document.getElementById("username_entry").value;
	var passwd = document.getElementById("password_entry").value;
	// need to make a request to the server, it will return an error
	// if it is a duplicate

	var request = new XMLHttpRequest();
	request.open('POST','/users/', true);
	request.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	request.onload = function(){
		r = JSON.parse(request.responseText);
		if (r.response == true){

			// create a cookie
			document.cookie="auth="+r.cookie;
			document.cookie="username="+r.usern+";";
			window.location.reload(true);
		} else {
			document.getElementById("username_entry").style.backgroundColor = "red";
			document.getElementById("password_entry").style.backgroundColor = "red";
		}
	}
	ags= "username="+usern+"&password="+passwd
	request.send(ags);
}

function login(){
	var usern = document.getElementById("username_entry").value;
	var passwd = document.getElementById("password_entry").value;
	var request = new XMLHttpRequest();
	request.open('PUT','/users/', true);
	request.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	request.onload = function(){
		r = JSON.parse(request.responseText);
		if (r.response == true){
			// create a cookie
			document.cookie="auth="+r.cookie+";username="+r.usern+";";
			document.cookie="username="+r.usern+";";
			window.location.reload(true);
		} else {
			document.getElementById("username_entry").style.backgroundColor = "red";
			document.getElementById("password_entry").style.backgroundColor = "red";
		}
	}
	args= "username="+usern+"&password="+passwd
	request.send(args);
}
