from core.base.model.AliceSkill import AliceSkill
from core.dialog.model.DialogSession import DialogSession
from core.util.Decorators import IntentHandler


class Talkcreator(AliceSkill):
	"""
	Author: Lazza
	Description: Creates the talk file for newly written skills
	"""


	def __init__(self):
		self.dummy = "Who you calling a dummy ya dummy ?"
		super().__init__()


	@IntentHandler('MyIntentName')
	def testIntent(self, session: DialogSession, **_kwargs):
		self.endDialog(
			sessionId=session.sessionId,
			text=f"I heard that... {self.dummy}"
		)


	@IntentHandler('MySecondIntentName')
	def secondTestIntent(self, session: DialogSession, **_kwargs):
		self.continueDialog(
			sessionId=session.sessionId,
			text="This is dialog session without f strings and variables"
		)


	def thirdTestMethod(self, session: DialogSession, **_kwargs):
		tester = "good one"
		self.say(
			text=self.randomTalk(text='sayHelloToTalkCreator', replace=[tester]),
			deviceUid=session.deviceUid
		)


	def testLine(self):
		test = "testVar"
		test2 = 'test2'
		test3 = "test3"
		self.logInfo(msg=f"I'm a logInfo message {test}")
		self.logWarning(msg=f"Heres a warning message {test2} and {test3}")
		print('random print statement')
		self.logError(msg="Throwing a error message into the mix without F strings")
		self.logDebug(msg="Here is a debug message without f strings")
		self.logCritical(msg=f"lets write a critical message. You used {test} but {test2} should be used: error is : {test3} ")
		self.logInfo(f'lets write a Info message. without the msg= tag. The line should be ignored')

		self.logWarning(msg='This message will be display wrong in the talks file and need manual editing cause i\'m using the wrong speech marks')
		# TC iGotMyOwnHeading
		self.logInfo(msg="This one has its own heading instead of systemMessageX")
