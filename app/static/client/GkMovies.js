var xhr;
	
function doSearch(elementName) {
	elementName += 'Search';
	var elementValue = document.getElementById(elementName).value.replace(' ', '+');
	var url = "displayMovies?" + elementName + '=' + elementValue;
	//alert("in doSearch, url=" + url);
	window.open(url, "_self");
}

function searchActor(actorName){
	actorName = actorName.replace(' ', '+');
	var url = "displayMovies?actorSearch=" + actorName;
	//alert("in searchActor, url=" + url);
	window.open(url, "_self");
}

function searchCrew(crewName){
	crewName = crewName.replace(' ', '+');
	var url = "displayMovies?crewSearch=" + crewName;
	//alert("in searchCrew, url=" + url);
	window.open(url, "_self");
}

function setDisplayType(displayType, path) {
	if ( path.startsWith('/settings') ) {
		path = 'settings'
	} else {
		path = 'displayMovies'
	}
	var url = path + '?displayType=' + displayType;
	//alert("in setDisplayType, url=" + url);
	window.open(url, "_self");
}

function searchSeries(series){
	var url = "displayMovies?seriesSearch=" + series;
	//alert("in seriesSearch, url=" + url);
	window.open(url, "_self");
}

function clearSeries(series){
	var url = "displayMovies?seriesSearch=";
	//alert("in seriesSearch, url=" + url);
	window.open(url, "_self");
}

/*
 * Add Movie Search Functions
 */
function adderTypeSelect(typeSelect) {
	var url = "addMovies?action=typeSelect&addTypeSelectSearch=" + typeSelect
	//alert("in setAddSearch, url=" + url);
	window.open(url, "_self");
}

function adderTitleSearchOmdb() {
	var addTitleSearch = document.getElementById("addTitleSearch").value.replaceAll(' ', '+');
	
	if ( addTitleSearch.length > 3 ) {
		var workingElement = document.getElementById("working")
		workingElement.style.display = 'inline'
			
		var noresultsElement = document.getElementById("no_results")
		if (noresultsElement != null ) {
			noresultsElement.style.display = 'none'
		}
	} 

	//alert ("addTitleSearch=:" + addTitleSearch + ":");
	
	var url = "addMovies?action=titleSearchOmdb&addTitleSearch=" + addTitleSearch
	//alert("in doAdderSearch, url=" + url);
	window.open(url, "_self");
}


function adderTitleSearchOmdbCandidate(badWord) {
	
	var addTitleSearch = document.getElementById("addTitleSearch").value;
	var candidate = document.getElementById("candidate").value
	
	//alert('titleSearch=' + titleSearch + ', candidate=' + candidate + ', badWord=' + badWord)
	
	var newTitleSearch = addTitleSearch.replace(badWord, candidate).replaceAll(' ', '+')
			
			
	var url = "addMovies?action=titleSearchOmdb&addTitleSearch=" + newTitleSearch
	//alert("in doAdderCandidate, url=" + url);
	window.open(url, "_self");
}



function adderTitleSearchRapid() {
	var addTitleSearch = document.getElementById('addTitleSearch').value.replaceAll(' ', '+');
	var personSearchSpinner = document.getElementById('personSearchSpinner');
	personSearchSpinner.style.display = 'inline'
		
	var url = "addMovies?action=titleSearchRapid&addTitleSearch=" + addTitleSearch + "&addPersonSearch="
	//alert("in doAdderCandidate, url=" + url);
	window.open(url, "_self");
}


function adderPersonListRapid(id) {

	
	btn = document.getElementById('button_' + id);
	spinner = document.getElementById('spinner_' + id);
	
	btn.style.display = 'none'
	spinner.style.display = 'inline'

	
	var url = "addMovies?action=personListRapid&nameId=" + id
	//alert("in listPersonMovies, url=" + url);
	window.open(url, "_self");
	
}


function adderPersonSearchRapid() {
	
	var addPersonSearch = document.getElementById('addPersonSearch').value.replaceAll(' ', '+');
	var lesser = document.getElementById('addLesserSearch')
	
	
	var personSearchSpinner = document.getElementById('personSearchSpinner');
	personSearchSpinner.style.display = 'inline'
		
	var url = "addMovies?action=personSearchRapid&addPersonSearch=" + addPersonSearch + "&addLesserSearch=" + lesser.checked + "&addTitleSearch="
	//alert("url=" + url)
	window.open(url, "_self");
}

function adderGenreListRapid(genreCode) {

	var popularSearchSpinner = document.getElementById('popularSearchSpinner');
	popularSearchSpinner.style.display = 'inline'
		
	var url = "addMovies?action=popularListGenreRapid&genreCode=" + genreCode
	//alert("url=" + url)
	window.open(url, "_self");
}

/*
 * Button Functions
 */

function doButton(element) {

	var url = "displayMovies?sortButton=" + element;
	//alert("in doButton, url=" + url);
	window.open(url, "_self");
}



function setSearchFocus(element) {
	//alert("in setSearchFocus, element=" + element);
	
	var thisSearch = document.getElementById(element);
	if (thisSearch == null) return
	
	//alert("in setSearchFocus, thisSearch=" + thisSearch);
	
	var val = thisSearch.value; //store the value of the element
	
	thisSearch.focus(); //sets focus to element

	//alert("in setSearchFocus val=:" + val + ":");
	thisSearch.value = ''; //clear the value of the element
	thisSearch.value = val; //set that value back.  
}

function changeInput(name, imdbMovieId, dataFormat) {
	var boxName = name + "_" + imdbMovieId;
	var value = document.getElementById(boxName).value;

	//alert("In changeInput, boxName=" + boxName)
    $.post('inputField', {
    	imdbMovieId: imdbMovieId,
        name: name,
        value: value,
        dataFormat: dataFormat
    }).done(function(response) {
    	if ( response != "") {
        	alert(response)
    	}
    }).fail(function() {
        alert("changeInput(): Unexpected Failure")
    });

}

function changeSettingsDisplayInput(inp, name, displayType, colAttribute, dataFormat) {
	//alert("In changeSettingsDisplayInput, name=" + name + ", colAttribute=" + colAttribute)
	
	var boxName = name + "_" + colAttribute;
	
	//alert('looking for ' + boxName)
	
	

	
	if ( dataFormat == 'boolean' ) {
		var value = inp.checked ? 'T' : 'F'
	} else {
		var value = document.getElementById(boxName).value;
	}
	
	//alert("In changeSettingsDisplayInput, name=" + name + ", colAttribute=" + colAttribute + ", dataFormat=" + dataFormat + ", boxName=" + boxName + ", value=" + value )
	
	
    $.post('inputSettingsDisplayField', {
    	name: name,
    	displayType: displayType,
    	colAttribute: colAttribute,
    	dataFormat: dataFormat,
        value: value
    }).done(function(response) {
    	if ( response != "") {
        	alert(response)
    	}
    }).fail(function() {
        alert("changeSettingsDisplayInput(): Unexpected Failure")
    });

}

function addMyMovie(tt, displayType) {
	//alert('addMovie starts, tt=' + tt)
	
	spinner = document.getElementById('spinner_' + tt + '_' + displayType);
	button = document.getElementById('button_' + tt + '_' + displayType);
	
	button_seen = document.getElementById('button_' + tt + '_seen');
	button_want = document.getElementById('button_' + tt + '_want');
	button_imdb = document.getElementById('button_' + tt + '_imdb');
	
	spinner.style.display = 'inline'
	button.style.display = 'none'
		
	plot = document.getElementById('div_' + tt + '_plot');

    $.post('addMovie', {
    	tt: tt,
    	displayType: displayType
    }).done(function(response) {
		var plot_div = document.getElementById('div_' + tt + '_plot');
		var cast_div = document.getElementById('div_' + tt + '_cast');
		var crew_div = document.getElementById('div_' + tt + '_crew');
		
		if ( crew_div != null ) {
    		var json = jQuery.parseJSON(response);

    		plot_div.innerHTML = json.plot
    		cast_div.innerHTML = json.cast
    		crew_div.innerHTML = json.crew	

    	} 
    
		spinner.style.display = 'none'
		button.style.display = 'inline'
				
		if ( displayType == 'seen' ) {
			button_seen.innerHTML = "I Saw this Movie";
			button_want.innerHTML = ''
				
		} else if ( displayType == 'want' ) {
			button_want.innerHTML = 'Movie on Watch List'
			
		} else if (displayType = 'imdb') {
			button_imdb.innerHTML = 'Movie Added to Imdb'
		}
    		

    	
    }).fail(function() {
        alert("addMyMovie(): Unexpected Failure")
    });
    
}



function refreshAdder(tt, what) {
	//alert('refreshAdder starts, tt=' + tt + ", what=" + what)
	
	div = document.getElementById('div_' + tt + '_' + what);
	spinner = document.getElementById('spinner_' + tt + '_' + what);
	tbl = document.getElementById('tbl_' + tt + '_' + what);
	
	spinner.style.display = 'inline'
	tbl.style.display = 'none'
		
    $.post('refreshAdder', {
    	tt: tt,
    	what: what
    }).done(function(response) {
    	spinner.style.display = 'none'
    	tbl.style.display = 'inline'	
    	div.innerHTML = response;
    	//alert('response = ' + response)
    	
    }).fail(function() {
        alert("refreshAdder(): Unexpected Failure")
    });

}




function updateMovies() {
	var url = "updateMovies?function=run"
	//alert("url=" + url)
	window.open(url, "_self");
}

function deleteMovie(imdb_movie_id, title) {
	
	var r = confirm("Are you sure you want to delete '" + title + "'?");
	if (r == false) {
		return;
	}

	var url = "displayMovies?imdb_movie_id=" + imdb_movie_id
	//alert("url=" + url)
	window.open(url, "_self");
}

function upCol(colName, displayType) {
	var url = "settings_display_upCol?name=" + colName + '&displayType=' + displayType
	//alert("url=" + url)
	window.open(url, "_self");
}

function dnCol(colName, displayType) {
	var url = "settings_display_dnCol?name=" + colName + '&displayType=' + displayType
	//alert("url=" + url)
	window.open(url, "_self");
}

function resetCol(colName, displayType) {
	var r = confirm("Are you sure you want to reset column '" + colName + "'?");
	if (r == false) {
		return;
	}
	
	
	var url = "settings_display_resetCol?name=" + colName + '&displayType=' + displayType
	//alert("url=" + url)
	window.open(url, "_self");
}

function resetSort(displayType) {
	var r = confirm("Are you sure you want to reset all column sorts?");
	if (r == false) {
		return;
	}
	
	
	var url = "settings_display_resetSort?displayType=" + displayType
	//alert("url=" + url)
	window.open(url, "_self");
}

function resetAll(displayType) {
	var r = confirm("Are you sure you want to reset all column displays?");
	if (r == false) {
		return;
	}
	
	var url = "settings_display_resetAll?displayType=" + displayType 
	//alert("url=" + url)
	window.open(url, "_self");
}

function settingsColors(selectCol) {

	var overColor = 'deepskyblue'
	var leaveColor = 'white'
    var elements= document.getElementsByTagName('tr');
	
    for(var i=0; i<elements.length;i++)
    {
	   	if ( ! (elements)[i].id.startsWith('user_')) {
	   		continue
	   		
	   	}
	   	/*
	   	 * Previously selected so highlight this one
	   	 */
		if ( (elements)[i].id == 'user_' + selectCol ) {
			setColor((elements)[i], 'on')
		}
	    
		
		/*
		 * On mouseenter, unlighlight all rows and hilight the new one.
		 */
	    (elements)[i].addEventListener("mouseenter", function(){
	    	
	    	for(var i=0; i<elements.length;i++)
	        {
	    	   	if (  (elements)[i].id.startsWith('user_')) {
	    	   		setColor( (elements)[i], 'off')
	    	   		
	    	   	}
	    		
	        }
	    	setColor(this, 'on')
	    });
	    
		/*
		 * On mouseleave, unlighlight the one we are leaving
		 */
	    (elements)[i].addEventListener("mouseleave", function(){
			setColor(this, 'off')
	   	});
	    
    }

}

function setColor(element, onoff) {
	var overColor = 'deepskyblue'
	var leaveColor = 'white'
	var color, display;
	
	if ( onoff == 'on' ) {
		color = overColor
		display = 'inline'
	} else {
		color = leaveColor
		display = 'none'
	}
	
	
	element.style = 'background-color:' + color + ';';
	arrow_id  = "arrow_" + element.id.substring(5)
	arrow_element =  document.getElementById(arrow_id);
	arrow_element.style.display = display
		
		
}

function changePerPage() {
	var perPage = document.getElementById('perPage');
	//alert('perPage' + perPage.value)
	var url = "displayMovies?perPage=" + perPage.value 
	window.open(url, "_self");
	
}
function help(path) {
	
	var url = "help?path=" + path.substring(1);
	
	var under = url.indexOf('_')
	if ( under > -1 ) {
		url = url.substring(0, under);
	}
	
	window.open(url, "helpWindow", "height=500,width=800,menubar=no,location=no");	
}

function popNewVersions(numVersions, rand) {

	if ( numVersions == 0 ) {
		return;
	} else if ( numVersions == 1 ) {
		var message = "A new version has"
	} else {
		var message = numVersions + " new versions have"
	}

	
	
	var r = confirm(message + " been installed since your last visit.\nWould you like to see what's new?");
	if (r == false) {
		updateLastVisit();
		return;
	}
	 
	 
	var url = "versions_new?r=" + rand;

	window.open(url, "versionsNewWindow", "height=400,width=650,menubar=no,location=no");	
}

function updateLastVisit() {	
	
	/*
	 * Silently update last visit
	 */
	 $.post('lastVisit', {
		 
	 	}).done(function(response) {

	    }).fail(function() {
	        alert("updateLastVisit(): Unexpected Failure")
	    });	
}

function movieSeen(tt) {
	var url = "movie_seen?tt=" + tt 
	//alert("url=" + url)
	window.open(url, "_self");
	
}

function backToOpener(url, rule) {
	alert('9 rule=' + rule)
	if ( rule == '/versions') {
		// Coming from Release Notes
		window.open(url, "_self");
	} else {
		// Coming from pop up
		opener.location.href=url;
		opener.focus();  //does not work 
		//window.close();	

	}
}

function setUpEye(url_rule) {
	const togglePassword = document.querySelector('#togglePassword');
	const password = document.querySelector('#password');
	const password2 = document.getElementById('password2');

	
	togglePassword.addEventListener('click', function (e) {
	    // toggle the type attribute
	    const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
	    
	    doPw(password, type, url_rule)
	    doPw(password2, type, url_rule)
	  
	    // toggle the eye slash icon
	    this.classList.toggle('fa-eye-slash');
	});
}

function doPw(pw, type, url_rule) {
	
	if ( pw == null ) {
		return
	}
	
	if ( url_rule.startsWith('/settings') ) {
	    if (pw.value == 'NothingToSee' && type == 'text' ) {
	    	pw.value = ''
	    } else if ( pw.value  == '' && type == 'password' ) {
	    	pw.value = 'NothingToSee'
	    }
	}
	
    pw.setAttribute('type', type);
}
