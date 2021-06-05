#!/usr/bin/env python
# coding: utf-8

# In[2]:


# python assignment 2 ( the program will take a little long to run for the first time it is not an infinite loop)
#written by : Dhruv Mathur (31973418)
#last updated: 22/5/2021

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patch
#helper class containing formating methods for game strings
class Helper:
    def __init__(self):
        pass
    
    # method to remove any '\n' characters from the end of a string
    def removeNextLineHelper(self, string):
        try:
            i = 0
            while i < len(string):
                if string[i] == "\n":
                    break
                i += 1
            return string[:i]
        except:
            pass
       
    #method to remove any spaces from the end of the string
    def removeSpace(self, string):
        try:
            i = 0
            while i < len(string):
                if string[i] == " ":
                    break
                i += 1
            return string[:i]
        except:
            pass
     
    #method to get the both first move from a game string
    def getFirstMoveHelper(self, string):
        i = 2
        while True:
            if self.isIndexHelper(i, string):
                break;
            i += 1
        return string[2:i]
        
    # method to get index of a partciular move in a game    
    def getIndexHelper(self, j, gameStr):
        start = j
        while True:
            if gameStr[j] == '.':
                break
            j += 1
        return gameStr[start:j]
    
    # method to check if a string is an index in the game
    def isIndexHelper(self, i, gameStr):
        try:
            if i == len(gameStr):
                return True
            if gameStr[i+1] == '.' or gameStr[i+2] == '.':
                return True
            return False
        except:
            pass
    
    # method to remove the result string from the last line of each game string
    def removeResultHelper(self, lastMoves):
        i = 0
        while True:
            if i == len(lastMoves) - 1:
                return lastMoves[:i]
            if lastMoves[i + 1] == '/' or lastMoves[i + 1] == '-':
                break
            i += 1
        return lastMoves[:i]
    
# ChessAnalyzer class for the first two tasks to seprate gamestrings and divide them into 
# black and white strings
class ChessAnalyzer:
    #constructor for the class, takes one argument the pgn filename
    def __init__(self, fileName):
        self.fileName = fileName
        self.gameStrings = []
        self.number_of_games = 0
        self.helper = Helper()
        
    # Task 3.2 to filter clean game strings from each match
    def filterData(self):
        #open the dataset and read all the games from it in string fromat hen close the file
        chessFile = open(self.fileName, 'r')
        content = chessFile.readlines()
        chessFile.close()
        # initializing variable i to parse through all the different lines from the dataset
        #to extract the pure game Strings
        i = 0
        while i < len(content):
            each = content[i]
            #defining a empty string for each indivisual game String 
            gameStr = ""
            # ignoring all the metadata by checking if a line starts with '[' or ']'
            if each[0] == '[' or each[len(each)-1] == ']':
                i += 1
                continue
            #ignoring empty lines too
            elif each == '\n':
                i += 1
                continue
            # adding to the gameStr defines above the pure game Strings 
            else:
                #using another index variable j just for parsing through different lines of the 
                #pure game String
                j = i 
                #now that we are on the pure game strings we have to parse through every line 
                #untill the next 
                while content[j] != '\n':
                    # check if its the last string to stop the loop after appending it
                    if j == len(content)-1:
                        gameStr += self.helper.removeResultHelper(content[j])
                        break
                    # if the next string not a new line or blank line coninue adding to the 
                    # game String this means you are not at the last line of the game string
                    elif content[j + 1] != '\n':
                        gameStr += self.helper.removeNextLineHelper(content[j])
                        gameStr += " "
                    # when here means at the last line of the game string so remove the result
                    # at the end of the string before appending it
                    else:
                        gameStr += self.helper.removeResultHelper(content[j])
                    j += 1
                i = j + 2
                self.gameStrings.append(gameStr[:len(gameStr)-2])
        # adding the game String to the game string file 
        outputFile = open('game_string.txt', 'w')
        for each in self.gameStrings:         
            outputFile.writelines(each)
            outputFile.writelines('\n')
        outputFile.close()

    # method for task 3.3 dividing the white moves and black moves of each game into seprate files
    def subFiles(self):
        #parsing through every game string 
        for j in range(len(self.gameStrings)):
            gameStr = self.gameStrings[j]
            # starting and ending index for each game string to parse from
            start = 0
            end = len(gameStr) 
            filenameWhite = str(j+1) + 'w' + '.txt'
            filenameBlack = str(j+1) + 'b' + '.txt'
            #opening the repective filename for each game to write in
            writeFileWhite = open(filenameWhite, 'w')
            writeFileBlack = open(filenameBlack, 'w')
            # initializing game strings to append to as 'gamenwhite and 'gamenblack'
            gameWhite = 'game' + str(j+1) + 'white' + '\n'
            gameBlack = 'game' + str(j+1) + 'black' + '\n'
            # loop for extracting the first black and white move from the particular gameString
            while start < end:
                if start >= end - 2:
                    break
                tempStr = ""
                temp_list = []
                # getting move number
                num = self.helper.getIndexHelper(start, gameStr)
                playerNo = int(num)
                # initializing strings with move number 
                gameWhite += str(playerNo) + '.'
                gameBlack += str(playerNo) + '.'
                i = start + len(num) + 1 
                # looping untill the next index is reached to extract move number 1
                while not self.helper.isIndexHelper(i, gameStr):
                    tempStr += gameStr[i]
                    i += 1
                # spliting white move from black move
                temp_list = tempStr.split(" ")
                gameWhite += self.helper.removeNextLineHelper(temp_list[0]) + " "
                #checking is there is a black move 
                if len(temp_list) > 1:
                    temp = temp_list[1]
                    gameBlack += self.helper.removeNextLineHelper(temp_list[1]) + " "
                start = i
            #writing to the specific file for the game and closing them
            writeFileWhite.writelines(gameWhite)
            writeFileWhite.writelines('\n')
            writeFileBlack.writelines(gameBlack)
            writeFileBlack.writelines('\n')
            writeFileWhite.close()
            writeFileBlack.close()
        
    # Method to get the total number of games in the dataset
    def getNumberOfGames(self):
        chessFile = open(self.fileName, 'r')
        content = chessFile.readlines()
        chessFile.close()
        # initializing variable i to parse through all the different lines from the dataset
        #to extract the pure game Strings
        i = 0
        # declaring the count variable
        count = 0
        while i < len(content):
            each = content[i]
            #defining a empty string for each indivisual game String 
            gameStr = ""
            # ignoring all the metadata by checking if a line starts with '[' or ']'
            if each[0] == '[' or each[len(each)-1] == ']':
                i += 1
                continue
            #ignoring empty lines too
            elif each == '\n':
                i += 1
                continue
            else:
                #using another index variable j just for parsing through different lines of the 
                #pure game String
                j = i 
                #game strings we have to parse through every line 
                #untill the next 
                while content[j] != '\n':
                    if j == len(content)-1:
                        break
                    j += 1
                    continue
                i = j + 2
                # updating count after each game string
                count += 1
        return count
    
# ChessMove Class for counting and plotting
class ChessMoves:
    # default constructor containing class attributes
    def __init__(self, filename):
        self.totalCount = {}
        self.chess_analyzer = ChessAnalyzer(filename)
        self.helper = Helper()
    
    # method to count the number uses of all white first moves and black first moves
    # return a tuple containing the dataframes of count
    def dataframeCounts(self):
        # getting the number of games from the ChessAnalyzer class to count the first move from each
        no_of_games = self.chess_analyzer.getNumberOfGames()
        whiteFirstMoves = []
        blackFirstMoves = []
        for i in range(no_of_games):
            # opening the first move files created by ChessAnalyzer object to get the first moves 
            # from each game black and white
            white_f_file = open(str(i+1) + 'w' + '.txt', 'r')
            black_f_file = open(str(i+1) + 'b' + '.txt', 'r')
            # getting the game strings of white first moves from a particular game
            read_each = list(white_f_file.readlines())
            each = read_each[1]
            # getting the first move from white game string
            first_move = self.helper.getFirstMoveHelper(each)
            whiteFirstMoves.append(first_move)
            
            # getting the game strings of black first moves from a particular game
            read_each = list(black_f_file.readlines())
            each = read_each[1]
            # getting the first move from black game String
            first_move = self.helper.getFirstMoveHelper(each)
            blackFirstMoves.append(first_move)
            white_f_file.close()
            black_f_file.close()
        white_count = {}
        black_count = {}
        # calculating count of each white first move in each game
        for each in whiteFirstMoves:
            if each not in white_count:
                white_count[each] = 1
            else:
                white_count[each] += 1
        # calculating count of each black first move in each game
        for each in blackFirstMoves:
            # checking if there is no black move
            if each != '\n':
                if each not in black_count:
                    black_count[each] = 1
                else:
                    black_count[each] += 1
        # creating a dataframe using the above dictionarys 
        df_white = pd.DataFrame({'move':white_count.keys(), 'count':white_count.values()})
        df_black = pd.DataFrame({'move':black_count.keys(),'count':black_count.values()})
        self.totalCount = {**white_count, **black_count}
        # creating a combined count dataframe for ploting purposes
        self.totalCount = dict(sorted(self.totalCount.items(), key=lambda item: item[1], reverse = True))
        return (df_white, df_black)

    # method to plot the 10 most common moves from all first moves 
    def plotCommonMoves(self):
        # getting the count data frames
        count_tuple = self.dataframeCounts()
        white_first_moves = list(count_tuple[0]['move'])
        black_first_moves = list(count_tuple[1]['move'])
        # creating a data frame using the total count dictionary
        df_count = pd.DataFrame({'move':self.totalCount.keys(), 'counts': self.totalCount.values()})
        # taking the top 10 most used moves
        df_top10 = df_count.head(10)
        moves = df_top10['move']
        # initialisg an empty colours lsit to assign different colors to white and black
        colours = []
        # assigning different colours to white moves and black moves 
        for i in range(len(moves)):
            if moves[i] in white_first_moves:
                colours.append('orange')
            else:
                colours.append('blue')
        # plotting white and black first moves using colours list
        df_top10.plot(x = 'move', y = 'counts', kind = 'bar', color = colours, xlabel = 'MOVES', ylabel = 'COUNT', title = 'Top 10 moves')
        # assigning different legend to both colours using patch objects
        white_bars = patch.Patch(color = 'orange', label = 'white first moves')
        black_bars = patch.Patch(color = 'blue', label = 'black first moves')
        # changing the leend of the plot
        plt.legend(handles = [white_bars, black_bars])
        # same as above plotting scatter plot
        df_top10.plot(x = 'move', y = 'counts', kind = 'scatter', color = colours, xlabel = 'MOVES', ylabel = 'COUNT', title = 'Top 10 moves')
        white_bars = patch.Patch(color = 'orange', label = 'white first moves')
        black_bars = patch.Patch(color = 'blue', label = 'black first moves')
        plt.legend(handles = [white_bars, black_bars])
        
        print('From this plot we can understand that d4 is the most commonly used first move for white' + '\n'
             + 'simmilarly Nf6 is the most popular move for black' + '\n' 
              + 'g6 is the least used move in the trend')
        
        
if __name__ == '__main__':
    filename = input("Enter filename: ")
    chess = ChessAnalyzer(filename)
    # to filter game Strings
    chess.filterData()
    # to divide game string into white and black
    chess.subFiles()
    chesscount = ChessMoves(filename)
    # to count the frequency of white and black first moves
    chesscount.dataframeCounts()
    # to plot the 10 most commons moves
    chesscount.plotCommonMoves()


# In[ ]:




