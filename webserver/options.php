<?php	
	$domain = "https://";
	$max_length = 200;
	
	# MYSQL
	$mysqlHost = 'localhost';
	$mysqlUser = '';
	$mysqlPassword = '';
	$mysqlDatabase = '';	
	
	# OPEN AI
	$open_ai_key = '';
	
	# PROXY
	$proxy_host     = "";
    $proxy_port     = "";
    $proxy_login    = "";
    $proxy_password = "";
	$proxy = "$proxy_host:$proxy_port";
	$proxy_auth = base64_encode("$proxy_login:$proxy_password");