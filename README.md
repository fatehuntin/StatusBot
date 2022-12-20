# StatusBot
Discord bot to facilitate account sharing


# Installation
**Installation Guide is for linux**

To begin using this bot simply use 
```shell
git clone https://github.com/fatehuntin/StatusBot.git
```
Then copy and rename example_config.py to config.py
```shell
cp example_config.py config.py
```
Then install the required packages
```shell
pip install -r requirements.txt
```

# Creating the bot on discord

Go to https://discord.com/developers/applications and create a new application using the button in the top left corner next to your profile picture 

![image](https://user-images.githubusercontent.com/79415142/208758390-e0daea1f-f772-4464-993b-797506d03e8f.png)

Once the application exists, go to the "bot" pannel 

![image](https://user-images.githubusercontent.com/79415142/208758762-d499fa7e-a119-4b3c-b22f-23704cd4839a.png)

Once you have created the bot you can toggle the "Public Bot" setting as this will let people other than you add the bot to servers if they have the link

The next step is to go to the URL generator tab under "oAuth2" then select the scope bot and the following permissions (more permissions is fine but less may prevent the bot from working properly. 

![image](https://user-images.githubusercontent.com/79415142/208760255-f2fa5241-83a8-42be-8ad0-407c7ce1a0e3.png)

After you select those permissions, an url should appear below that looks similar to this ```https://discord.com/api/oauth2/authorize?client_id=[your id will be here]&permissions=264192&scope=bot```

Copy this link into a browser and then you can add the bot to any server you have permission to add bots to.



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
