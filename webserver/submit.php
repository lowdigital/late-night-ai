<?php
	header('Content-Type: application/json; charset=utf-8');
	include ('options.php');
	include ('dbconnect.php');
	
	$postData = file_get_contents('php://input');
	$data = json_decode($postData, true);
	
	$requestor_id   = $link->real_escape_string($data['requestor_id']);
	$type 			    = 'topic';
	$source         = 'youtube';
	$user_id        = 'N/A';
	$topic          = $link->real_escape_string($data['topic']);
	$topic_original = $topic;
	$priority       = 1;
	
	$query = "INSERT INTO `topics_suggested` (`type`, `source`, `requestor_id`, `topic`, `topic_original`, `priority`)" .
		"VALUES ('$type', '$source', '$requestor_id', '$topic', '$topic_original', '$priority')";
	$link->query($query);
	
	$output['success'] = true;
	echo json_encode($output);
	$link->close();