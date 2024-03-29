from asyncio.windows_events import NULL
import random
import os

class Hangman:

    def __init__(self):
        self.attempts = 10

    def wordGuessed(self,guessValue): # Validating if the word have been guessed

        guessSoFar = ""

        for i in guessValue:
            guessSoFar += i

        return guessSoFar

    def guessingTheWord(self,wordChoiced, inputKeyboard, guessValue): # Reading the attempt letter 

        if (inputKeyboard is None): # If the game has just started
            for i in range (0, len(wordChoiced)-1):
                if (i == 0 or i == len(wordChoiced)-2):
                    if (i == 0):
                        first = wordChoiced[i]
                    if (i ==len(wordChoiced)-2):
                        last = wordChoiced[i]
                    guessValue.append(wordChoiced[i])
                else:
                    guessValue.append(' _ ')

            for i in range (0, len(wordChoiced)-1): # Validating if last or first letter repeats in the word
                if (wordChoiced[i] == first):
                    guessValue[i] = first
                if (wordChoiced[i] == last):
                    guessValue[i] = last  

            return guessValue
        else:
            flag = False
            for i in range (0, len(wordChoiced)-1): # Reading the input and validating the word
                if (inputKeyboard == wordChoiced[i]):
                    if (guessValue[i] != inputKeyboard):
                        guessValue[i] = inputKeyboard
                        flag = True

            if (flag == False):
                attempts = self.getAttempts()
                attempts = attempts-1
                self.setAttempts(attempts)

            return guessValue

    def randomWord(self):

        saveWords = []

        with open("./data.txt", "r", encoding= "utf-8") as f:
            for line in f:
                saveWords.append(line)

        randomPosition = (random.randint(0, len(saveWords)))

        choice = saveWords[randomPosition]
        
        return choice

    def interface(self,wordChoiced, inputKeyboard, guessValue):
        
        guess = self.guessingTheWord(wordChoiced, inputKeyboard, guessValue)
        attempts = self.getAttempts()

        os.system("cls")
        print ("\n")
        print ("¡¡ WELCOME TO HANGMAN GAME !!\n")
        print ("Guess the word bellow by entering letters that you think the word contains.\n")
        print ("Type EXIT if you want to stop playing. \n")
        print ("YOU HAVE " +str(attempts)+ " ATTEMPTS REMAINING \n")

        finalWord = ""
        for i in guess:
            finalWord += i

        print (finalWord)
        
        word = self.wordGuessed(guess) #Validating if already win
        wordLen = len(wordChoiced)
        wordCompare = wordChoiced.replace(wordChoiced[wordLen-1],"")
        wordCompare = wordCompare.strip()
        if (word == wordCompare):
            return 'WIN'
        if (attempts == 0): #You lose if run out of attempts
            return 'LOSE'
        else: 
            return guess

    def setAttempts(self,value):
        self.attempts = value

    def getAttempts(self):
        return self.attempts

    def run(self):

        wordChoiced = self.randomWord()
        new_sentence = wordChoiced.maketrans('áéíóú', 'aeiou')
        wordChoiced = wordChoiced.translate(new_sentence) #Eliminating special letters

        inputKeyboard = None
        guessValue = []

        while(True):
            try:
                    
                if (inputKeyboard is None or inputKeyboard.isalpha()):
                    if (inputKeyboard != None):
                        if (len(inputKeyboard)>1 and inputKeyboard != 'EXIT'):
                            inputKeyboard = input("Enter only one letter please")
                    
                    guessValue = self.interface(wordChoiced, inputKeyboard, guessValue)
                    if (guessValue == 'WIN' or guessValue == 'LOSE' or inputKeyboard == 'EXIT'):
                        break

                    inputKeyboard = input()
        
                else:
                    inputKeyboard = input("You most enter a letter")
            except AssertionError as e:
                print (e)
            except ValueError:
                print ("Letra por fa")

        if (guessValue == 'WIN'):
            os.system("cls")
            print('¡¡ YOU HAVE WON !! \n')
            print('The word was: ' + wordChoiced)
        if (guessValue == 'LOSE'):
            os.system("cls")
            print('YOU LOSE :( \n')
            print('The word was: ' + wordChoiced)


object = Hangman()
object.run()