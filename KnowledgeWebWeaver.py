import ctypes, csv, datetime, sys, os, re

STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12

FOREGROUND_BLACK = 0x00 # black.
FOREGROUND_DARKBLUE = 0x01 # dark blue.
FOREGROUND_DARKGREEN = 0x02 # dark green.
FOREGROUND_DARKSKYBLUE = 0x03 # dark skyblue.
FOREGROUND_DARKPINK = 0x04 # dark PINK.
FOREGROUND_DARKPINK = 0x05 # dark pink.
FOREGROUND_DARKYELLOW = 0x06 # dark yellow.
FOREGROUND_DARKWHITE = 0x07 # dark white.
FOREGROUND_DARKGRAY = 0x08 # dark gray.
FOREGROUND_BLUE = 0x09 # blue.
FOREGROUND_GREEN = 0x0a # green.
FOREGROUND_SKYBLUE = 0x0b # skyblue.
FOREGROUND_RED = 0x0c # red.
FOREGROUND_PINK = 0x0d # pink.
FOREGROUND_YELLOW = 0x0e # yellow.
FOREGROUND_WHITE = 0x0f # white.

BACKGROUND_BLUE = 0x10 # dark blue.
BACKGROUND_GREEN = 0x20 # dark green.
BACKGROUND_DARKSKYBLUE = 0x30 # dark skyblue.
BACKGROUND_DARKPINK = 0x40 # dark PINK.
BACKGROUND_DARKPINK = 0x50 # dark pink.
BACKGROUND_DARKYELLOW = 0x60 # dark yellow.
BACKGROUND_DARKWHITE = 0x70 # dark white.
BACKGROUND_DARKGRAY = 0x80 # dark gray.
BACKGROUND_BLUE = 0x90 # blue.
BACKGROUND_GREEN = 0xa0 # green.
BACKGROUND_SKYBLUE = 0xb0 # skyblue.
BACKGROUND_PINK = 0xc0 # PINK.
BACKGROUND_PINK = 0xd0 # pink.
BACKGROUND_YELLOW = 0xe0 # yellow.
BACKGROUND_WHITE = 0xf0 # white.

# get handle
std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

def set_cmd_text_color(color, handle=std_out_handle):
    Bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
    return Bool

#reset white
def resetColor():
    set_cmd_text_color(FOREGROUND_PINK | FOREGROUND_GREEN | FOREGROUND_BLUE)

###############################################################

def FindB(wordData):
    for wordNum in range(len(wordData)):
        if wordData[wordNum] == '[b]':
            return wordNum
    return -1
        
def CalcInterval(grade, curEF, curInterval):

    nextEF = curEF - 0.8 + 0.28 * grade - 0.02 * grade * grade
    if nextEF < 1.3:
        nextEF = 1.3
    if nextEF > 2.5:
        nextEF = 2.5

    if curInterval == 0:
        nextInterval = 1
    elif curInterval == 1:
        nextInterval = 6
    else:
        nextInterval = curInterval * nextEF

    twoList = [nextEF, nextInterval]
    return twoList

def SaveFile(file, wordsData):
    wordsFile = open(file, "w", newline='', encoding='UTF-8')
    csvwriter = csv.writer(wordsFile)
    for wordData in wordsData:
        csvwriter.writerow(wordData)
    wordsFile.close()

def spellHint(spelledWord,cue):
    match = re.search(r"^[a-zA-Z'-]+$", spelledWord)
    if not match is None:
        englishWord = True
    else:
        englishWord = False

    if englishWord:
        cue = cue.strip().split()
        for itemIndex in range(len(cue)):
            word = cue[itemIndex]

            allMatched = True
            for charIndex in range(len(spelledWord)):
                if charIndex >= len(word) or spelledWord[charIndex] != word[charIndex]:
                    allMatched = False
                    break

            if charIndex / len(spelledWord) >= 0.6:
                    if allMatched and len(spelledWord) == len(word):
                        cue[itemIndex] = '~'
                    elif allMatched:
                        cue[itemIndex] = '~' + word[charIndex+1:len(word)]
                    elif len(spelledWord) <= len(word):
                        cue[itemIndex] = '~' + word[charIndex:len(word)]

        newCue = ''
        for item in cue:
            newCue = newCue + item + ' '

    else:
        spelledWordRe = re.compile(spelledWord)
        newCue = spelledWordRe.sub('~',cue)
    return newCue.strip(', ')

def PrintCue(item,cue,enter):
    if len(cue) > len(item):
        length = int(len(cue) * 1.5)
    else:
        length = int(len(item) * 1.5)
    if length > 30:
        length = 30
    set_cmd_text_color(FOREGROUND_SKYBLUE)
    print('**' * length)
    set_cmd_text_color(FOREGROUND_YELLOW)
    if enter:
        print(item.strip())
    else:
        print(item.strip(),end = '')
    print(cue)
    set_cmd_text_color(FOREGROUND_SKYBLUE)
    print('**' * length)
    resetColor()

def makeCue(wordData):
    Bposition = FindB(wordData)
    thereIsHint = True
    if Bposition == -1 and len(wordData) == 1:
        thereIsHint = False
    if Bposition != -1 and len(wordData) == 5:
        thereIsHint = False
    if thereIsHint:
        cue = ''
        for itemIndex in range(1, len(wordData)):
            if itemIndex == Bposition:
                break
            if wordData[itemIndex].strip(', ') != '':
                cue = cue + wordData[itemIndex]
                if itemIndex != Bposition - 1:
                    cue = cue + ', '
        cue = cue.strip(', ')
        return cue
    return ''

def PrintDate(day,nextRepetition):
    if day == 1:
        print('The next review date is tomorrow.')
    elif day == 2:
        print('The next review date is the day after tomorrow.')
    else:
        print('The next review date is ' + nextRepetition.strftime('%Y/%m/%d(') + str(int(day + 0.5)) + ' days later).')


set_cmd_text_color(FOREGROUND_YELLOW)
name = 'Knowledge Web Weaver'
producer = 'Author: Jerry Pan'
mail = 'MailTo: p47pan@sina.com'
version = 'v1.4 2018/10/7'
length = 50
print('*' * length)
print('*' + ' ' * int((length - 2 - len(name)) / 2) + name + ' ' * int((length - 2 - len(name)) / 2) + '*')
if length % 2 == 0:
    print('*-' * int(length / 2))
else:
    print('*-' * int((length - 1) / 2) + '*')
print('*' + ' ' * (length - 2 - len(producer)) + producer + '*')
print('*' + ' ' * (length - 2 - len(mail)) + mail + '*')
print('*' + ' ' * (length - 2 - len(version)) + version + '*')
print('*' * length)
print('Welcome to Knowledge Web Weaver!')
resetColor()

while True:
    folder = input('Your Name Please(name/exit): ')
    if folder.lower() == 'exit':
        sys.exit()
    allFiles = []
    if os.path.exists(folder):
        for folderName, subFolders, fileNames in os.walk(folder):
            for fileIndex in range(len(fileNames)):
                fileName = fileNames[fileIndex]
                if fileNames[fileIndex].endswith('.csv'):
                    allFiles.append(fileName)
                    print(str(len(allFiles)) + ': ' + fileName[0:fileName.rfind('.')])
        while True:
            resetColor()
            fileIndex = input('choose a file to review(enter the number/exit):')
            if fileIndex.lower() == 'exit':
                sys.exit()
            if fileIndex.isdecimal():
                fileIndex = int(fileIndex)
                if fileIndex > 0 and fileIndex < len(fileNames) + 1:
                    file = fileNames[fileIndex - 1]
                    break
        break
    else:
        set_cmd_text_color(FOREGROUND_PINK)
        print('No folder named ' + folder)
        resetColor()

fileName = folder + '\\' + file
wordsFile = open(fileName, encoding='UTF-8')
wordsReader = csv.reader(wordsFile)
wordsData = list(wordsReader)
wordsFile.close()

wordsForRecall = []
dateTimeFormat = '%Y/%m/%d %H:%M:%S'

for wordIndex in range(len(wordsData)):
    wordData = wordsData[wordIndex]
    if wordData == []:
        continue
    firstWord = wordData[0]
    if len(firstWord) > 0 and firstWord[0] == '\ufeff':
         wordData[0] = wordData[0][1:]
    Bposition = FindB(wordData)
    if Bposition == -1:
        wordsForRecall.append(wordIndex)
    else:
        nextRepetitionStr = wordData[Bposition + 3]
        nextRepetition = datetime.datetime.strptime(nextRepetitionStr,dateTimeFormat)
        if datetime.datetime.now() >= nextRepetition:
            wordsForRecall.append(wordIndex)


if wordsForRecall == []:
    set_cmd_text_color(FOREGROUND_PINK)
    print('Congratlations!  No items for reviewing!')
    resetColor()
    os.system('pause')
    sys.exit()
set_cmd_text_color(FOREGROUND_PINK)
if len(wordsForRecall) == 1:
    print('You have ' + str(len(wordsForRecall)) + ' item for reviewing.')
else:
    print('You have ' + str(len(wordsForRecall)) + ' items for reviewing.')
resetColor()
while True:
    groupNum = input('How many item do you want in a group?(1~50/exit)')
    if groupNum.lower() == 'exit':
        sys.exit()
    if str(groupNum).isdecimal():
        groupNum = int(groupNum)
        if groupNum > 50:
            groupNum = 50
        if groupNum < 1:
            groupNum = 1
        break

sortedWordsForRecall = []
for wordIndex in wordsForRecall:
    usedWordData = wordsData[wordIndex]
    usedBposition = FindB(usedWordData)
    biggerThanAll = True
    if usedBposition == -1:
        sortedWordsForRecall.append(wordIndex)
        biggerThanAll = False
    else:
        usedNextRepetition = datetime.datetime.strptime(usedWordData[usedBposition + 3],dateTimeFormat)
        for index in range(len(sortedWordsForRecall)):
            otherWordData = wordsData[sortedWordsForRecall[index]]
            otherBposition = FindB(otherWordData)
            if otherBposition == -1:
                sortedWordsForRecall.insert(index, wordIndex)
                biggerThanAll = False
                break
            otherNextRepetition = datetime.datetime.strptime(otherWordData[otherBposition + 3],dateTimeFormat)
            if usedNextRepetition < otherNextRepetition:
                sortedWordsForRecall.insert(index, wordIndex)
                biggerThanAll = False
                break
    if biggerThanAll:
        sortedWordsForRecall.append(wordIndex)

if len(sortedWordsForRecall)%groupNum == 0:
    groups = int(len(sortedWordsForRecall) / groupNum)
else:
    groups = len(sortedWordsForRecall) // groupNum + 1
    
for recitedGroupNum in range(groups):
    isRepeting = False
    recitedGroup = []
    for index in range(recitedGroupNum * groupNum,(recitedGroupNum + 1) * groupNum):
        if index >= len(sortedWordsForRecall):
            break
        recitedGroup.append(sortedWordsForRecall[index])

    set_cmd_text_color(FOREGROUND_PINK)
    os.system('pause')
    set_cmd_text_color(FOREGROUND_GREEN)
    os.system('cls')
    print('=' * 15 + ' group ' + str(recitedGroupNum + 1) + ' ' + '=' * 15)
    resetColor()
    
    while True:
        needRepete = []
        for wordIndex in range(len(recitedGroup)):
            wordData = wordsData[recitedGroup[wordIndex]]
            Bposition = FindB(wordData)
            
            item = wordData[0].strip()
            set_cmd_text_color(FOREGROUND_GREEN)
            length = int(len(item) * 1.5)
            if length > 30:
                length = 30
            print('-' * 15 + ' item ' + str(recitedGroupNum + 1) + '-' + str(wordIndex + 1) + '(' + str(len(recitedGroup)) + ') ' + '-' * 15)
            set_cmd_text_color(FOREGROUND_SKYBLUE)
            print('+-' * length + '+')
            set_cmd_text_color(FOREGROUND_YELLOW)
            print(item)
            set_cmd_text_color(FOREGROUND_SKYBLUE)
            print('+-' * length + '+')
            resetColor()

            while True:
                grade = input('Grade(0~5/Exit):')
                if grade.lower() == 'exit':
                    SaveFile(fileName, wordsData)
                    sys.exit()
                if grade.isdecimal():
                    grade = float(grade)
                    break

            cue = makeCue(wordData)
            if cue != '':
                PrintCue(item,cue,True)
            
            if not isRepeting:
                if Bposition == -1:
                    twoList = CalcInterval(grade, 2.5, 0)
                    wordData.append('[b]')
                    wordData.append(twoList[0])
                    wordData.append(twoList[1])
                    nextInterval = datetime.timedelta(days = 1)
                    nextRepetition = datetime.datetime.now() + nextInterval
                    wordData.append(nextRepetition.strftime(dateTimeFormat))
                else:
                    curEF = float(wordData[Bposition + 1])
                    curInterval = float(wordData[Bposition + 2])
                    if grade < 3:
                        curInterval = 0
                    twoList = CalcInterval(grade, curEF, curInterval)
                    wordData[Bposition + 1] = twoList[0]
                    wordData[Bposition + 2] = twoList[1]
                    nextRepetition = datetime.datetime.now() + datetime.timedelta(days = twoList[1])
                    wordData[Bposition + 3] = nextRepetition.strftime(dateTimeFormat)
                    
            if grade < 4:
                needRepete.append(recitedGroup[wordIndex])
            else:
                set_cmd_text_color(FOREGROUND_PINK)
                Bposition = FindB(wordData)
                PrintDate(wordData[Bposition + 2], nextRepetition)
                
            set_cmd_text_color(FOREGROUND_PINK)
            os.system('pause')
            resetColor()
            os.system('cls')
        if len(needRepete) == 0:
            set_cmd_text_color(FOREGROUND_PINK)
            resetColor()
            break
        recitedGroup = needRepete
        isRepeting = True
        set_cmd_text_color(FOREGROUND_PINK)
        print("Repete time for this group of reviewing.")
        resetColor()
        
    while True:
        spellOrNot = input('Spell or not?(T/F/exit):')
        if spellOrNot.lower() == 'exit':
            SaveFile(fileName, wordsData)
            sys.exit()
        if spellOrNot.lower().strip() == 't':
            spellBool = True
            break
        if spellOrNot.lower().strip() == 'f':
            spellBool = False
            break
    os.system('cls')

    if spellBool:
        isRepeting = False
        recitedGroup = []
        for index in range(recitedGroupNum * groupNum,(recitedGroupNum + 1) * groupNum):
            if index >= len(sortedWordsForRecall):
                break
            recitedGroup.append(sortedWordsForRecall[index])
        
        set_cmd_text_color(FOREGROUND_PINK)
        print('Spelling of this group')
        resetColor()
        while True:
            if isRepeting:
                set_cmd_text_color(FOREGROUND_PINK)
                print('Repete time for this group of spelling')
                resetColor()
            needRepete = []
            spelledGroupLen = len(recitedGroup)
            for spelledIndex in range(len(recitedGroup)):
                spelledWordData = wordsData[recitedGroup[spelledIndex]]
                cue = makeCue(spelledWordData)
                if cue == '':
                    spelledGroupLen = spelledGroupLen - 1

            spelledIndexReal = 0        
            for spelledIndex in range(len(recitedGroup)):
                spelledWordData = wordsData[recitedGroup[spelledIndex]]
                spelledWord = spelledWordData[0]
                cue = makeCue(spelledWordData)
                if cue == '':
                    continue
                set_cmd_text_color(FOREGROUND_GREEN)
                print('-' * 15 + ' item ' + str(recitedGroupNum + 1) + '-' + str(spelledIndexReal + 1) + '(' + str(spelledGroupLen) + ') ' + '-' * 15)
                spelledIndexReal = spelledIndexReal + 1
                resetColor()
                newCue = spellHint(spelledWord, cue)
                if newCue != '':
                    PrintCue('\n',newCue,False)
                spellAnswer = input('spell/exit:')
                if spellAnswer.strip().lower() == 'exit':
                    SaveFile(fileName, wordsData)
                    sys.exit()

                Bposition = FindB(spelledWordData)
                if spellAnswer.strip().lower() != spelledWord.strip().lower():
                    set_cmd_text_color(FOREGROUND_PINK)
                    print('Oops...the correct one is “' + spelledWord + '”.')
                    resetColor()
                    needRepete.append(recitedGroup[spelledIndex])
                    
                    curEF = float(spelledWordData[Bposition + 1])
                    curInterval = float(spelledWordData[Bposition + 2])
                    nextRepetitionStr = spelledWordData[Bposition + 3]
                    nextRepetition = datetime.datetime.strptime(nextRepetitionStr,dateTimeFormat)
                    
                    if not isRepeting:
                        twoList = CalcInterval(4, curEF, 0)
                        spelledWordData[Bposition + 1] = twoList[0]
                        spelledWordData[Bposition + 2] = twoList[1]
                        nextRepetition = datetime.datetime.now() + datetime.timedelta(days = twoList[1])
                        spelledWordData[Bposition + 3] = nextRepetition.strftime(dateTimeFormat)
                else:
                    set_cmd_text_color(FOREGROUND_PINK)
                    print('Yeah, you are a genius.')
                    nextRepetition = datetime.datetime.now() + datetime.timedelta(days = float(spelledWordData[Bposition + 2]))
                    PrintDate(spelledWordData[Bposition + 2],nextRepetition)
                    resetColor()
                set_cmd_text_color(FOREGROUND_PINK) 
                os.system('pause')
                resetColor()
                os.system('cls')
            if needRepete == []:
                break
            recitedGroup = needRepete
            isRepeting = True

    SaveFile(fileName, wordsData)

set_cmd_text_color(FOREGROUND_PINK)
print('Congratulations!  Reviewing Complete!')
os.system('pause')
 
   
    
            
        
