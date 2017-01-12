<?php

$servername = "172.16.16.3";
$username = "erp";
$password = "eerr123#";
$dbname = "dbilldb";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$sql = "SELECT credit FROM cc_card WHERE username = ".$_GET['query'." LIMIT 1"];
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    // output data of each row
    while($row = $result->fetch_assoc()) {
	$output = array('balance' => $row['credit']);
	echo json_encode($output);
    }
} else {
    $output = array('balance' => 'Unavailable');
    echo json_encode($output);
}

$conn->close();

?>
