import json
from pathlib import Path

import sys


class CopyTooTalk:
	"""
	This file will scan through each line of a Py file and if it finds a systemLog message or a dialog message

	--EG: self.logInfo(msg='I am some text')
	or
	self.endDialog(
			sessionId=session.sessionId,
			text=f'its now {time} oclock'
			)

	It will then copy the output text and change it to (as per above examples)
	  - self.logInfo(self.randomTalk(text="systemmessage1")) and them write that in place of the original line in the *.py file
	  of as per above example..
	  - text=self.randomTalk(text="dialogmessage2", replace=[time])

	  It will then write to the talks file the compatible json format talks dictionary.
	It will also substitue {time} for {0} (or {1} etc depending on amount of vars)
	when writing to the talks file.

	NOTE: When writing to the talks file it "appends"  to any existing json data. So you can then do what you wish
	with the talks file once written, IE: delete old data, copy over old lines, leave it as it is etc

	**To setup your run configuration in pycharm **

	1. For the script field = point it to TalkCreator.py file
	2. For paramaters field = $FilePath$ $ContentRoot$ en
	3. Working directory shoudl automatically be filed when you select the script
	4. Excecution boxes can all stay unticked
	5. oh and name it whatever, maybe talkCreator?

	**To run**

	Open a skills .py file you want to scan in pycharm. Then "run" "talkCreator"  or whatever you called it

	PS - make sure to set the correct language variable in the configuration paramaters. As per point #2 above
	it reflects en for english

	EG parmeters = $FilePath$ $ContentRoot$ en or $FilePath$ $ContentRoot$ de etc

	TIP* Excluding the msg= from a system log message will exclude it from being processed

	The script also looks for text='' not text="" or visa versa, depending on what the var self._speechSymbol is set to.
	by default it's '\"' but feel free to change it to "\'" if that's your normal writing style

	If you add "# TC <talksName>" above the line you want to convert it will use what ever <talkName> is
	 instead of calling it systemMessage1 or dialogMessage2 etc. Example

	 # TC okIwontSendMessage
	 text='ok, no worries. I wont send that message then'

	 this will become text='self.randomTalk(text="okIwontSendMessage"),'
	 rather than text='self.randomTalk(text="dialogMessage1")'

	 ** ANOTHER TIP **
	 Set self._testMode to True and you can test the output without writing to any file.
	 That way you can test before changing anything.Change back to false to write to file

	 ** And Another **
	 Make sure at minimum, your talks file has {}. A completely blank talks file will raise a error
	"""


	def __init__(self):

		self._counter = 0
		self._changesMade = False
		self._msgList = ['logInfo', 'logDebug', 'logWarning', 'logError', 'logCritical', 'logFatal']
		self._newCode = ""
		self._finalTalk = dict()
		self._extractedVarsForPYfile = list()
		self._aDialogMessage = False
		self._copyOfOriginalText = ""
		self._usingFStrings = False
		self._previousLine = ""
		self.cleanCode = ""
		self._testMode = False # set to True to not write anything, set to False to write to files
		self._speechSymbol = '\"' # set to "\'" if you normally use text='' rather than text=""

	#Create a class variable to shut sonar up
	TEXT_F_STRING = 'text=f'

	def checkForLogInfo(self):

		# Open the PY file in read mode
		with open(sys.argv[1], 'r') as reader:
			fileData = reader.read()

			# for each line of text in the PY file.....
			for position, line in enumerate(fileData.split("\n")):
				# iterate over the line looking for system and dialog messages
				if '# TC' in line:
					self._previousLine = line
				for item in self._msgList:
					if 'self.randomTalk' in line:
						print(f'Skipping this line as it looks like its already done. {line}')
						self._newCode = f'{self._newCode}\n{line}'
						break
					# if self.logInfo for example is in the line of text
					if f'self.{item}(msg=' in line:
						print("")
						print(f' Found a System message. the line is ==> {line}')
						# store that line in the global var
						self.extractTheMessage(line=line)
						break
					if 'text=' in line:
						print("")
						print(f'Found a dialog message. The line is ==> {line}')
						self._aDialogMessage = True
						self.extractTheMessage(line=line)
						break
				else:
					# if no system message or dialog message in the line, just re write the line
					self._newCode = f'{self._newCode}\n{line}'

			# go to method for writing to the py file
			self.writeTooPYFile(value=self._newCode)


	# if the line is using a msg=f'string'
	def fStringMsg(self, line, start, end, xValue):

		# grab just the msg fom that line for use with the talk File later
		textForTalkFile = line[line.find(start) + xValue + len(start):line.rfind(end)]

		# grab just the text for use with the PY file
		self._copyOfOriginalText = textForTalkFile

		return textForTalkFile


	def extractTheMessage(self, line):
		# Set a counter for adding numbers to the talksfile dicionary item
		self._counter += 1

		# look up the line for start points and grab all text after that untill  end point
		if CopyTooTalk.TEXT_F_STRING in line:
			start = CopyTooTalk.TEXT_F_STRING
			end = self._speechSymbol
		elif f'text={self._speechSymbol}' in line:
			start = 'text='
			end = f'{self._speechSymbol}'
		elif '(msg=f' in line:
			start = f'(msg=f{self._speechSymbol}'
			end = f'{self._speechSymbol})'
		elif '(msg=' in line:
			start = f'(msg={self._speechSymbol}'
			end = f'{self._speechSymbol})'
		else:
			print('OOPS, something went wrong. The line probably doesn\'t have a text string and is using a var, or your using \'\' instead of \"\" ??')
			return

		# if the line is a f string then change the start line position
		if 'msg=f' in line:
			self._usingFStrings = True
			textForTalkFile = self.fStringMsg(line=line, start=start, end=end, xValue=0)

		elif CopyTooTalk.TEXT_F_STRING in line:
			self._usingFStrings = True
			textForTalkFile = self.fStringMsg(line=line, start=start, end=end, xValue=1)

		elif f'text={self._speechSymbol}' in line:
			self._usingFStrings = False
			# if the line is not a f string and just text= then change start position to this
			textForTalkFile = line[line.find(start) + 1 + len(start):line.rfind(end)]
			self._copyOfOriginalText = textForTalkFile

		else:
			self._usingFStrings = False
			# if the line is not a f string then must be a msg= so change start position to this
			textForTalkFile = line[line.find(start) + 0 + len(start):line.rfind(end)]
			self._copyOfOriginalText = textForTalkFile
		if self._previousLine:
			self._previousLine = self._previousLine.split('TC')[1].replace(" ","")
			print(f"previous line is now {self._previousLine}")

		self.extractTheVarsFromMessage(textForTalkFile=textForTalkFile, line=line)


	def extractTheVarsFromMessage(self, textForTalkFile, line):
		# prepare needed items to extract the vars (if any) from the textForTalkFile
		i = 0
		newStart = '{'
		newEnd = '}'
		self._extractedVarsForPYfile = list()
		# store the variables in a list
		for potentialVariable in textForTalkFile.split(" "):
			# this is the complete {variableName} with brackets
			completeVariable = potentialVariable

			if '{' in potentialVariable:

				# extract the actual Potentialvariable name from between the { and the }, then add to a list
				extractedVariable = potentialVariable[potentialVariable.find(newStart) + len(newStart):potentialVariable.rfind(newEnd)].replace(" ", "")
				# add those extracted variables to a list for use with the py re writing
				self._extractedVarsForPYfile.append(extractedVariable)
				# print(f'just appended {extractedVariable} to the list = {self._extractedVarsForPYfile}')

				# change the Potentialvariable to {Number} for the talk file
				newIndexVariable = f' {i}.'.replace(" ", "{").replace(".", "}")
				newText = textForTalkFile.replace(completeVariable, newIndexVariable)
				# Copy newText back to textForTalkFile to reduce confusion
				textForTalkFile = newText
				i += 1

		self.createtheTalkFileDictionary(textForTalkFile, line=line)


	def createtheTalkFileDictionary(self, textForTalkFile, line):
		# create the talks file dictionary to be written

		if self._aDialogMessage:
			if not self._previousLine:
				key = 'systemMessage'
				self._finalTalk[f'{key}{self._counter}'] = {
					'default':
						[
							f'{textForTalkFile}'
						]
				}
			else:
				self._finalTalk[f'{self._previousLine}'] = {
					'default':
						[
							f'{textForTalkFile}'
						],
					'short':[
						""
					]
				}
		else:
			if not self._previousLine:
				key = 'dialogMessage'
				self._finalTalk[f'{key}{self._counter}'] = {
					'default':
						[
							f'{textForTalkFile}'
						],
					'short':[
						""
					]
				}
			else:
				self._finalTalk[f'{self._previousLine}'] = {
					'default':
						[
							f'{textForTalkFile}'
						],
					'short':[
						""
					]
				}
		self.createPYfileLines(textForTalkFile=textForTalkFile, line=line)


	def createPYfileLines(self, textForTalkFile, line):
		# If we have extracted vars
		replaceThisText = ""
		withThisText = ""
		elementsInList = len(self._extractedVarsForPYfile)

		# Only way i could get the var from the list without the quotes *shrug*
		cleanValuesFromList = ""
		if elementsInList > 1 and self._extractedVarsForPYfile:
			for x in self._extractedVarsForPYfile:
				cleanValuesFromList = f'{x} {cleanValuesFromList}'
			#add commas
			cleanValuesFromList = cleanValuesFromList.replace(" ", ",", elementsInList - 1)

		elif elementsInList == 1:
			cleanValuesFromList = self._extractedVarsForPYfile[0]
		else:
			cleanValuesFromList = self._extractedVarsForPYfile

		if self._extractedVarsForPYfile:
			# if the line is not a dialog message and has variables and uses a f string
			if not self._aDialogMessage and self._usingFStrings:
				replaceThisText = f'(msg=f{self._speechSymbol}{self._copyOfOriginalText}{self._speechSymbol})'
				if self._previousLine:
					withThisText = f'(self.randomTalk(text="{self._previousLine}", replace=[{cleanValuesFromList}]))'
				else:
					withThisText = f'(self.randomTalk(text="systemMessage{self._counter}", replace=[{cleanValuesFromList}]))'

			elif self._aDialogMessage and self._usingFStrings:
				# if the line is a dialog message and has variables and uses a f String
				replaceThisText = f'f{self._speechSymbol}{self._copyOfOriginalText}{self._speechSymbol}'
				if self._previousLine:
					withThisText = f'self.randomTalk(text="{self._previousLine}", replace=[{cleanValuesFromList}])'
				else:
					withThisText = f'self.randomTalk(text="dialogMessage{self._counter}", replace=[{cleanValuesFromList}])'

				# reset textInput status
				self._aDialogMessage = False

			writeThisToPYFile2 = line.replace(replaceThisText, withThisText)

			self._newCode = f'{self._newCode}\n{writeThisToPYFile2}'
			self._changesMade = True

		# If the line of code has no vars in it
		else:
			replaceThisText = ""
			withThisText = ""
			# if it's a system message without a variable in it but still a fstring
			if not self._aDialogMessage and self._usingFStrings:
				replaceThisText = f'msg=f{self._speechSymbol}{self._copyOfOriginalText}{self._speechSymbol})'
				if self._previousLine:
					withThisText = f'self.randomTalk(text="{self._previousLine}"))'
				else:
					withThisText = f'self.randomTalk(text="systemMessage{self._counter}"))'

			# if its a dialog message with no vars in it and using f strings
			elif self._aDialogMessage and self._usingFStrings:
				# if it's a dialog message without a variable in it
				replaceThisText = f'f{self._speechSymbol}{self._copyOfOriginalText}{self._speechSymbol}'
				if self._previousLine:
					withThisText = f'self.randomTalk(text="{self._previousLine}")'
				else:
					withThisText = f'self.randomTalk(text="dialogMessage{self._counter}")'

			# reset the textInput status
				self._aDialogMessage = False
			# if its a dialog message and not using f strings

			elif self._aDialogMessage and not self._usingFStrings:
				# if it's a dialog message without a variable in it
				replaceThisText = f'{self._speechSymbol}{self._copyOfOriginalText}{self._speechSymbol}'
				if self._previousLine:
					withThisText = f'self.randomTalk(text="{self._previousLine}")'
				else:
					withThisText = f'self.randomTalk(text="dialogMessage{self._counter}")'

				# reset the textInput status
				self._aDialogMessage = False

			# if its a system message and not using f strings
			elif not self._aDialogMessage and not self._usingFStrings:
				replaceThisText = f'(msg={self._speechSymbol}{self._copyOfOriginalText}{self._speechSymbol})'
				if self._previousLine:
					withThisText = f'(self.randomTalk(text="{self._previousLine}"))'
				else:
					withThisText = f'(self.randomTalk(text="dialogMessage{self._counter}"))'

			writeThisToPYFile = line.replace(replaceThisText, withThisText)
			self._previousLine = ""

			# add the modified line to a self._newCode object
			self._newCode = f'{self._newCode}\n{writeThisToPYFile}'

			# Set status of self._changesMade to reflect that there's been modifications
			self._changesMade = True

		return textForTalkFile


	# write the new line to the PY file
	def writeTooPYFile(self, value):
		# if there was no file modifications then do nothing
		if not self._changesMade:
			return
		# print the py file lines to the console. value is the current line to write
		print(value)
		# Write the lines to the actual PY file
		if not self._testMode:
			with open(sys.argv[1], 'w') as writer:
				writer.write(value)

		self.writeToTalkFile()


	# write changes to the talk file
	def writeToTalkFile(self):
		file = Path(f'{sys.argv[2]}/talks/{sys.argv[3]}.json')
		print(f"Text file path is {file}")
		if not self._testMode:
			with open(file, 'r+') as file:
				exisitingTalkData = json.load(file)
				exisitingTalkData.update(self._finalTalk)
				file.seek(0)
				json.dump(exisitingTalkData, file, sort_keys=True, ensure_ascii=False, indent=4)
		else:
			print('The Talks file will look like this')
			print('___________________________________________')
			print("")
			print(json.dumps(self._finalTalk, sort_keys=True, ensure_ascii=False, indent=4))

		self.cleanUpCode()

	def cleanUpCode(self):
		# Open the PY file in read mode
		print('Now removing all the # TC lines from the code')
		if self._testMode:
			print('Because your in test mode you wont see the self.randomTalk conversions here ')
			print('Scroll up to see those conversion. This is just showing the # TC comments removed')
		print("________________________________________")
		with open(sys.argv[1], 'r') as reader:
			fileData = reader.read()

			# for each line of text in the PY file.....
			for position, line in enumerate(fileData.split("\n")):
				# iterate over the line looking # TC comments
				if not '# TC' in line:
					self.cleanCode = f'{self.cleanCode}\n{line}'

			print(self.cleanCode)

			if not self._testMode:
				with open(sys.argv[1], 'w') as writer:
					writer.write(self.cleanCode)


copy2talk = CopyTooTalk()
copy2talk.checkForLogInfo()
