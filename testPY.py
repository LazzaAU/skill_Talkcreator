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
			text=f'I heard that... {self.dummy}',
			siteId=session.siteId
		)


	@IntentHandler('MySecondIntentName')
	def secondTestIntent(self, session: DialogSession, **_kwargs):
		self.continueDialog(
			sessionId=session.sessionId,
			text='this is not a f string dialog session'
		)


	def thirdTestmethod(self, session: DialogSession, **_kwargs):
		tester = "good one"
		self.say(
			text=self.randomTalk(text='sayHelloToTalkCreator', replace=[tester]),
			siteId=session.siteId
		)


	def testLine(self):
		test = "testVar"
		test2 = 'test2'
		test3 = "test3"
		self.logInfo(msg=f'I\'m a logInfo message {test}')
		self.logWarning(msg=f'heres a warning message {test2} and {test3}')
		print('random print statement')
		self.logError(msg='Throwing a error message into the mix')
		self.logDebug(msg='here is a debug message')
		self.logCritical(msg=f'lets write a critical message')
