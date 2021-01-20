# badDiscordBot  
bot can do some stuff, but he's still pretty bad  

## commands  
!image \<string\> - searches yahoo for the provided string, returns an embed with the best match.   
!rimage \<string\> - searches yahoo for the provided string, returns an embed with an random match.   
!d \<int\> - rolls a dice.  
!math \<string\> - evaluates the given string.
!code \<codeblock\> - sends a post to hackerearth.net to evaluate the codeblock.

## requirements
``pip install -r requirements.txt``  
``token`` a file containing your bot token for discord as its only line  
``hackerearth`` a file containing your "client_secret" for [api.hackereath](https://api.hackerearth.com/v3/code/run/)