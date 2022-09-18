# Talkcreator

[![Continous Integration](https://gitlab.com/project-alice-assistant/skills/skill_Talkcreator/badges/master/pipeline.svg)](https://gitlab.com/project-alice-assistant/skills/skill_Talkcreator/pipelines/latest) [![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=project-alice-assistant_skill_Talkcreator&metric=alert_status)](https://sonarcloud.io/dashboard?id=project-alice-assistant_skill_Talkcreator)

Creates the talk file for loginfo type code

- Author: Lazza
- Maintainers: N/A
- Alice minimum version: 1.0.0
- Languages:

  - en

**NOTE: THIS IS NOT A ALICE SKILL......**
    - This is just packaged as a skill for testing reasons.
    - To test the skill you can do the below steps on making run configurations
        then open testPY.py file and run the configuration on this file to see the outcome
        
In normal use, you would write your entire skill then run the TalkCreator script
 to create a talks file which you can then add second and third etc. random lines too manually.
 This script gets rid of the boring , time-consuming bits :)

**Second NOTE**

 - **this code "SHOULD" append data to your Talks file. So with a clean talks file you'll get a clean listing in the 
 talks file. With existing data in the json file you'll get the new data appended at the start of the file
  and the old talk data towards the end. That way you can still manually modify the json data if needed

See doc string in TalkCreator.py for more info on the skill

**To set up your run configuration in pycharm **


1. For the script field = point it to TalkCreator.py file
2. For paramaters field  = ```$FilePath$ $FileDir$ en``` #NOTE: replace en with your default language file IE: de or fr etc
3. Working directory shoudl automatically be filed when you select the script
4. Excecution boxes can all stay unticked
5. Oh! and name it whatever, maybe ```talkCreator```?

Refer configSETUP.png if stuck.

Extra Tip....

- Run this code to push existing System Log messages to the talks file
- Then use the translator skill to translate your System Log messages to other languages
- Now the world gets to read System Logs in their natural language :)

### New Features

1. If you add "# TC *talksName*" above the line you want to convert, it will use 
what ever <talkName> is instead of calling it systemMessage1 or dialogMessage2 etc.

Example

    ```
	 # TC okIwontSendMessage
	 text='ok, no worries. I wont send that message then'
    ```
this will become text='self.randomTalk(text="okIwontSendMessage"),'
 rather than text='self.randomTalk(text="dialogMessage1")'

2. In the TalkCreator.py file set self._testMode to True to run the talkCreator 
without actually writing to any file. You can then see the output in pycharms
run console to confirm it will write as expected.

3. Set self._speechSymbol to "\'" if you normally write your code like text='this is my message'
set it to '\"' if you usually write your code like text="this is my message"

