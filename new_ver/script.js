// getting all required elements
const searchWrapper = document.querySelector(".search-input");
const inputBox = searchWrapper.querySelector("input");
const suggBox = searchWrapper.querySelector(".autocom-box");
const icon = searchWrapper.querySelector(".icon");
let linkTag = searchWrapper.querySelector("a");
let webLink;

inputBox.addEventListener( "keypress", function( event ) {
	if (event.key === "Enter") {
		do_search();
	}
} );

// if user press any key and release
inputBox.onkeyup = (e)=>{
	return;
    let userData = e.target.value; //user enetered data
    let emptyArray = [];
    if(userData){
        icon.onclick = ()=>{
			do_search();
        }
        emptyArray = suggestions.filter((data)=>{
            //filtering array value and user characters to lowercase and return only those words which are start with user enetered chars
            //return data.toLocaleLowerCase().startsWith(userData.toLocaleLowerCase());
            return ( data.toLocaleLowerCase().search(userData.toLocaleLowerCase()) >= 0 ) ? true : false;
        });
        emptyArray = emptyArray.map((data)=>{
            // passing return data inside li tag
            return data = `<li>${data}</li>`;
        });
        searchWrapper.classList.add("active"); //show autocomplete box
        showSuggestions(emptyArray);
        let allList = suggBox.querySelectorAll("li");
        for (let i = 0; i < allList.length; i++) {
            //adding onclick attribute in all li tag
            allList[i].setAttribute("onclick", "select(this);do_search()");
        }
    }else{
        searchWrapper.classList.remove("active"); //hide autocomplete box
    }
}

function select(element){
    let selectData = element.textContent;
    inputBox.value = selectData;
    icon.onclick = ()=>{
		do_search();
    }
    searchWrapper.classList.remove("active");
}

function showSuggestions(list){
    let listData;
    if(!list.length){
        userValue = inputBox.value;
        listData = `<li>${userValue}</li>`;
    }else{
      listData = list.join('');
    }
    suggBox.innerHTML = listData;
}

function do_search( action ) {
	var search_term = $("#search_term").val();

	$.blockUI({ message: null }); 
	$.ajax( {
		type:'post',
		url:'get_results.php',
		data:{
			search:"search",
			search_term:search_term
		},
		success:function(response) {
			if ( response != "" ) {
				$("#buttons").show();
				$("#buttons2").show();
			}
			$("#result_div").html( response );
			setTimeout( $.unblockUI, 100 );
		}
	} );
 
	return false;
}

function do_next_prev( ac ) {
	var search_term = $("#search_term").val();
	$.blockUI({ message: null }); 

	$.ajax( {
		type:'post',
		url:'get_results.php',
		data:{
			search: "search",
			search_term: search_term,
			action: ac
		},
		success:function(response) {
			$("#result_div").html( response );
			$.unblockUI();
		}
	} );
 
	return false;}

function move() {	
	var elem = document.getElementById("myBar");
	var width = 1;
	var id = setInterval(frame, 1);
	
	function frame() {
		if (width >= 100) {
			clearInterval(id);
			$("#myBarWrapper").hide();
		} else {
		  width += 1;
		  elem.style.width = width + '%';
		}
	}
}

function disable_next( val ) {
	$("#btn_next1").prop('disabled', val);
	$("#btn_next2").prop('disabled', val);
}

function disable_prev( val ) {
	$("#btn_prev1").prop('disabled', val);
	$("#btn_prev2").prop('disabled', val);
}