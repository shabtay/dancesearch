<?php 
	session_start(); 
	
	$_SESSION["search_term"] = "";
?>
<!DOCTYPE html>
<html lang="en" dir="ltr">
	<head>
		<meta charset="utf-8">
		<title>LatinFest - Your Next Dance</title>
		<link rel="stylesheet" href="style.css">
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css"/>
	</head>
	<body>
		<div class="wrapper">
			<img class="logo" src="LatinFest.png" />
			<div class="search-input">
				<a href="" target="_blank" hidden></a>
				<input type="text" id="search_term" placeholder='ex. "bachata spain", "salsa jan 2023", "madrid", "kizomba may"'>
				<div class="autocom-box">
				</div>
				<div class="icon" onclick="do_search()"><i class="fas fa-search"></i></div>
			</div>

			<div id="myBarWrapper" class="w3-light-grey" style="display:none; margin-top: 15px;">
			  <div id="myBar" class="w3-container w3-green" style="height:10px; width:15%; background-color: #5445fd!important; border-radius: 25px;"></div>
			</div>

			<div id="buttons" style="display:none; margin-top: 15px">
				<button class="btn" onclick='do_next_prev("prev")'><i class="fas fa-arrow-left"></i> Prev</button>
				<button class="btn" onclick='do_next_prev("next")'>Next <i class="fas fa-arrow-right"></i></button>
			</div>
			
			<div id="result_div" class="results"></div>
		</div>

		<script src="suggestions.js"></script> 
		<script src="script.js"></script> 
		<script src="js/jquery.js"></script> 
		<script src="js/jquery.blockUI.js"></script> 
	</body>
</html>