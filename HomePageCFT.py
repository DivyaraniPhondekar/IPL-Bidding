import boto3,json 
import datetime

from boto3.dynamodb.conditions import Key, Attr
def lambda_handler(event, context):
    print(event)
    eid = event['eid']
    print(eid)
    
    amt = int(event['amt'])
    print(amt)
    
    now = datetime.datetime.now()
    
    current_date = now.strftime("%d-%m-20%y")
    print(current_date)
    
    
    
    dynamodb = boto3.resource('dynamodb')
    bidtbl = dynamodb.Table('Schedule')
    response = bidtbl.scan()
  
  
    items = response['Items']
    
    html = '''
<!DOCTYPE html>
<html>
<head>
<title>Bidding system</title>
<style>
	table,td,th{
    		border:1px solid black;
    }
</style>

</head>
<body>

<h1 id="para1">Welcome to Bidding System </h1>
<p></p>

<p><b>EmailId: </b> <span id="log" ></span></p>
<p><b>InitialAMT: </b><span id="pass"></span></p>

<table>
	<tr>
	
		<td>
        	Match ID	
        </td>
        
		<td>
        	Match Date	
        </td>
        
		<td >
        	Match Time	
        </td>
        <td>
        	Team1 VS Team2
        </td>
    
		<td>
        	Counter
        </td>
       
       	<td>
        	Click
        </td>
		
    </tr>
    <script>//var count_for_button=0;</script>
    <script>
    
    //var count_for_buttons=0;
    var count=0;  
    function timedisablefun(count_for_button){

document.getElementsByClassName("betting_button_class")[count_for_button].disabled = true;
  var tnow = new Date().getTime();
// alert(tnow) = 1522996202640 today 12 pm
  
  var MatchTime = document.getElementsByClassName("time2")[count_for_button].innerText;
  var splittime = MatchTime.split(":");
  
  var a = parseInt(splittime[0]);


  var z = parseInt(splittime[1])*60000;

  var b = (a-2)*3600000 + z + 1523471400771;

  var m = (a-1)*3600000 + z + 1523471400771; 
  
  var c = b - tnow;

  //count_for_buttons++;
  setTimeout(function(){ var x =setInterval(function(){
      
  }, 1000);
	myFunction() }, c); // c's value
  

 var counter  = 0;
 var timeleft = 0;
 if(c<0 && c>-3600000)
 {
   timeleft = parseInt((m - tnow)/1000);
 }
 else if (c > 0) 
 {
      timeleft = 3600;
 }
 
  //timeleft = 3600;
 function convertintosecnods(s)
 { 
    if(s>0)
    { 
 	    var min = parseInt(s/60);
        var sec = s % 60;
        return min + ":" + sec;
    }
    else
    {
        return 0;
    }
    
 }
 
 function myFunction() {
    //count_for_button++;
    if(timeleft>0)
    {
        document.getElementsByClassName("betting_button_class")[count_for_button].disabled = false;
    }    
   document.getElementsByClassName("time1")[count_for_button].innerHTML=convertintosecnods(timeleft - counter);
   // var interval = setInterval(timeIt,1000);
   
   var interval = setInterval(timeIt,1000)
   
    function timeIt(){
    	counter ++;	
   // if(convertintosecnods(timeleft - counter) > 0)
    document.getElementsByClassName('time1')[count_for_button].innerHTML=convertintosecnods(timeleft - counter);
    
   	if(timeleft == counter)
    {
    	clearInterval(interval);
		document.getElementsByClassName("betting_button_class")[count_for_button].disabled = true;
     }
     
    }
}
 }
    </script>
    '''
    
    mtchcont=0
    for i in range(len(items)):
        if(current_date == items[i]['date']):
            
            mtchcont+=1
            html = html + '''<tr><td>'''+str(items[i]['matchId']) +'''</td>
		    <td>'''+items[i]['date']+'''</td>
    
  		<td>
        	<span class="time2">'''+items[i]['time'] +'''</span>
        </td>
        <td>'''+items[i]['team1'] + ''' VS '''+ items[i]['team2'] + '''</td>
		<td>
        	Time -- <span class="time1"></span>
        </td>
			
        <td>
        	<a href = "https://s3.ap-south-1.amazonaws.com/divyaranitraining/bidPage.html?MATCHID='''+ str(items[i]['matchId']) +'''&TEAM1='''+items[i]['team1']+'''&TEAM2='''+items[i]['team2'] + '''&EID='''+eid+ '''&AMT=''' + str(amt) + ''' "><input id="myBtn" class="betting_button_class" type ="button" value="Betting"></a>
        	<script>timedisablefun(count++);</script>
        </td></tr>
        
        '''
    
    if(mtchcont==0):
        html = html + ''' <h1>No Matches for Today </h1> '''

    html= html + '''    
</table>

<script language="JavaScript">

	function getDetails()
	{
		var parameters = location.search.substring(1).split("&");

		var temp = parameters[0].split("=");
		Mail = unescape(temp[1]);

		temp = parameters[1].split("=");
		Amount = unescape(temp[1]);

		document.getElementById("log").innerHTML = Mail;
		document.getElementById("pass").innerHTML = Amount;
	    
	}
getDetails();

localStorage.setItem(1, z);
</script>

</body>
</html>
'''
    return html