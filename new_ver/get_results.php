<?php

function norm_data( $data ) {
    $index_to_del = array();
    
    for ( $i = 0; $i <= count( $data ) - 2; $i++ ) {
        if ( ! isset( $index_to_del[$i] ) ) {
            for ( $j = $i + 1; $j <= count( $data ) - 1; $j++ ) {
                if ( $data[$i]['org_name'] == $data[$j]['org_name'] ) {
                    $data[$i]['dance_type'] = $data[$i]['dance_type'] . ", " . $data[$j]['dance_type'];
                    array_unshift( $index_to_del, $j );
				}
			}
		}
    }
	
    rsort( $index_to_del );
	
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
	while( $row = $get_result->fetch_assoc() ) {
		array_push( $data, $row );
	}

	
	$data = norm_data( $data );

	echo "<hr />";
	foreach( $data as $row ) {
		$parsed_url = parse_url( $row['url'], PHP_URL_SCHEME );
		$parsed_url .= "://" . parse_url( $row['url'], PHP_URL_HOST );

		$clean_img_url = parse_url( $row['image_url'], PHP_URL_SCHEME );
		$clean_img_url .= "://" . parse_url( $row['image_url'], PHP_URL_HOST );
		$clean_img_url .= parse_url( $row['image_url'], PHP_URL_PATH );
		
		echo "<div class='result_block'>
		<div class='festival_img'><img src='".$clean_img_url."' /></div>
		<div class='text_block'>
		<a class='url'>$parsed_url... ( ". $row['dance_type'] ." )</a><br />
		<a class='link_title' href='".$row['url']."'>".$row['org_name']."</a><br />
		<div class='details'>" . $row['flocation'] . " - " . $row['from_date'] . " - " . $row['dance_type'] . "</div>
		</div>
		</div>";
		//echo "<li><a href='".$row['url']."'><span class='title'>".$row['org_name']."</span><br><span class='desc'>".$row['flocation']." - " . $row['from_date'] . "</span></a></li>";
	}
}
?>