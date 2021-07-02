<?php
	header("Access-Control-Allow-Origin:*");
	//header("Content-type:text/text");
	extract($_POST);
	$users = json_decode(file_get_contents("users.json"), true);
	
	if(isset($users[$username]))
	{
		echo "User already exists";
	}
	else
	{	

		
		$users[$username] = $password;
		//$file = fopen("users.json", "w");
		
		$str = json_encode($users);

		//fwrite($file, $str, strlen($str));
		file_put_contents("users.json",$str);

		//fclose($file);
		
		echo "1";
	}
?>