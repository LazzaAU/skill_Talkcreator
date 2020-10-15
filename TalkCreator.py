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

	NOTE: When writing to the talks file it overwrites any existsing data so best used once you've written your initial code
	then add extra lines manually, but at least the boring parts are already done by then :)

	PS: Current code adds the variables to the Py file as strings (with quotes) and have not yet worked out
	how to remove those quotes in this situation as .stip etc seem to have no effect

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


	def checkForLogInfo(self):

		# Open the PY file in read mode
		with open(sys.argv[1], 'r') as reader:
			fileData = reader.read()

			# for each line of text in the PY file.....
			for position, line in enumerate(fileData.split("\n")):
				# iterate over the line looking for system and dialog messages
				for item in self._msgList:
					if '(text=' in line:
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
		start = ""
		end = ""
		# look up the line for (msg= and grab all text after that untill  ==> ')
		if 'text=f' in line:
			start = 'text=f'
			end = '\''
		elif 'text=\'' in line:
			start = 'text='
			end = '\''
		elif '(msg=f' in line:
			start = '(msg=f\''
			end = '\')'
		elif '(msg=' in line:
			start = '(msg=\''
			end = '\')'
		else:
			print('OOPS, something went wrong )')
			return

		# if the line is a f string then change the start line position
		if 'msg=f' in line:
			self._usingFStrings = True
			textForTalkFile = self.fStringMsg(line=line, start=start, end=end, xValue=0)

		elif 'text=f' in line:
			self._usingFStrings = True
			textForTalkFile = self.fStringMsg(line=line, start=start, end=end, xValue=1)

		elif 'text=\'' in line:
			self._usingFStrings = False
			# if the line is not a f string and just text= then change start position to this
			textForTalkFile = line[line.find(start) + 1 + len(start):line.rfind(end)]
			self._copyOfOriginalText = textForTalkFile

		else:
			self._usingFStrings = False
			# if the line is not a f string then must be a msg= so change start position to this
			textForTalkFile = line[line.find(start) + 0 + len(start):line.rfind(end)]
			self._copyOfOriginalText = textForTalkFile

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
				extractedVariable = potentialVariable[potentialVariable.find(newStart) + len(newStart):potentialVariable.rfind(newEnd)]
				# add those extracted variables to a list for use with the py re writing
				self._extractedVarsForPYfile.append(extractedVariable)
				# print(f'just appended {extractedVariable} to the list = {self._extractedVarsForPYfile}')

				# change the Potentialvariable to {Number} for the talk file
				newIndexVariable = f'{{i}}'.strip(" ")
				newText = textForTalkFile.replace(completeVariable, newIndexVariable)
				# Copy newText back to textForTalkFile to reduce confusion
				textForTalkFile = newText
				i += 1

		self.createtheTalkFileDictionary(textForTalkFile, line=line)


	def createtheTalkFileDictionary(self, textForTalkFile, line):
		# create the talks file dictionary to be written

		if not self._aDialogMessage:
			key = 'systemMessage'
		else:
			key = 'dialogMessage'

		self._finalTalk[f'{key}{self._counter}'] = {
			'default':
				[
					f'{textForTalkFile}'
				]
		}

		self.createPYfileLines(textForTalkFile=textForTalkFile, line=line)


	def createPYfileLines(self, textForTalkFile, line):
		# If we have extracted vars
		replaceThisText = ""
		withThisText = ""

		if self._extractedVarsForPYfile:
			# if the line is not a dialog message and has variables and uses a f string
			if not self._aDialogMessage and self._usingFStrings:
				replaceThisText = f'(msg=f\'{self._copyOfOriginalText}\')'
				withThisText = f'(self.randomTalk(text="systemMessage{self._counter}", replace={self._extractedVarsForPYfile}))'

			elif self._aDialogMessage and self._usingFStrings:
				# if the line is a dialog message and has variables and uses a f String
				replaceThisText = f'f\'{self._copyOfOriginalText}\''
				withThisText = f'self.randomTalk(text="dialogMessage{self._counter}", replace={self._extractedVarsForPYfile})'
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
				replaceThisText = f'msg=f\'{self._copyOfOriginalText}\')'
				withThisText = f'self.randomTalk(text="systemMessage{self._counter}"))'

			# if its a dialog message with no vars in it and using f strings
			elif self._aDialogMessage and self._usingFStrings:
				# if it's a dialog message without a variable in it
				replaceThisText = f'f\'{self._copyOfOriginalText}\''
				withThisText = f'self.randomTalk(text="dialogMessage{self._counter}")'
				# reset the textInput status
				self._aDialogMessage = False
			# if its a dialog message and not using f strings

			elif self._aDialogMessage and not self._usingFStrings:
				# if it's a dialog message without a variable in it
				replaceThisText = f'\'{self._copyOfOriginalText}\''
				withThisText = f'self.randomTalk(text="dialogMessage{self._counter}")'
				# reset the textInput status
				self._aDialogMessage = False

			# if its a system message and not using f strings
			elif not self._aDialogMessage and not self._usingFStrings:
				replaceThisText = f'(msg=\'{self._copyOfOriginalText}\')'
				withThisText = f'(self.randomTalk(text="dialogMessage{self._counter}"))'

			writeThisToPYFile = line.replace(replaceThisText, withThisText)

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
		with open(sys.argv[1], 'w') as writer:
			writer.write(value)

		self.writeToTalkFile()


	# write changes tot he talk file
	def writeToTalkFile(self):
		talksFilePath = Path(f'{sys.argv[2]}/talks/en.json')

		with open(talksFilePath, 'w') as writer:
			json.dump(self._finalTalk, writer, sort_keys=True, ensure_ascii=False, indent=4)


copy2talk = CopyTooTalk()
copy2talk.checkForLogInfo()
