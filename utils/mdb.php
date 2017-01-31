<?php

$dbName = $_SERVER["DOCUMENT_ROOT"] . "/php/unis.mdb";
//$dbName = "smb://172.16.16.8/C$/Program Files/UNIS/unis.mdb";

if (!file_exists($dbName)) {
    die("Could not find database file.");
}

$conn = new PDO("odbc:DRIVER=MDBTools; DBQ=$dbName; Uid='admin'; Pwd='unisamho';");

$sql  = "SELECT C_Date, C_Time, C_Unique FROM tEnter";
$sql .= " WHERE C_Date = '" . $_GET['date'] . "'";

$stmt = $conn->query($sql);
while ($row = $stmt->fetch()) {
    $output = array('date' => $row['C_Date'], 'time' => $row['C_Time'], 'unique' => $row['C_Unique']);
    echo json_encode($output);
}

?>
