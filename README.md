# Warzone_idle

This project is a IDLE bot. And IDLE bot aims to simulate activity in a game for several reasons. Here it is to gain Experience in game for people who don't have a lot of time to unlock weapons for example. Or to gain weapons Exp in specific mode. Or can be used to lower your KDA. Since Warzone is a sweaty game, some lobbies might be full of cheaters or people with very high KDA, the only solution I found to play with people of my skills is by lowering my KDA.

This program needs the game to be in main focus. For that you can not use your computer while botting.

# Disclaimer 

This project is not a cheat. It won't replace your brain and gameplay. I made this project for fun. This idle bot is against Activitions/CoD Terms of Service since it is sending keyboard keys to the game.

I do not take any responsibility for any account bans. I have no guarantee this bot is safe for you account.

## How to setup :

* Setup first the project:

    * Be sure to have Python 3 installed on your OS.

        ```shell
        $> git clone https://github.com/Uranium2/Warzone_idle
        $> cd Warzone_idle
        $> python3 -m venv .venv
        $> .venv\Script\activate
        (.venv) $> pip3 install -r requirements.txt
        ```

    * To launch :

        ```shell
        (.venv) $> python3 main.py
        ```
        The first launch might take some time since it will download and compile an OCR model on your nachine. This OCR is used to detect whenever you are in the exit menu and relaunch a new game.

* Setup Warzone_idle :

    * You need to configure yourself the localisation of `Play` button and which game mode you want to play. The reason I use this methode is that the bot can be used on any resolution on any computers. You have to set properly where to click, the bot will do the rest once configured.

    * When you configures button, a screenshot of your main screen will be made (if you play the game on a second screen, it won't detect your second screen). Then you will have to draw a rectangle on the buttons the bot needs to click.

        * The `Play` button in the one on the top left corner of your screen.

        * The `Play_mode_main_menu` button is the button that corresponds to your main game mode. BR, plunder, Cash etc.

        * The `Play_mode_sub_menu` button is the one to select a specific mode in BR for example. In BR you can be in solo, duo, trio, quad. You have to chose those types of buttons with this settings.

    * You can setup a specific loadout the bot will pickup in modes like `Punder` so you can focus the exp gain on this weapon. The loadout name has to be `Myloadout`. Sometimes it won't use it, that's why I also set it to be on top of the list AND has favourite loadout.

    * You need to set up in the game auto parachute deployement. Else you won't survive long to gain any exp. The more you stay alive, the more exp you will get at the end of the match in BR. 

    * Press `F3` to toggle on or off the bot. Make sure to select Warzone game client. Else it will send keys to wherever you pressed.

    * __Be aware.__ If you press `ENTER` in game, it will send keys in the chat.