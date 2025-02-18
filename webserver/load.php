<?php
    header('Content-Type: application/json; charset=utf-8');
	include ('options.php');
	include ('dbconnect.php');
    
    $npc = array();
    
    $counter = 0;
	$query = "SELECT * FROM `topics_generated` ORDER BY `priority` DESC LIMIT 1";
    if ($result = $link -> query($query)) {
        while ($row = $result->fetch_assoc()) {
            $counter++;
            $item = $row;
        }
    }
    
    if ($counter == 1){       
        $query = "TRUNCATE TABLE `topics_current`";
        $link->query($query);
        
        $prepeared = $item;
        foreach ($prepeared as &$prepeared_item){
            $prepeared_item = $link->real_escape_string($prepeared_item);
        }
        $query = "INSERT INTO `topics_current` (`date`, `type`, `speaker`, `priority`, `source`, `requestor_id`, `user_id`, `topic`, `topic_original`, `characters`, `scenario`, `npc`)" .
            "VALUES ('" . $prepeared['date'] . "', '" . $prepeared['type'] . "', '" . $prepeared['speaker'] . "', " . $prepeared['priority'] . ", '" . $prepeared['source'] . "', '" . $prepeared['requestor_id'] . "', '" . $prepeared['user_id'] . "', '" . $prepeared['topic'] . "', '" . $prepeared['topic_original'] . "', '" . $prepeared['characters'] . "', '" . $prepeared['scenario'] . "', '" . $prepeared['npc'] . "')";
        $link->query($query);
        
        $query = "DELETE FROM `topics_generated` WHERE `id` = " . $item['id'] . " ORDER BY `priority` DESC";
        $link->query($query);
        
        $item['status'] = true;
        $item['npc'] = $npc;
    } else {
        $item['status'] = false;
    }
    
    echo json_encode($item);
	$link->close();