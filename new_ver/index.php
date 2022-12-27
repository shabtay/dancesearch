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
				<input type="text" id="search_term" placeholder="Type to search...">
				<div class="autocom-box">
				</div>
				<div class="icon" onclick="do_search()"><i class="fas fa-search"></i></div>
			</div>
			<div id="result_div" class="results"></div>
		</div>

		<script src="suggestions.js"></script> 
		<script src="script.js"></script> 
		<script src="js/jquery.js"></script> 
	</body>
</html>