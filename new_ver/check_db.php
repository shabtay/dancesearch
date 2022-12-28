<?php
	$host="latinfashabtay.mysql.db";
	$username="latinfashabtay";
	$password="P0o9i8u7y6";
	$databasename="latinfashabtay";
 
	$conn= new mysqli($host,$username,$password,$databasename);
	
	$get_ts = $conn->query("SELECT DISTINCT(max(ts)) as ts FROM urls;");
	$ts = $get_ts->fetch_assoc();
	echo $ts['ts'];
?>