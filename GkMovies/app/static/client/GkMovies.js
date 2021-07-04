var xhr;

const clearSearchValues = ['title', 'genre', 'actor', 'crew', 'plot.outline', 'plot.summary', 'dateAdded', 'my_date_seen', 'my_rating', 'my_review', 'user01', 'user02', 'user03', 'user04', 'user05', 'user06', 'user07', 'user08', 'user09', 'user10' ]

/*
 * Display Movie Search Functions
 */
function showBaseSpinner(url) {
	var base_spinner = document.getElementById('base_spinner')
	if ( base_spinner != null ) {
		base_spinner.style.display = 'inline'
	} 
	
	bodyHeight =  window.innerHeight - 270
	tok = url.indexOf('?') > -1 ? '&' : '?'
	
	url += tok + "bodyHeight=" + bodyHeight
	//alert('in showBaseSpinner, url=' + url);
	window.open(url, "_self");	
}


function showSpinner() {
	var base_spinner = document.getElementById('base_spinner')
	if ( base_spinner != null ) {
	
		base_spinner.style.display = 'inline'
	} 
}

function hideSpinner() {
	var base_spinner = document.getElementById('base_spinner')
	if ( base_spinner != null ) {
		base_spinner.style.display = 'none'
	} 
}


function doMovies() {
	/*
	 *  Called when a new page is constructed
	 */

	showSpinner()
	
	//alert('doMovies())
	$.post('isFiltered', {

	}).done(function(response) {
		if ( response == 'True' ) {
			var displayMoviesFilterRowClear = document.getElementById('displayMoviesFilterRowClear');
			displayMoviesFilterRowClear.style.display = 'inline'
		}
    }).fail(function() {
        alert("doMovies(): Unexpected Failure on isFiltered")
    });
	
	
    $.post('doMovies', {
    	bodyHeight:  window.innerHeight - 250,
    }).done(function(response) {
    	//displayMoviesTitleTable = document.getElementById('displayMoviesTitleTable');
    	displayMoviesFilterRow = document.getElementById('displayMoviesFilterRow');
    	displayMoviesFilterRow.style.display = 'inline'
    		
    	redraw(response)

    		
    	displayMoviesTitleTable.style.backgroundColor = '#EBF5FB'
    	displayMoviesTitleTable.style.borderTop = "1px solid #222222";
    	displayMoviesTitleTable.style.borderLeft = "1px solid #222222"; 	
    	displayMoviesTitleTable.style.borderRight = "1px solid #222222";

    	hideSpinner()
    	
    }).fail(function() {
        alert("doMovies(): Unexpected Failure")
    });
    

}


function createFilterWait(elementName) {
	//alert('createFilterWait(): elementName=' + elementName)
	var element = document.getElementById(elementName)
	let timeout = null;
	
	element.addEventListener('input', function (e) {	    
	    clearTimeout(timeout);

	    // Make a new timeout set to go off in 500ms (1/2 second)
	    timeout = setTimeout(function () {
	        //console.log('Input Value:', element.value);
	    	doFilter(elementName)
	    }, 500);
	    
	}) 
}



function doFilter(elementName) {
	var elementValue = document.getElementById(elementName).value.replace(' ', '+');
	
	showSpinner()

	
	//alert('doFilter(): elementName=' + elementName + ', elementValue=' + elementValue)
    $.post('filterMovies', {
    	elementName: elementName,
    	elementValue: elementValue
    }).done(function(response) {
    	redraw(response)
    	
    	var displayMoviesFilterRowClear = document.getElementById('displayMoviesFilterRowClear');
    	displayMoviesFilterRowClear.style.display = 'inline'

    	hideSpinner()
    	
    }).fail(function() {
        alert("doFilter(): Unexpected Failure")
    });
    

}

function clearFilters(elementName) {
	showSpinner()

	//alert('clearFilters() elementName=' + elementName + ', elementValue=' + elementValue)
    $.post('clearFilters', {
    }).done(function(response) {
    	redraw(response)
    	displayMoviesFilterRowClear.style.display = 'none'
    	clearFilterFields()
    	hideSpinner()
    	
    }).fail(function() {
        alert("doFilter(): Unexpected Failure")
    });
    

}

function clearFilterFields() {
	
	for (var i = 0; i < clearSearchValues.length; i++) {
		//console.log('checking ' + clearSearchValues[i])
		element = document.getElementById(clearSearchValues[i] + 'Search')
		if (element != null ) {
			element.value = ''
		}
	}
	
}

function doPager(elementName, elementValue) {
	
	showSpinner()

	//alert('doPager() elementName=' + elementName + ', elementValue=' + elementValue)
    $.post('pageMovies', {
    	elementName: elementName,
    	elementValue: elementValue
    }).done(function(response) {
    	redraw(response)
    	hideSpinner()
    	
    }).fail(function() {
        alert("doPager(): Unexpected Failure")
    });
    

}




function doSort(sort) {
	
	showSpinner()
	
	//alert('doSort() elementName=' + elementName + ', elementValue=' + elementValue)
    $.post('sortMovies', {
    	sortButton: sort,
    }).done(function(response) {
    	redraw(response)
    	hideSpinner()
    	
    }).fail(function() {
        alert("doSort(): Unexpected Failure")
    });

}




function changePerPage() {
	var elementName = 'perPage'
	var elementValue = document.getElementById('perPage').value;
	
	doPager(elementName, elementValue)
	
}

function filterActor(actorName){
	actorSearch = document.getElementById('actorSearch');
	actorSearch.value = actorName
	doFilter('actorSearch')
}

function filterCrew(crewName){
	crewSearch = document.getElementById('crewSearch');
	crewSearch.value = crewName
	doFilter('crewSearch')
}

function setDisplayType(displayType, path) {

	param='?displayType=' + displayType;
	if ( path.startsWith('/settings') ) {
		url = 'settings' + param
		//alert("in setDisplayType, url=" + url);
		window.open(url, "_self");	
	} else {
		url = 'displayMovies' + param
		//alert("in setDisplayType, url=" + url);
		
		var base_spinner = document.getElementById('base_spinner')
		if ( base_spinner != null ) {
			base_spinner.style.display = 'inline'
		} 

		window.open(url, "_self");

	}
	
	//alert("in setDisplayType, url=" + url);
	
}


function deleteMovie(imdb_movie_id, title) {
	
	var r = confirm("Are you sure you want to delete '" + title + "'?");
	if (r == false) {
		return;
	}

		
	showSpinner()
	
	//alert('deleteMovie()')
	
    $.post('deleteMovie', {
    	imdb_movie_id: imdb_movie_id,
    	elementName: 'delete',
    	elementValue: ''
    }).done(function(response) {
    	redraw(response)
    	hideSpinner()
    	
    }).fail(function() {
        alert("deleteMovie(): Unexpected Failure")
    });

}


function filterSeries(series){

	showSpinner()
	

    $.post('filterSeries', {
    	elementName: 'seriesSearch',
    	elementValue: series
    }).done(function(response) {

    	redraw(response)
    	hideSpinner()
    	
    }).fail(function() {
        alert("filterSeries(): Unexpected Failure")
    });
	
}

function clearSeries(series){
	filterSeries('')
}




function redraw(response) {
	
	var displayMoviesFoundCell = document.getElementById('displayMoviesFoundCell');
	var displayMoviesPageCell = document.getElementById('displayMoviesPageCell');
	var displayMoviesSortRow = document.getElementById('displayMoviesSortRow');
	var displayMoviesBody = document.getElementById('displayMoviesBody');

	
	displayMoviesFoundCell.innerHTML = response.renderFoundCell;
	displayMoviesPageCell.innerHTML = response.renderPageCell;
	displayMoviesSortRow.innerHTML = response.renderSortRow;
	displayMoviesBody.innerHTML = response.renderBody;

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
	var addTitleSearch = document.getElementById("addTitleSearch");
	var addTitleSearchValue = addTitleSearch.value.replaceAll(' ', '+')
	var workingElement = document.getElementById("working")
	workingElement.style.display = 'inline'
	
	var no_results = document.getElementById("no_results")
	no_results.style.display = 'none'
		
    $.post('addMoviesOmdbCandidates', {
    	addTitleSearch: addTitleSearchValue
    }).done(function(response) {
    	candidates = document.getElementById("candidates")
    	candidates.innerHTML = response
    }).fail(function() {
        alert("adderTitleSearchOmdb(): Unexpected Failure")
    });
    

    $.post('addMoviesOmdb', {
    	addTitleSearch: addTitleSearchValue
    }).done(function(response) {
    	workingElement.style.display = 'none'
    	addMoviesTable = document.getElementById("addMoviesTable")
    	addMoviesTable.innerHTML = response
    	
    	if (addTitleSearchValue != '' && response.indexOf('<TD') == -1 ) {
    		//alert('addTitleSearchValue=' + addTitleSearchValue)
    		//alert('response.indexOf=' + response.indexOf('<TD'))
    		no_results.style.display = 'inline'
    	} 
    }).fail(function() {
        alert("adderTitleSearchOmdb(): Unexpected Failure")
    });

}


function adderTitleSearchOmdbCandidate(badWord) {
	 
	var addTitleSearch = document.getElementById("addTitleSearch")
	var candidate = document.getElementById("candidate").value
	var candidates = document.getElementById("candidate")
	
	var newTitleSearch = addTitleSearch.value.replace(badWord, candidate).replaceAll(' ', '+')
	//alert('In adderTitleSearchOmdbCandidate, titleSearch=' + newTitleSearch)		
	var noresultsElement = document.getElementById("no_results")
	
	var workingElement = document.getElementById("working")
	workingElement.style.display = 'inline'
	var no_results = document.getElementById("no_results")
	no_results.style.display = 'none'
		
	$.post('addMoviesOmdb', {
    	addTitleSearch: newTitleSearch
    }).done(function(response) {
    	workingElement.style.display = 'none'
    	addTitleSearch.value = newTitleSearch
    	candidates.innerHTML = ''
    	addMoviesTable = document.getElementById("addMoviesTable")
    	addMoviesTable.innerHTML = response
    	
    	if ( addTitleSearch.value != '' && response.indexOf('<TD') == -1 ){
    		no_results.style.display = 'inline'
    	} 
    	
    }).fail(function() {
        alert("adderTitleSearchOmdb(): Unexpected Failure")
    });

}


function adderSearchRapid() {
	var addTitleSearch = document.getElementById('addTitleSearch').value
	var addPersonSearch = document.getElementById('addPersonSearch').value
	
	if (addTitleSearch != '') {
		adderTitleSearchRapid()
	} else if (addPersonSearch != '')  {
		adderPersonSearchRapid()
	}
	
}

function adderTitleSearchRapid() {
	var addTitleSearch = document.getElementById('addTitleSearch').value.replaceAll(' ', '+');
	var personSearchSpinner = document.getElementById('personSearchSpinner');
	personSearchSpinner.style.display = 'inline'
		
	var url = "addMovies?action=titleSearchRapid&addTitleSearch=" + addTitleSearch + "&addPersonSearch="
	//alert("in adderTitleSearchRapid, url=" + url);
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

function adderPersonListRapid(id) {

	
	btn = document.getElementById('button_' + id);
	spinner = document.getElementById('spinner_' + id);
	
	btn.style.display = 'none'
	spinner.style.display = 'inline'

	
	var url = "addMovies?action=personListRapid&nameId=" + id
	//alert("in listPersonMovies, url=" + url);
	window.open(url, "_self");
	
}

function adderGenreListRapid(lastChecked) {
	var showMine = document.getElementById('showMineField').checked ? 'True' : 'False'
	var checkedCodes = setGenreCheckBoxesBefore(lastChecked)

	rankField = document.getElementById('rankField-0').checked ? 'rank' : 'popularity'
	
	no_movies = document.getElementById('no_movies')
	if ( no_movies != null ) {
		no_movies.style.display = 'none';
	}
	document.getElementById('genres_selected').style.display = 'none'
	document.getElementById('popularSearchSpinner').style.display = 'inline'
		
	var url = "addMovies?action=popularListGenreRapid&rankField=" + rankField + "&showMine=" + showMine + '&checkedCodes=' + checkedCodes
	//alert("url=" + url)
	window.open(url, "_self");
}

function setGenreCheckBoxesBefore(lastChecked) {

	
	var checkBoxes = document.getElementsByTagName('input');	
	
	checkedCodes = ''
	if ( lastChecked == 'genreBoxes-all' ) {
		var lastCheckedOn = document.getElementById(lastChecked).checked
		if (lastCheckedOn) {
			/*
			 * Last Checked On is All Genres so de-check all other check boxes
			 */
			for (var i = 0; i < checkBoxes.length; i++) {
				if ( checkBoxes[i].name.startsWith('genreBoxes') && checkBoxes[i].name != 'genreBoxes-all') {
					checkBoxes[i].checked = false;
				}
			}
			checkedCodes = 'all,'
		} else {
			checkedCodes = 'none,'
		}
	} else {
		/*
		 * Some other check box was checked.
		 */
		if (lastChecked != '') {
			/*
			 * It was another genre checkbox so set all to false.
			 */
			document.getElementById('genreBoxes-all').checked = false
		} else {
			/*
			 * Its was Rank or show mine so no action, the calling routine will handle it.
			 */
		}
	
		found = false;
		for (var i = 0; i < checkBoxes.length; i++) {
			if (checkBoxes[i].name.startsWith('genreBoxes') && checkBoxes[i].checked) {
				checkedCodes += checkBoxes[i].name.substring(11) + ',';
				found = true
			}
		}
		
		if (!found) {
			checkedCodes = 'none,'
		}
	}

	return checkedCodes;
}

function setGenreCheckBoxesAfter(checked) {
	var checkBoxes = document.getElementsByTagName('input');
	
	for (var i = 0; i < checkBoxes.length; i++) {
		if (! checkBoxes[i].name.startsWith('genreBoxes-')) {
			continue;
		}
		
		name = checkBoxes[i].name.substring(11) + ','
		//console.log('looking for ' + name)
		if (checked.indexOf(name) != -1 ) {
			checkBoxes[i].checked = true
		}
	}
}


function clearText(name) {
	//alert('clearText name=' + name)
	var element = document.getElementById(name)
	element.value = ''
}

function createWait(id) {
	var element = document.getElementById(id)
	let timeout = null;
	
	element.addEventListener('input', function (e) {	    
	    clearTimeout(timeout);

	    // Make a new timeout set to go off in 500ms (1/2 second)
	    timeout = setTimeout(function () {
	        //console.log('Input Value:', element.value);
	        adderTitleSearchOmdb()
	    }, 500);
	    
	});
	
	

    
    
}

/*
 * Club Functions
 */
function movieReview(club_id, imdb_movie_id) {
	var url = 'movieReview?club_id=' + club_id + '&imdb_movie_id=' + imdb_movie_id
	//alert("url=" + url)
	
	window.open(url, "reviewWindow", "height=750,width=850,menubar=no,location=no");	

	
}

function displayClub(club_id) {
	var url = 'displayClub?club_id=' + club_id
	showBaseSpinner(url)
}


/* 
function changeUserReview(boxName, club_id, user_movie_id)
{
	elementName = boxName + '_' + user_movie_id
	var value = document.getElementById(elementName).value;
	//alert('changeUserReview(): boxName=' + boxName + ', user_movie_id=' + user_movie_id + ', value=' + value)
	
	$.post('changeUserReview', {
		club_id: club_id,
		user_movie_id: user_movie_id,
		boxName: boxName,
		value: value
	}).done(function(response) {
    	if ( response != "") {
    		if ( response.startsWith('==')){
    			// new average rating
    			avg = response.substring(2)
    			document.getElementById('my_rating').value = avg;
    			clubChangeAverage(club_id, user_movie_id, avg)
    		} else {
    			alert(response)
    		}

    	}
    }).fail(function() {
        alert("changeUserReview(): Unexpected Failure")
    });

}  */

function clubUpdateField(club_id, user_movie_id, name, dataFormat) {
	box = name + '_' + user_movie_id
	//alert('In clubUpdateField(): club_id=' + club_id + ', user_movie_id=' + user_movie_id + ', name=' + name + ', dataFormat=' + dataFormat)
	var value = document.getElementById(box).value;
	//alert('In clubUpdateField(): value=' + value)
	console.log('clubUpdateField() called')
            

    $.post('clubUpdateField', {
    	club_id: club_id,
    	user_movie_id: user_movie_id,
        name: name,
        value: value,
        dataFormat: dataFormat
    }).done(function(response) {
     	if ( response != "") {
    		if ( response.startsWith('==')){
    			// new club average rating
    			under = response.indexOf('_')
    			user_movie_id = response.substring(2, under)  // club's user movie
    			avg = response.substring(under+1)
    			box = name + '_' + user_movie_id
    			document.getElementById(box).value = avg;
    		} else {
    			alert(response)
    		}

    	}
    }).fail(function() {
        alert("clubUpdateField(): Unexpected Failure")
    });

}



function clubManageDelete(club_id, name) {
	var r = confirm("Are you sure you want to delete club: '" + name + "'?");
	if (r == false) {
		return;
	}
	
	
	var url = 'clubManageDelete?club_id=' + club_id
	//alert("url=" + url)
	window.open(url, "_self");
}


function clubReviewSync(club_id, imdb_movie_id, cnt) {
	//console.log('clubReviewSync(): club_id=' + club_id + ', imdb_movie_id=' + imdb_movie_id + ', cnt=' + cnt)
	

	timeout = 500
	
	setTimeout(function() {
	
		$.post('clubGetCache', {
	    	club_id: club_id,
	    	imdb_movie_id: imdb_movie_id
	    }).done(function(response) {
		    for(var i = 0; i < response.length; i++) {
		    	tuple = response[i]
		    	element = document.getElementById(tuple[0])
		    	if ( element.value.trimEnd() != tuple[1].trimEnd()) {
		    		element.value = tuple[1].trimEnd()

		    		//console.log('set key = ' + tuple[0])
		    		//console.log('element.value = :' + element.value + ':')
		    		//console.log('tuple[1] = :' + tuple[1] + ':')
		    	}
		    }
	    }).fail(function() {
	        return
	    });
	
		clubReviewSync(club_id, imdb_movie_id, cnt+1)
		
	}, timeout);
	
}

/*
 * Other Functions
 */





function setSearchFocus(element) {
	//alert("3 in setSearchFocus, element=" + element);
	
	var thisSearch = document.getElementById(element);
	if (thisSearch == null) return
	
	//alert("in setSearchFocus, thisSearch=" + thisSearch);
	
	var val = thisSearch.value; //store the value of the element

	thisSearch.focus(); //sets focus to element
	//focusAndOpenKeyboard(thisSearch); // for iOS

	//alert("in setSearchFocus val=:" + val + ":");
	thisSearch.value = ''; //clear the value of the element
	thisSearch.value = val; //set that value back. 

	//focusAndOpenKeyboard(thisSearch); // for iOS
}


function focusAndOpenKeyboard(element) {
	//alert('in focusAndOpenKeyboard')
	//console.log('30 focusAndOpenKeyboard(), element.value=' + element.value)
	timeout = 2000
	
	//var catDiv = document.createElement("div");
	//catDiv.innerHTML = "HELLO WORLD";
	//document.body.appendChild(catDiv);

	// Align temp input element approximately where the input element is
    // so the cursor doesn't jump around
    var fakeInput = document.createElement('input');
    fakeInput.setAttribute('type', 'text')
    fakeInput.style.position = 'absolute';
    fakeInput.style.top = (element.offsetTop + 170) + 'px';
    fakeInput.style.left = (element.offsetLeft + 170) + 'px';
    fakeInput.style.height = '20px';
    fakeInput.style.fontSize = '16px'
    //fakeInput.style.opacity = '.9';
    // Put this temp element as a child of the page <body> and focus on it
    //document.body.prepend(fakeInput)	
    document.body.appendChild(fakeInput);
    fakeInput.focus();
    
    // The keyboard is open. Now do a delayed focus on the target element
    setTimeout(function() {
    	element.focus();
    	element.click();
      // Remove the temp element
      document.body.removeChild(fakeInput);
    }, timeout);
    
}


function changeInput(name, imdbMovieId, dataFormat) {
	var boxName = name + "_" + imdbMovieId;
	//alert('In changeInput, name=' + name + ', imdbMovieId=' + imdbMovieId + ', dataFormat=' + dataFormat)
	var value = document.getElementById(boxName).value;

	//alert('In changeInput, name=' + name + ', imdbMovieId=' + imdbMovieId + ', dataFormat=' + dataFormat + ', value=' + value)
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
	//alert("changeSettingsDisplayInput(): name=" + name + ", colAttribute=" + colAttribute)
	
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

function allCast(tt) {
	  //alert('get all cast')
	  
	  var div = document.getElementById('div_' + tt + '_cast')
	  
	  $.post('allCast', {
	    	tt: tt
	    }).done(function(response) {
	    	//alert(response)
	    	div.innerHTML = response
	    }).fail(function() {
	        alert("changeSettingsDisplayInput(): Unexpected Failure")
	    });
	
}


function addMovie(displayType, tt) {
	//alert('addMovie(): displayType=' + displayType + ', tt=' + tt)

	spinner = document.getElementById('spinner_' + tt + '_' + displayType);
	button = document.getElementById('button_' + tt + '_' + displayType);
	
	button_seen = document.getElementById('button_' + tt + '_seen');
	button_want = document.getElementById('button_' + tt + '_want');
	button_imdb = document.getElementById('button_' + tt + '_imdb');
	
	spinner.style.display = 'inline'
	button.style.display = 'none'
		
	plot = document.getElementById('div_' + tt + '_plot');

    $.post('addMovie', {
    	displayType: displayType,
    	tt: tt
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
    

				
		if ( displayType == 'seen' ) {
			button_seen.innerHTML = "Saw this Movie";
			button_want.innerHTML = ''
				
		} else if ( displayType == 'want' ) {
			button_want.innerHTML = 'Movie on\nWatch List'
			
		} else if (displayType = 'imdb') {
			button_imdb.innerHTML = 'Movie Added to Imdb'
		}
    		
		spinner.style.display = 'none'
		button.style.display = 'inline'
    	
    }).fail(function() {
        alert("addMovie(): Unexpected Failure")
    });
  
}



function refreshAdder(tt, what) {
	//alert('refreshAdder starts, tt=' + tt + ", what=" + what)
	
	div = document.getElementById('div_' + tt + '_' + what);
	spinner = document.getElementById('spinner_' + tt + '_' + what);
	tbl = document.getElementById('tbl_' + tt + '_' + what);
	getbtn = document.getElementById('getbtn_' + tt + '_' + what);
	
	spinner.style.display = 'inline'
	tbl.style.display = 'none'
		
    $.post('refreshAdder', {
    	tt: tt,
    	what: what
    }).done(function(response) {
    	spinner.style.display = 'none'
    	tbl.style.display = 'inline'
    	getbtn.style.display = 'none'
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



function upCol(colName, displayType) {
	var url = 'settings_display_upCol?name=' + colName + '&displayType=' + displayType
	//alert("url=" + url)
	window.open(url, "_self");
}

function dnCol(colName, displayType) {
	var url = 'settings_display_dnCol?name=' + colName + '&displayType=' + displayType
	//alert("url=" + url)
	window.open(url, "_self");
}

function resetCol(colName, displayType) {
	var r = confirm("Are you sure you want to reset column '" + colName + "'?");
	if (r == false) {
		return;
	}
	
	
	var url = 'settings_display_resetCol?name=' + colName + '&displayType=' + displayType
	//alert("url=" + url)
	window.open(url, "_self");
}

function resetSort(displayType) {
	var r = confirm("Are you sure you want to reset all column sorts?");
	if (r == false) {
		return;
	}
	
	
	var url = 'settings_display_resetSort?displayType=' + displayType
	//alert("url=" + url)
	window.open(url, "_self");
}

function resetAll(displayType) {
	var r = confirm("Are you sure you want to reset all column displays?");
	if (r == false) {
		return;
	}
	
	var url = 'settings_display_resetAll?displayType=' + displayType 
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
	var url = 'movieSeen?tt=' + tt
	//alert("url=" + url)
	window.open(url, "entryWindow", "height=700,width=600,menubar=no,location=no");	
	
}


function backToOpener(url, rule) {
	//alert('9 rule=' + rule)
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





