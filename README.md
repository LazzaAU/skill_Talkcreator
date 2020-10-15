# Talkcreator

[![Continous Integration](https://gitlab.com/project-alice-assistant/skills/skill_Talkcreator/badges/master/pipeline.svg)](https://gitlab.com/project-alice-assistant/skills/skill_Talkcreator/pipelines/latest) [![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=project-alice-assistant_skill_Talkcreator&metric=alert_status)](https://sonarcloud.io/dashboard?id=project-alice-assistant_skill_Talkcreator)

Creates the talk file for loginfo type code

- Author: Lazzaau
- Maintainers: N/A
- Alice minimum version: 1.0.0
- Languages:

  - en

**NOTE: THIS IS NOT A ALICE SKILL......**
    - This is just packaged as a skill for testing reasons.
    - to test the skill you can do the below steps on making run configurations
        then open testPY.py file and run the configuration on this file to see the outcome
        
In normal use, you would write your entire skill then run the TalkCreator script
 to create a talks file which you can then add second and third etc random lines to manually..
 This script gets rid of the boring , time consuming bits :)
  
See doc string in TalkCreator.py for more info on the skill

**To setup your run configuration in pycharm **

1. For the script field = point it to TalkCreator.py file
2. For paramaters field  = ```$FilePath$ $ContentRoot$```
3. working directory shoudl automatically be filed when you select the script
4. Excecution boxes can all stay unticked
5  oh and name it whatever, maybe ```talkCreator```?

Refer configSETUP.png if stuck
