<?php

function norm_data( $data ) {
    $index_to_del = array();
    
    $i = 0;
    while ( $i <= count( $data ) - 2 ) {
        $j = $i + 1;
        if ( ! isset( $index_to_del[$i] ) ) {
            while ( $j <= count( $data ) - 1 ) {
                if ( $results[$i]['org_name'] == $results[$j]['org_name'] ) {
                    $results[$i]['dance_type'] .= ", $results[$j]['dance_type']";
                    $index_to_del.array_unshift($j);
				}
                $j++;
			}
		}
        $i++;
    }
	
    $index_to_del = rsort( $index_to_del );
	
    $i = 0;
    while ( $i < count( $index_to_del ) ) {
        $item = $index_to_del[$i];
        $i++;
		unset( $data[$item] );
	}
	$data = array_values( $data );
		
	return( $data );
}

if( isset($_POST['search']) ) {
	$host="localhost";
	$username="root";
	$password="";
	$databasename="dance_search";
	$conn= new mysqli($host,$username,$password,$databasename);

	$search_val=$_POST['search_term'];

	$data = array();

	$get_result = $conn->query("SELECT u.url, u.image_url, u.name, u.dance_type, u.from_date, u.flocation, u.org_name, MATCH (name) AGAINST ('$search_val' IN BOOLEAN MODE) AS score FROM urls u WHERE NOW()<from_date and MATCH (name) AGAINST ('$search_val' IN BOOLEAN MODE) > 0 ORDER BY `score` DESC, from_date ASC;");
	echo "<hr />";
	while( $row=$get_result->fetch_assoc() ) {
		array_push( $data, $row );
	}
	
	$data = norm_data( $data );
	
#	while( $row=$get_result->fetch_assoc() ) {
	foreach( $data as $row ) {
		echo "<div class='result_block'>
		<div class='festival_img'><img src='".$row['image_url']."' /></div>
		<div class='text_block'>
		<a class='url'>https://dfksjd.sdfsdfs...</a><br />
		<a class='link_title' href='".$row['url']."'>".$row['org_name']."</a><br />
		<div class='details'>" . $row['flocation'] . " - " . $row['from_date'] . " - " . $row['dance_type'] . "</div>
		</div>
		</div>";
		//echo "<li><a href='".$row['url']."'><span class='title'>".$row['org_name']."</span><br><span class='desc'>".$row['flocation']." - " . $row['from_date'] . "</span></a></li>";
	}
}
?>