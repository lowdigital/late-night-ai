<?php
    header('Content-Type: application/json; charset=utf-8');
    include ('options.php');
    include ('dbconnect.php');
    
    $postData = file_get_contents('php://input');
    $data = json_decode($postData, true);
    
    $requestor_id   = $link->real_escape_string($data['requestor_id']);
    $type           = $link->real_escape_string($data['type']);
    $characters     = $link->real_escape_string(json_encode($data['characters']));
    $source         = $link->real_escape_string($data['source']);
    $user_id        = $link->real_escape_string($data['user_id']);
    $topic          = $link->real_escape_string($data['topic']);
    $topic_original = $link->real_escape_string($data['topic_original']);
    $priority       = intval($link->real_escape_string($data['priority']));
    $scenario       = $link->real_escape_string(json_encode($data['scenario']));
    
    $query = "INSERT INTO `topics_generated` (`requestor_id`, `type`, `characters`, `source`, `user_id`, `topic`, `topic_original`, `priority`, `scenario`)" .
		"VALUES ('$requestor_id', '$type', '$characters', '$source', '$user_id', '$topic', '$topic_original', '$priority', '$scenario')";
    $link->query($query);
    
    $output['success'] = true;
    echo json_encode($output);
    $link->close();