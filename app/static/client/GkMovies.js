var xhr;

var searches = ["title", "review", "genre", "actor", "plot", "user01", "user02", "user03", "user04", "user05"];

function getSearchParams() {
	//alert('getSearchParams starts')
	var searchParams = "";
	for (i = 0; i < searches.length; i++) {
		elementName = searches[i] + "Search";
		var element = document.getElementById(elementName);
		if ( element != null ) {
			searchParams += "&" + elementName + "=" + element.value;
		}
	}
	return searchParams;
	

}
function doSearch(element) {

	var url = "displayMovies?thisSearch=" + element + "Search" + getSearchParams();
	//alert("in doSearch, url=" + url);
	window.open(url, "_self");
}

function doAdderSearch() {
	var titleSearch = document.getElementById("titleSearch").value.replace(' ', '+');
	//alert ("titleSearch=:" + titleSearch + ":");
	
	var url = "addMovies?titleSearch=" + titleSearch
	//alert("in doAdderSearch, url=" + url);
	window.open(url, "_self");
}

function doButton(element) {

	var url = "displayMovies?sortButton=" + element + getSearchParams();
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
        alert("Unexpected Failure")
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
        alert("Unexpected Failure")
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
    		div_button = document.getElementById('button_' + tt);
    		div_button.innerHTML = "Movie Added";
    	}
    }).fail(function() {
        alert("Unexpected Failure")
    });
    
    
	//var url = "addMovies?function=addMovie&tt=" + tt + "&titleSearch=" + titleSearch;
	//alert("in doSearch, url=" + url);
	//window.open(url, "_self");
}

function updateMovies() {
	var url = "updateMovies?function=run"
	//alert("url=" + url)
	window.open(url, "_self");
}

function deleteMovie(imdb_movie_id, title) {
	
	var r = confirm("Are you usre you want to delete '" + title + "'?");
	if (r == false) {
		return;
	}

	var url = "displayMovies?imdb_movie_id=" + imdb_movie_id + getSearchParams();
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
	var url = "settings_display_resetCol?name=" + colName 
	//alert("url=" + url)
	window.open(url, "_self");
}

function resetSort() {
	var url = "settings_display_resetSort"
	//alert("url=" + url)
	window.open(url, "_self");
}

function resetAll() {
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
