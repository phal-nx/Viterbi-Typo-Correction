import sys
import string
import math

numofchars = 1
mapping = { char:value for value,char in enumerate(string.ascii_lowercase)}
reversemapping = dict(enumerate(string.ascii_lowercase))

initialprobs = [1] * 26
charactercount = [1] * 26
outputtransitions = [[1 for i in range(26)]for j in range(26)]
statetransitions = [[1 for i in range(26)]for j in range(26)]
outputprobs = [[1 for i in range(26)]for j in range(26)]
stateprobs = [[1 for i in range(26)]for j in range(26)]
maxProbabilityState = dict()
maxProbabilityOut = dict()


def getData(filename):
    global numofchars
    infile = open(filename)
    index = 0
    prevorigletter =  'd'
        #  Training loop for data
    for line in infile:  # Iterate through lines of file
        if '..' in line:  # If its the end of training data
            break
        
        words = line.split()
        if index == 0:  # If its the first char
            charactercount[mapping[words[0]]]+=1
            index+=1
        elif words[0] == '_':  # If the start of a new word
            index = 0      # Reset index
        else:   # If in the middle of a word
            statetransitions[mapping[prevorigletter]][mapping[words[0]]] += 1
            outputtransitions[mapping[words[0]]][mapping[words[1]]] += 1  
            index += 1
            #print("statetransitions[",mapping[prevorigletter],"][mapping[",words[0],"]")
        prevorigletter = words[0]
    infile.close()


def calcProbability():
    global initialprobs, charactercount, outputtransitions, statetransitions
    global outputprobs, stateprobs
    numofchars = sum(charactercount)
    # Calculate all 3 probabilities
    for row in range(0,26):
        sumofoutputrow = sum(outputtransitions[row])
        sumofstaterow = sum (statetransitions[row])
        for column in range(0,26):
            outputprobs[row][column] = math.log(outputtransitions[row][column]/sumofoutputrow)
            stateprobs[row][column] = math.log(statetransitions[row][column]/sumofstaterow)
            #print("Storing stateprobs [",row, "][",column,"] is ", math.log(statetransitions[row][column]/sumofstaterow))
        initialprobs[row] = math.log(charactercount[row]/numofchars)


def calcMaxProbability():
    global maxProbabilityOut, maxProbabilityState
    for i, character in enumerate(mapping):
        maxProbabilityState[i] = reversemapping[stateprobs[i].index(max(stateprobs[i]))]
        print(reversemapping[i], " is most likely paired with ", maxProbabilityState[i])
        
        

def viterbi(filename):
    testmode=true
    viterbi = [{}]
    newOutput = ""
    prevorigletter = "b"
    for line in infile:  # Iterate through remaining lines for testing
        char= line.split[0]
        if ( '..' in line):
            testmode=true
        elif(testmode):
            if (startofword):
                newOutput += .index(max(initialprobs[mapping[char]] + outputprobs[mapping[char]]))  # Output probs is incorrect, not sure what to pass in
                
            else:
                mostLikelyChar = max( maxProbabilityState[mapping[prevorigletter]] + stateprob[prevorigletter][mapping[char]] + outputprobs[x][t])  # Taking the Max but that's a val.
                #  Unsure how to get the char to add to the new Output from the number
                newOutput += mostLikelyChar
        prevorigletter = char



def main():
    getData(sys.argv[1])
    calcProbability()
    calcMaxProbability()
    print ("The count of characters is: ", charactercount)
main()
