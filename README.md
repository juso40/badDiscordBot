# badDiscordBot   

~~bot can do some stuff, but he's still pretty bad~~  
He can do lots of stuff now, but he's still a bad bot.  
You now can even play Pokemon using discord commands!  

## commands  
!image \<string\> - searches yahoo for the provided string, returns an embed with the best match.   
-Example: ``!image some funny dog``  

!rimage \<string\> - searches yahoo for the provided string, returns an embed with an random match.  
-Example: ``!rimage some random funny dog``     

!reddit \<string>\> - searches the provided subreddit string for a random image in its top 50 hot posts.  
-Example: ``!reddit photos``  

!d \<int\> - rolls a dice.
-Example: ``!d 42069``    

!decide \<string\> - picks a random choice provided by your string, each option should be seperated by ``;``  
-Example: ``!decide option1;option2;option3``  

!math \<string\> - evaluates the given string.  
-Example: ``!math (sin(cos(5))/20)**3``  

!code \<codeblock\> - sends a post to hackerearth.net to evaluate the codeblock.  
-Example:  
```py    
!code ```py
print("hello")```
```    

!crabravethis \<string\> - Crabraveifies your text.  
-Example: ``!crabravethis This Text will now contain many crabs``  

!emojify \<string\> - Emojifies your text.  
-Example: ``!emojify This text will now contain many emojies``  

!uwu \<string\> - Replaces all occurrences of u's and o's with OwO and UwU.  
-Example: ``!uwu This will now contain some UwU and OwO``  

!pokemon \<button\> - allows the discord chat to play pokemon on this bots pc. But VisualBoyAdvance has to be runnning and be in focus. Only tested on Windows10.  
-Example: ``!pokemon a``  
!pokemonstatus - Posts the last taken frame of the current pokemon session. Also prints out the current input buffer for the game.  



## requirements
``pip install -r requirements.txt``  
``token`` a file containing your bot token for discord as its only line  
``hackerearth`` a file containing your "client_secret" for [api.hackereath](https://api.hackerearth.com/v3/code/run/)   
```redditsecret``` a file containing your client_secret, client_id and user_agent in one line seperated by ``;``   
```VisualBoyAdvance.exe + a pokemon rom```  used for the ``!pokemon`` command. The game has to be running and be in foreground/focused.