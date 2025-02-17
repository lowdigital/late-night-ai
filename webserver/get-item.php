<?php
    header('Content-Type: application/json; charset=utf-8');
	include ('options.php');
	include ('dbconnect.php');
    
    $counter = 0;
	$query = "SELECT * FROM `topics_suggested` ORDER BY `priority` DESC LIMIT 1";
    if ($result = $link->query($query)) {
        while ($row = $result->fetch_assoc()) {
            $counter++;
            $item = $row;
        }
    }
    
    if ($counter == 1){
        $query = "DELETE FROM `topics_suggested` WHERE `id` = " . $item['id'];
        $link->query($query);
        
        $item['status'] = true;
    } else {
        $item['status'] = false;
    }
    
    echo json_encode($item);
	$link->close();