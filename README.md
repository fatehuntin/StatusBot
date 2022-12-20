# StatusBot
Discord bot to facilitate account sharing


# Installation
To begin using this bot simply use 
```shell
git clone https://github.com/fatehuntin/StatusBot.git
```
Then copy and rename example_config.py to config.py
```shell
cp example_config.py config.py
```

# Configuration

The config file has comments that should be enough

To get uuid's just put usernames into https://namemc.com, click on their name and copy the uuid

The api_key should be from hypixel using /api new (if you reset your api in game accidentally it will break the bot)

The KEY variable should be filled using your bot key found on the discord developper profile under bot

Both of the channel variables should be filled using channel ID's copied from discord (developper mode must be on)






![image](https://user-images.githubusercontent.com/79415142/208345831-9ad0f6e6-953f-4fbf-bd04-8588a38d0c2b.png)

# Operating 

There are many ways to run the bot but personally I use a screen ```screen -S statusbot``` then run the main.py file ```python3 main.py``` then simply detach from the screen using Ctrl + A Ctrl + D

To resume the screen to either restart or view errors if it has failed simply do ```screen -r```

If you have any problems at all feel free to dm me on discord ```Fate#8398```
