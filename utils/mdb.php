<?php

$dbName = $_SERVER["DOCUMENT_ROOT"] . "/php/unis.mdb";
//$dbName = "smb://172.16.16.8/C$/Program Files/UNIS/unis.mdb";

if (!file_exists($dbName)) {
    die("Could not find database file.");
}

$conn = new PDO("odbc:DRIVER=MDBTools; DBQ=$dbName; Uid='admin'; Pwd='unisamho';");

$sql  = "SELECT C_Date, C_Time, C_Unique FROM tEnter";
$sql .= " WHERE C_Date >= '" . $_GET['date'] . "'";

$data = array();

$stmt = $conn->query($sql);
while ($row = $stmt->fetch()) {

//    echo str_pad($row['C_Unique'], 10, "0", STR_PAD_LEFT).",";
//    echo $row['C_Date']." ".$row['C_Time']."\r";

    array_push($data, array(str_pad($row['C_Unique'], 10, '0', STR_PAD_LEFT).', '.$row['C_Date'].', '.$row['C_Time']));
}

header('Content-Type:application/json;charset=utf-8');
echo json_encode($data);

?>

