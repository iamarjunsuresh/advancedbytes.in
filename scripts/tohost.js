/*
 * This is a JavaScript Scratchpad.
 *
 * Enter some JavaScript, then Right Click or choose from the Execute Menu:
 * 1. Run to evaluate the selected text (Ctrl+R),
 * 2. Inspect to bring up an Object Inspector on the result (Ctrl+I), or,
 * 3. Display to insert the result in a comment after the selection. (Ctrl+L)
 */

// ==UserScript==
// @name        mycashkit
// @namespace   sinklecurd.asia
// @description autoquiz
// @include     http://userscripts-mirror.org/scripts/show/10583
// @include     http://www.mycashkit.com/quiz/*
// @version     1
// @grant GM_setValue
// @grant GM_getValue
// @require
// ==/UserScript==
// jQuery 1.1.3.1



var correctanswer;
var result=null;
var answerno;
var lastanswerno;

function get_answerno()
{
  answerno=null;
  
var ques=$("h5").text();
 
 var num="";
  num=num+ques[1];
  if(ques[2]!='.'){num=num+ques[2];}
 // alert("quesno"+num);
  var qno=parseInt(num);
  qno--;
  num=qno.toString();
  answerno=num;
  
  return;
  
}

function sendanswer()
{

$.post('ajax_answer.php', {
		ques_id:$('#ques_id').val(),
		ans:correctanswer,

		action:'SaveAnswer'
	}, function(response){	
	var str=unescape(response);
if(str.search('SUPERB')==-1)
{
	
	//window.location.href="http://www.mycashkit.com/quiz/index.php";

}
	else{	
$('#load_quiz').html(unescape(response));	
}			
	});
}
function getdata(url) {
  if(lastanswerno==answerno){
    console.log("no new question");
    return;}
correctanswer="";
  if($.isNumeric(answerno)==false){
    
    console.log("h5 not number");
    return;}

 console.log('myFunc is called');
if(result==null)
{
    $.get(url, function (data) {
      
      console.log ('jQuery.get worked');
      result=data;
	   correctanswer=result.data[answerno]['CORRECT_ANSWER'];
      lastanswerno=answerno;
sendanswer();
	}

     
     )
    .error ( function (respObj) {
        console.log ("Error! ", respObj.status, respObj.statusText);
    } )
    .complete ( function (respObj) {
        console.log ("AJAX Complete. Status: ", respObj.status);
    } );
}
else{

 correctanswer=result.data[answerno]['CORRECT_ANSWER'];
      lastanswerno=answerno;
sendanswer();
}
}


function doit(){
  
  console.log("running")
get_answerno();
getdata('http://www.mycashkit.com/API/quiz.api.php?action=getNextOrRunningQuiz');




}
doit();
setInterval(doit,10000);

