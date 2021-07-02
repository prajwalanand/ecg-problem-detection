<?php
	header("Access-Control-Allow-Origin: *");
	extract($_GET);
	$users = json_decode(file_get_contents("users.json"), true);
	//fopen("current.txt","w");
	$str = "";
	file_put_contents("current.txt",$str);
	if(isset($users[$usr]))
	{
		if($users[$usr] == $pwd)
		{
			file_put_contents("current.txt",$usr);
			echo "1";
		}
		else
		{
			echo "Incorrect password";
		}
	}
	else
	{
		echo "User does not exist";
	}
?>