<?php
	$link = mysqli_connect($mysqlHost, $mysqlUser, $mysqlPassword, $mysqlDatabase);
	if (!$link) {
		exit;
	}
	$link->query("SET NAMES 'utf8mb4'");