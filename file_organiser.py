VERSION =	1.1
# DO NOT EDIT
# Impletmented by Alex Dowsett
##################################################################

HELP 	= ['\nThis software is designed to organise sensory data files into seperate',
		   'folders where each folder contains the repeats of a test.',
		   '\nHelp:',
		   '\n\u2022 The source folder should contain all the textfiles (.txt) of sensory data.',
		   '\n\u2022 The destination folder is where the the organised files are exported.',
		   "\n\u2022 The 'Rename test name' box can be used to change a file's name or\n   experiment's name. The following text substitutions can be used:\n   '<number>', '<time>', <date>' which will be substitued appropriately\n   depending on the data within the particular text file.",
		   "\n    - If you wish to keep the original file name untick the 'Apply name change to\n       file name' checkbox.",
		   "    - If you wish to keep the original experiment name untick the 'Apply name\n       change to experiment name' checkbox.",
		   "\n\u2022 If you wish to compress the output folder as a .zip file tick the 'Compress\n    output folder' checkbox.\n"
		]

AUTHOR 	= ['\t\t\t   University of Surrey		', 
		   '\t\t               Created by Alex Dowsett		',
		]


##################################################################

from PyQt6 import QtCore, QtGui, QtWidgets
import PyQt6
import sys
import tempfile
from warnings import warn
from datetime import datetime
import os
from distutils.dir_util import copy_tree
from shutil import make_archive
import ctypes


##################################################################

images_dir = 'images/'
icon_path = images_dir+'icon.ico'
logo_path = images_dir+'logo.png'
folder_im_path = images_dir+'folder-import.png'
folder_ex_path = images_dir+'folder-export.png'
question_path = images_dir+'question.png'

##################################################################

try: # If run through PyInstaller
	icon_path = os.path.join(sys._MEIPASS, icon_path)
	logo_path = os.path.join(sys._MEIPASS, logo_path)
	folder_im_path = os.path.join(sys._MEIPASS, folder_im_path)
	folder_ex_path = os.path.join(sys._MEIPASS, folder_ex_path)
	question_path = os.path.join(sys._MEIPASS, question_path)
	myappid = u'mycompany.myproduct.subproduct.version' # arbitrary string
	ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

except AttributeError:
	pass


##################################################################

def main():

	global win
	app = QtWidgets.QApplication(sys.argv)
	app.setWindowIcon(QtGui.QIcon(icon_path))
	win = Window()
	win.show()
	sys.exit(app.exec())

##################################################################

class Window(QtWidgets.QMainWindow):
    '''Main Window.'''
    def __init__(self, parent=None):
        '''Initializer.'''
        try:
            self.isVisible()
        except RuntimeError:
            super().__init__(parent)

        # Window Config
        self.setWindowTitle("Sensor File Organiser")
        self.resize(350, 500)
        self.setFixedSize(350, 500)
        self.setWindowIcon(QtGui.QIcon(logo_path))

        self.statusBar = QtWidgets.QStatusBar(self)
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage('')

        # Fonts
        self.font = QtGui.QFont()
        self.font.setBold(True)
        self.font.setPointSize(11)

        self.font2 = QtGui.QFont()
        self.font2.setItalic(True)

        # Confirmation Button
        self.confirmB = QtWidgets.QPushButton("Convert files", self)
        self.confirmB.setGeometry(QtCore.QRect(25, 210, 300, 40))
        self.confirmB.clicked.connect(self.confirm)
        self.confirmB.setStatusTip('Confirm and export organised files to destination folder.')

		# Source Folder Widgets
        self.fileL = QtWidgets.QLabel("Select source folder:", self)
        self.fileL.setGeometry(QtCore.QRect(25, 25, 325, 25))
        self.fileL.setFont(self.font)

        self.fileE = QtWidgets.QLineEdit("Select folder containing sensor data files...", self)
        self.fileE.setGeometry(QtCore.QRect(25, 50, 300, 25))
        self.fileE.setReadOnly(True)
        self.fileE.defaultMousePressEvent = self.fileE.mousePressEvent
        self.fileE.mousePressEvent = self.file
        self.fileE.setFont(self.font2)
        self.fileE.setStatusTip('Source folder directory.')

        self.fileB = QtWidgets.QPushButton("Select Folder", self)
        self.fileB.setGeometry(QtCore.QRect(201, 75, 125, 25))
        self.fileB.clicked.connect(self.file)
        self.fileB.setStatusTip('Select a source folder containing the sensor data files.')

        self.fileI = QtWidgets.QLabel(self)
        self.fileI.setGeometry(QtCore.QRect(6, 51, 25, 25))
        self.filePixMap = QtGui.QPixmap(folder_im_path)
        self.fileI.setPixmap(self.filePixMap)

        # Destination Folder Widgets
        self.fileL2 = QtWidgets.QLabel("Select destination folder:", self)
        self.fileL2.setGeometry(QtCore.QRect(25, 110, 325, 25))
        self.fileL2.setFont(self.font)

        self.fileE2 = QtWidgets.QLineEdit(os.path.expanduser('~/Downloads').replace('\\', '/'), self)
        self.fileE2.setGeometry(QtCore.QRect(25, 135, 300, 25))
        self.fileE2.setStatusTip('Destination folder directory.')

        self.fileB2 = QtWidgets.QPushButton("Select Folder", self)
        self.fileB2.setGeometry(QtCore.QRect(201, 160, 125, 25))
        self.fileB2.clicked.connect(self.file2)
        self.fileB2.setStatusTip('Select a destination where the organised files will be exported.')

        self.fileI2 = QtWidgets.QLabel(self)
        self.fileI2.setGeometry(QtCore.QRect(6, 136, 25, 25))
        self.file2PixMap = QtGui.QPixmap(folder_ex_path)
        self.fileI2.setPixmap(self.file2PixMap)

        # Options
        self.fileL = QtWidgets.QLabel("Settings (optional):", self)
        self.fileL.setGeometry(QtCore.QRect(25, 260, 325, 25))
        self.fileL.setFont(self.font)

        self.compressC = QtWidgets.QCheckBox("Compress output folder", self)
        self.compressC.setGeometry(QtCore.QRect(30, 400, 170, 25))
        self.compressC.setStatusTip('Check this box to compress the output as a .zip file.')

        self.font3 = QtGui.QFont()
        self.font3.setPointSize(8)

        self.changeNameE = QtWidgets.QLineEdit("Day <number> <date> <time>", self)
        self.changeNameE.setGeometry(QtCore.QRect(25, 313, 300, 25))
        self.changeNameE.setStatusTip('Enter name format here.')
        self.changeNameE.setFont(self.font3)

        self.changeNameL = QtWidgets.QLabel("Rename test name:", self)
        self.changeNameL.setGeometry(QtCore.QRect(25, 290, 300, 25))

        self.changeFileNameC = QtWidgets.QCheckBox("Apply name change to file name", self)
        self.changeFileNameC.setGeometry(QtCore.QRect(50, 340, 230, 25))
        self.changeFileNameC.setStatusTip('Check to rename the text files with this format.')
        self.changeFileNameC.toggled.connect(self.checkbox)
        self.changeFileNameC.setChecked(True)

        self.changeExperimentNameC = QtWidgets.QCheckBox("Apply name change to experiment name", self)
        self.changeExperimentNameC.setGeometry(QtCore.QRect(50, 363, 250, 25))
        self.changeExperimentNameC.setStatusTip('Check to rename the experiment names with this format.')
        self.changeExperimentNameC.toggled.connect(self.checkbox)
        self.changeExperimentNameC.setChecked(True)

        # Information
        self.helpI = QtWidgets.QLabel(self)
        self.helpI.setGeometry(QtCore.QRect(328, 469, 16, 16))
        self.helpPixMap = QtGui.QPixmap(question_path)
        self.helpI.mousePressEvent = self.help
        self.helpI.setStatusTip('Click here for help and information.')
        self.helpI.setPixmap(self.helpPixMap)

        self.font4 = QtGui.QFont()
        self.font4.setPointSize(7)

        self.verL = QtWidgets.QLabel("Version: "+str(VERSION), self)
        self.verL.setGeometry(QtCore.QRect(275, 467, 50, 20))
        self.verL.setStatusTip('Software Version.')
        self.verL.setFont(self.font4)

##################################################################

    def msgbox(self, title, message, type=''):
    	msg = QtWidgets.QMessageBox(parent=self, text=message+'\n')

    	if type.casefold() == 'warning':
    		msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
    	elif type.casefold() == 'error':
    		msg.setIcon(QtWidgets.QMessageBox.Icon.Critical)
    	elif type.casefold() == 'information':
    		msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
    	else:
    		msg.setIcon(QtWidgets.QMessageBox.Icon.NoIcon)
    	if type != '':
    		title = ': ' + title
    	msg.setWindowTitle(type.capitalize() + title)
    	msg.exec()

    def checkbox(self):
        if self.changeFileNameC.isChecked() or self.changeExperimentNameC.isChecked():
        	self.changeNameE.setStyleSheet("color: black;")
        	self.changeNameE.setReadOnly(False)
        else:
        	self.changeNameE.setStyleSheet("color: gray;")
        	self.changeNameE.setReadOnly(True)


    def confirm(self):
    	dirname = self.fileE.text()
    	if dirname == "Select folder containing sensor data files...":
    		self.msgbox("Source folder not found", "Please select the source folder that contain the sensor data files.", 'warning')
    		return

    	if not os.path.exists(dirname):
    		self.msgbox("Source folder not found", "Source folder does not exist.\nPlease check if the folder directory is correct.", 'error')
    		return

    	if not os.path.exists(self.fileE2.text()):
    		self.msgbox("Destination folder not found", "Destination folder does not exist.\nPlease check if the folder directory is correct.", 'error')
    		return

    	name = self.changeNameE.text()

    	if name.strip() == '':
    		self.changeFileNameC.setChecked(False)
    		self.changeExperimentNameC.setChecked(False)

    	if (self.changeFileNameC.isChecked() or self.changeExperimentNameC.isChecked()) and not (( '<number>' in name) or  ( ('<date>' in name) and ('<time>' in name)	)	):
    		print('heelo)')
    		self.msgbox('Rename format not valid', "The new name must meet one of the following conditions to the avoid file names clashing:\n \u2022 contain '<number>'\n \u2022 contain '<time>'' and '<date>'", 'error')
    		return

    	temp = name.replace('<number>', '').replace('<date>','').replace('<time>','')
    	illegalChars = set('\/:*?"<>|')

    	if '<' in temp or '>' in temp:
    		self.msgbox('Incorrect use of angle brackets', 'Angle brackets ('<' and '>') can only be used with the following text substitution: \n\t\u2022  <number>\n\t\u2022  <time>\n\t\u2022  <date>', 'error')
    		return

    	if any((c in illegalChars) for c in temp):
    		self.msgbox('File name contains illegal characters', 'A file name cannot contain any of the following characters:\n\t\u2022  \\/:*?"<>|', 'error')
    		return


    	files = os.listdir(dirname)

    	dataFiles = []
    	for file in files:
    		dataFiles.append([DataFile(file, dirname)])
    		try:
    			dataFiles[-1].append(dataFiles[-1][0].timestamp)
    		except AttributeError:
    			return

    	dataFiles = sorted(dataFiles, key=lambda x: x[1])


    	with tempfile.TemporaryDirectory() as tmpdirname:
    		print('Created temporary directory at ', tmpdirname)
    		tmpdirname = tmpdirname.replace('\\', '/') 
    		container = datetime.now().strftime("/sensor files %d-%m-%Y %H.%M.%S/")


    		lastRepeat = 9999
    		group = 0
    		for dataFile in dataFiles:

    			if dataFile[0].repeat <= lastRepeat:
    				group += 1

    				if self.changeFileNameC.isChecked():
    					n = name.replace('<number>', str(group)).replace('<date>', dataFile[0].date.replace('/', '-')).replace('<time>', dataFile[0].time.replace(':', '.'))
    				else:
    					n = dataFile[0].fileName

    				dirname = tmpdirname + container + n + '/'
    				os.makedirs(dirname, exist_ok=True)


    			if self.changeFileNameC.isChecked():
    				n = name.replace('<number>', str(group)).replace('<date>', dataFile[0].date.replace('/', '-')).replace('<time>', dataFile[0].time.replace(':', '.'))
    			else:
    				n = dataFile[0].fileName

    			if self.changeFileNameC.isChecked():
    				destinationFile = dirname + n + ' Repeat {}.txt'.format(dataFile[0].repeat)
    			else:
    				destinationFile = dirname + n

    			if self.changeExperimentNameC.isChecked():
    					experimentName = name.replace('<number>', str(group)).replace('<date>', '').replace('<time>', '').strip()
    					dataFile[0].lines[dataFile[0].experimentNameIndex] = dataFile[0].experimentNamePrefix + '= "' + experimentName + '"\n'
    			f = open(destinationFile, 'w')
    			f.writelines(dataFile[0].lines)
    			f.close()

    			lastRepeat = dataFile[0].repeat

    		if self.compressC.isChecked():
    			make_archive(self.fileE2.text()+'/'+container.replace('/',''), 'zip', tmpdirname+container)
    		else:
    			copy_tree(tmpdirname, self.fileE2.text())

    	del dataFiles
    	print('Conversion complete.')
    	self.msgbox("Export complete", "Success!\n\nThe organised files have been exported to the destination folder:\t\n{}{}".format(self.fileE2.text(), container), 'information')


    def file(self, *args):
    	folder = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Source Folder Directory"))
    	if not folder:
    		return

    	self.fileE.setText(folder)
    	self.fileE.setReadOnly(False)
    	self.fileE.mousePressEvent = self.fileE.defaultMousePressEvent
    	self.font2.setItalic(False)
    	self.fileE.setFont(self.font2)

    def file2(self, *args):
    	folder = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Destination Folder Directory"))
    	if not folder:
    		return

    	self.fileE2.setText(folder)

    def help(self, *args):

    	self.msgbox("Help and information", (	'\n'.join(HELP)	)+'\n\n-------------------------------------------------------------------------------\n\n'+(	'\n'.join(AUTHOR)		)	+'\n')

##################################################################

class DataFile:
	def __init__(self, filename, dirname):

		self.fileName = filename
		self.longFileName = dirname + '/' + filename


		try:
			f = open(self.longFileName, 'r')
			lines = f.readlines()
			f.close()

			err = True
			i = 0
			for line in lines:
				if 'name' in line.casefold() and 'experiment' in line.casefold():
					try:
						temp = line.split('=')
						self.experimentNameIndex = i
						self.experimentNamePrefix = temp[0]
						err = False
					except:
						pass
					break
				i += 1

			if err and (win.changeFileNameC.isChecked() or win.changeExperimentNameC.isChecked()):
				warn('File ' + self.fileName + ': Experiment name not found.')
				win.msgbox('Experiment name not found', "Experiment name not found for file '{}'.\nAdd 'Name of the experiment =' field to this sensor text file\nin order to rename this file.\nAlternatively turn the rename options off in Settings.".format(self.fileName), 'error')
				return


			err = True
			for line in lines:
				if 'repeat' in line.casefold() and ('no' in line.casefold() or 'number' in line.casefold()):
					try:
						temp = line.split('=').pop().strip().split('/')
						self.repeat = int(temp[0])
						self.noRepeats = int(temp[1])
						err = False
					except:
						pass
					break

			if err:
				warn('File ' + self.fileName + ': Repeats not found.')
				win.msgbox('Repeats not found', "Repeats value not found for file '{}'.\nAdd 'Repeats =' field in the format 'X/Y' to this sensor text file in order to include this file.".format(self.fileName), 'error')
				return

			err = True
			for line in lines:
				if 'time' in line.casefold() and '=' in line.casefold():
					try:
						self.time = line.split('=').pop().strip()
						err = False
					except:
						pass
					break

			if err:
				warn('File ' + self.fileName + ': Time not found.')
				win.msgbox('Time not found', "Time value not found for file '{}'.\nAdd 'Time =' field in the format 'HH:MM:SS' to this sensor text file in order to include this file.".format(self.fileName), 'error')
				return

			err = True
			for line in lines:
				if 'date' in line.casefold() and '=' in line.casefold():
					try:
						self.date = line.split('=').pop().strip()
						err = False
					except:
						pass
					break

			if err:
				warn('File ' + self.fileName + ': Date not found.')
				win.msgbox('Date not found', "Date value not found for file '{}'.\nAdd 'Date =' field in the format 'DD/MM/YYYY' to this sensor text file in order to include this file.".format(self.fileName), 'error')
				return

			self.datetime = datetime.strptime((self.date + ' | ' + self.time), '%d/%m/%Y | %H:%M:%S')
			self.timestamp = self.datetime.timestamp()
			self.lines = lines


		except FileNotFoundError as e:
			warn('File ' + self.fileName + ': Unreadable file / file not found.')

##################################################################

if __name__ == "__main__":
	main()