
$(document).ready(function(){
	console.log('Document is ready')


	//Show Dropdown Options:
	function dropdwnFunc() {
	  document.getElementById("myDropdown").classList.toggle("show");
	}

	// Close the dropdown menu if the user clicks outside of it
	window.onclick = function(event) {
	  if (!event.target.matches('.dropbtn')) {
	    var dropdowns = document.getElementsByClassName("dropdown-content");
	    var i;
	    for (i = 0; i < dropdowns.length; i++) {
	      var openDropdown = dropdowns[i];
	      if (openDropdown.classList.contains('show')) {
	        openDropdown.classList.remove('show');
	      }
	    }
	  }
	}
	

	// append column to the HTML table
	function addColumn() {
	    var tbl = document.getElementById('meal_table'), // table reference
	        i;
	    // open loop for each row and append cell
	    for (i = 0; i < tbl.rows.length; i++) {
	        createCell(tbl.rows[i].insertCell(tbl.rows[i].cells.length), 'Add Ing', 'col');
	    }
	}

	// create DIV element and append to the table cell
	function createCell(cell, text, style) {
	    var div = document.createElement('div'), // create DIV element
	        txt = document.createTextNode(text); // create text node
	    div.appendChild(txt);                    // append text node to the DIV
	    div.setAttribute('class', style);        // set DIV class attribute
	    div.setAttribute('className', style);    // set DIV class attribute for IE (?!)
	    cell.appendChild(div);                   // append DIV to the table cell
	}

	function deleteColumn(tblId)
	{
		var allRows = document.getElementById(tblId).rows;
		for (var i=0; i<allRows.length; i++) {
			if (allRows[i].cells.length > 1) {
				allRows[i].deleteCell(-1);
			}
		}
	}


	// Add meal column
	$("#addMealCol").click(async function(){
		console.log('add column button clicked')
		addColumn();

	})


	// Add meal column
	$("#dropbtn").click(async function(){
		console.log('dropdown btn was clicked')
		dropdwnFunc();
	})






})








