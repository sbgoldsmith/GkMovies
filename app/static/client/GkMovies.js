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


function doAdderSearch() {
	var titleSearch = document.getElementById("titleSearch").value.replaceAll(' ', '+');
	//alert ("titleSearch=:" + titleSearch + ":");
	
	var url = "addMovies?titleSearch=" + titleSearch
	//alert("in doAdderSearch, url=" + url);
	window.open(url, "_self");
}


function doAdderCandidate(badWord) {
	
	var titleSearch = document.getElementById("titleSearch").value;
	var candidate = document.getElementById("candidate").value
	
	//alert('titleSearch=' + titleSearch + ', candidate=' + candidate + ', badWord=' + badWord)
	
	var newTitleSearch = titleSearch.replace(badWord, candidate).replaceAll(' ', '+')
			
			
	var url = "addMovies?titleSearch=" + newTitleSearch
	//alert("in doAdderCandidate, url=" + url);
	window.open(url, "_self");
}

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

function changeInput(name, imdbMovieId, dataType) {
	var boxName = name + "_" + imdbMovieId;
	var value = document.getElementById(boxName).value;

	//alert("In changeInput, boxName=" + boxName)
    $.post('inputField', {
    	imdbMovieId: imdbMovieId,
        name: name,
        value: value,
        dataType: dataType
    }).done(function(response) {
    	if ( response != "") {
        	alert(response)
    	}
    }).fail(function() {
        alert("changeInput(): Unexpected Failure")
    });

}

function changeSettingsDisplayInput(inp, name, colAttribute, dataType) {
	//alert("In changeSettingsDisplayInput, name=" + name + ", colAttribute=" + colAttribute)
	
	var boxName = name + "_" + colAttribute;
	
	//alert('looking for ' + boxName)
	
	

	
	if ( dataType == 'boolean' ) {
		var value = inp.checked ? 'T' : 'F'
	} else {
		var value = document.getElementById(boxName).value;
	}
	
	//alert("In changeSettingsDisplayInput, name=" + name + ", colAttribute=" + colAttribute + ", dataType=" + dataType + ", boxName=" + boxName + ", value=" + value )
	
	
    $.post('inputSettingsDisplayField', {
    	name: name,
    	colAttribute: colAttribute,
    	dataType: dataType,
        value: value
    }).done(function(response) {
    	if ( response != "") {
        	alert(response)
    	}
    }).fail(function() {
        alert("changeSettingsDisplayInput(): Unexpected Failure")
    });

}

function addMyMovie(tt) {
	//alert('addMovie starts, tt=' + tt)
	
    $.post('addMovie', {
    	tt: tt
    }).done(function(response) {
    	if ( response != "") {
        	alert(response)
    	} else {
    		user_div_button = document.getElementById('user_button_' + tt);
    		user_div_button.innerHTML = "Movie Added";
    		
    		imdb_div_button = document.getElementById('imdb_button_' + tt);
    		imdb_div_button.innerHTML = "Movie Loaded";
    	}
    }).fail(function() {
        alert("addMyMovie(): Unexpected Failure")
    });
    
}

function addImdb(tt) {
	//alert('addImdb starts, tt=' + tt)
	
    $.post('addImdb', {
    	tt: tt
    }).done(function(response) {
    	if ( response != "") {
        	alert(response)
    	} else {
    		imdb_div_button = document.getElementById('imdb_button_' + tt);
    		imdb_div_button.innerHTML = "Movie Loaded";
    	}
    }).fail(function() {
        alert("addImdb(): Unexpected Failure")
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

function upCol(colName) {
	var url = "settings_display_upCol?name=" + colName 
	//alert("url=" + url)
	window.open(url, "_self");
}

function dnCol(colName) {
	var url = "settings_display_dnCol?name=" + colName 
	//alert("url=" + url)
	window.open(url, "_self");
}

function resetCol(colName) {
	var r = confirm("Are you sure you want to reset column '" + colName + "'?");
	if (r == false) {
		return;
	}
	
	
	var url = "settings_display_resetCol?name=" + colName 
	//alert("url=" + url)
	window.open(url, "_self");
}

function resetSort() {
	var r = confirm("Are you sure you want to reset all column sorts?");
	if (r == false) {
		return;
	}
	
	
	var url = "settings_display_resetSort"
	//alert("url=" + url)
	window.open(url, "_self");
}

function resetAll() {
	var r = confirm("Are you sure you want to reset all column displays?");
	if (r == false) {
		return;
	}
	
	var url = "settings_display_resetAll" 
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
	
	//alert(url)
	window.open(url, "helpWindow", "height=500,width=800,menubar=no");	
}

function popNewVersions(numVersions) {

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
	 
	 
	var url = "versions_new";

	window.open(url, "versionsNewWindow", "height=400,width=600,menubar=no");	
}

function updateLastVisit() {	
	
	/*
	 * Silently update last visit
	 */
	 $.post('lastVisit', {
		 
	 	}).done(function(response) {

	    }).fail(function() {
	        alert("popNewVersions(): Unexpected Failure")
	    });	
}

function openerWindow(url) {
	opener.location.href=url;
}