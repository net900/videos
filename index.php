<?php
$url = urldecode($_GET['url']);
?>
<!DOCTYPE html>
<html>
<head>
<title>PlayerJS播放器</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<meta http-equiv="X-UA-Compatible" content="IE=11" />
<meta http-equiv="Access-Control-Allow-Origin" content="*" />
<meta content="width=device-width,initial-scale=1.0,maximum-scale=1.0,user-scalable=no" id="viewport" name="viewport">
<script src="playerjs.js" type="text/javascript"></script>
<style>html,body{margin:0;padding:0;width:100%;height:100%;}
    #stats{position:fixed;top:5px;left:10px;font-size:12px;color:#fdfdfd;z-index:2147483647;text-shadow:1px 1px 1px #000, 1px 1px 1px #000}</style>
<!--新增提醒-->
<script language="javascript">
function codefans(){
var box=document.getElementById("divbox");
box.style.display="none";
}
//2秒，可以改动
setTimeout("codefans()",20000);
</script>
</head>
<body>
<div id="playerCnt" style="width:100%;height:100%;"></div>
<script>
var urls = "<?=$url?>";
var player = new Playerjs({   
    id:"playerCnt",
    autoplay : 1, 
    "file":urls,
	"poster":"",
	"title":"",
	"cuid":"<?=$url?>"
});
</script>
</body>
</html>
