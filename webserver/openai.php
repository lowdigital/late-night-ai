<?php
    header('Content-Type: application/json; charset=utf-8');
    include("options.php");

	$input = file_get_contents('php://input');
	$data = json_decode($input);
	$topic = $data->topic ?? '';

	$request_data = [
		'model' => 'gpt-4o-mini',
		'messages' => [
			['role' => 'user', 'content' => $topic],
		],
		'temperature' => 0.7,
		'max_tokens' => 1000
	];
	$jsonData = json_encode($request_data);

	$options = [
		'http' => [
			'method' => 'POST',
			'header' => [
				"Content-Type: application/json",
				"Authorization: Bearer $open_ai_key"
			],
			'content' => $jsonData,
			'request_fulluri' => true,
		],
		'ssl' => [
			'verify_peer' => false,
			'verify_peer_name' => false,
		]
	];
	$context = stream_context_create($options);

	$response = file_get_contents("https://api.openai.com/v1/chat/completions", false, $context);
	echo $response;