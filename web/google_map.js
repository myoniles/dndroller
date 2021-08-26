var user_placed_marker = null;
var gm_markers = [];

function initMap() {
	var center_loc = {lat: 40.426554, lng: -86.914252};
	var zoom_init = 16;
	args = window.location.href.split('id=')
	if (args.length > 1){
		// we have an argument passed, if it is an ID,
		// we should update the initial values
		var request = new XMLHttpRequest();
		request.open('GET','/bathroom/'+args[1], true);
		request.onload = function(){
			a = JSON.parse(request.responseText);
			console.log(a);
			var center_loc= { lat:a.lat, lng: a.lng};
			var zoom_init = 20;
			map = new google.maps.Map(document.getElementById('map'),{
			center: center_loc,
			zoom: zoom_init
			})
			place_bathroom( a, map);
		}
		request.send();
		return;
	}
	console.log(center_loc)
	console.log(zoom_init)

	map = new google.maps.Map(document.getElementById('map'),{
		center: center_loc,
		zoom: zoom_init
	});
	get_all_br(map);

	map.addListener('click', function(event){
		if (user_placed_marker != null)
			user_placed_marker.setMap(null);
		user_placed_marker = new google.maps.Marker({
			position: event.latLng,
			map: map,
		});
		document.getElementById("add_lat").value = event.latLng.lat();
		document.getElementById("add_lng").value = event.latLng.lng();
	});
}

function generate_marker_html( br_obj ){
	content_str = '<div class="markerWindow">'
		+'<a href=\"/br.html?id=' + br_obj._id + '\">'
		+'<h3>'+br_obj.name+'</h3>'
		+ '</a>';
		if( br_obj.stars != 0 ){
			content_str = content_str+ '<p>'
			+ br_obj.stars + ' stars'
			+ '</p>'
		}
		if( br_obj.tp_ply != null ){
			content_str = content_str+ '<p>'
			+'Toilet Paper Ply: '+ br_obj.tp_ply
			+ '</p>'
		}
		if( br_obj.diaper == true ){
			content_str = content_str+ '<p>'
			+ 'Diaper Changing Station'
			+ '</p>'
		}
		content_str += '</div>';
	return content_str
}

function place_bathroom( br_obj, map_obj){
	var marker = new google.maps.Marker({
		position:{lat:br_obj.lat, lng:br_obj.lng},
		map:map_obj,
		icon: '/toilets_inclusive.png'
	});
	content_str = generate_marker_html(br_obj);
	var info_window = new google.maps.InfoWindow({
		content: content_str
	});

	marker.addListener('click', function(){
		info_window.open(map_obj, marker);
	});
}

function gen_info( id ){
	var request = new XMLHttpRequest();
	request.open('GET','/bathroom/'+id, true);
	request.onload = function(){
		console.log(request.responseText);
		br_obj = JSON.parse(request.responseText);
		info_obj = document.getElementById("drawer")

		// add the needed information
		// build the info string
		info_str = "<h2>" + br_obj.name+'</h2>';
		if( br_obj.stars != 0 ){
			info_str = info_str+ '<p>'
			+ br_obj.stars + ' stars'
			+ '</p>'
		}
		if( br_obj.tp_ply != null ){
			info_str = info_str+ '<p>'
			+'Toilet Paper Ply: '+ br_obj.tp_ply
			+ '</p>'
		}
		if( br_obj.diaper == true ){
			info_str = info_str+ '<p>'
			+ 'Diaper Changing Station'
			+ '</p>'
		}
		// append to the document
		info_obj.children.br_info.innerHTML = info_str;

		// add the comments
		if (br_obj.comments.length ==0 ){
			info_obj.children.comments.innerHTML = '<p>Sorry, No Comments Here!</p>'
		} else {
			info_obj.children.comments.innerHTML = ''
			for (var i = br_obj.comments.length-1; i >= 0;	i--){
				// build the div
				// append to the document
				comment_div = document.createElement('div');
				comment_div.className = 'comment';
				commenthtml = '<h6 color=#7f3fff>' + br_obj.comments[i].user
				+ " | " + br_obj.comments[i].stars + " stars"
				+'</h3>'
				+'<p>'+br_obj.comments[i].body +'</p>';
				comment_div.innerHTML = commenthtml;
				info_obj.children.comments.appendChild(comment_div);
			}
		}

	}
	request.send();
	return;
}

function get_all_br( map_obj ){
	var request = new XMLHttpRequest();
	request.open('POST','/bathrooms_all/', true);
	request.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	request.onload = function(){
		a = JSON.parse(request.responseText);
		for ( var i = 0; i < a.length; i++){
			place_bathroom(a[i], map_obj);
		}
	}
	args = window.location.href.split('?')
	if ( args.length > 1)
		request.send(args[1]);
	else
		request.send();
	console.log(args)
}

// shamelessly stolen from https://stackoverflow.com/questions/7542586/new-formdata-application-x-www-form-urlencoded
function urlencodeFormData(fd){
	var s = '';
	function encode(s){ return encodeURIComponent(s).replace(/%20/g,'+'); }
	for(var pair of fd.entries()){
			if(typeof pair[1]=='string'){
					s += (s?'&':'') + encode(pair[0])+'='+encode(pair[1]);
			}
	}
	return s;
}

function create_br(){
	var frm = document.getElementById('create_br_form');
	var frmdata = new FormData(frm);
	var x_encod = urlencodeFormData(frmdata);
	console.log(frmdata);
	var xhr = new XMLHttpRequest();
	xhr.open('POST', '/bathrooms/', true);
	xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	xhr.onload = function(){
		console.log(xhr.responseText);
		var res = JSON.parse(xhr.responseText)
		if (res._id){
			var urls = window.location.href.split("?");
			window.location.href = "http://yoniles.com:3000/br.html?id="+res._id;
		}
	}
	xhr.send(x_encod);
}
