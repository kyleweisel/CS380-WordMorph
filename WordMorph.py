#
# CS 380 Homework 1
# April 11, 2015
# Kyle Weisel (weisel@drexel.edu)
#

from random import randint


class Rule:

    index = 0
    char = ""

    def __init__(self, index, char):
        self.index = index
        self.char = char

    def __str__(self):
        return "The rule will change the character at index " + str(self.index) + " to " + str(self.char)


class State:

    INITIAL_STATE = "chase"
    FINAL_STATE = "catch"

    currentState = ""
    dictionary = []

    def isFinished(self):
        return self.currentState == self.FINAL_STATE

    def __init__(self):
        self.currentState = self.INITIAL_STATE
        with open('dict1000.txt') as f:
            self.dictionary = [line.rstrip('\n') for line in f]
            self.currentState = self.INITIAL_STATE

    def __str__(self):
        return "The current state is the word: " + str(self.currentState)


def goal(state):
    return state.isFinished()


def applyRule(rule, state):
    currentStateList = list(state.currentState)
    currentStateList[rule.index] = rule.char
    newState = ''.join(i for i in currentStateList)
    return newState


def applyRuleToState(rule, state):
    state.currentState = applyRule(rule, state)


def precondition(rule, state):
    return True if (applyRule(rule, state) in state.dictionary) else False


def generateRules(state):

    rules = []

    for i in range(0, len(state.dictionary)):

        if numMatchedChars(state.currentState, state.dictionary[i]) == 4:

            # Find the changed character
            stateAsList = list(state.currentState)
            matchAsList = list(state.dictionary[i])

            changeIndex = -1
            changeChar = ""

            for j in range(0, len(stateAsList)):
                if stateAsList[j] != matchAsList[j]:
                    changeIndex = j
                    changeChar = matchAsList[j]

            rules.append(Rule(changeIndex, changeChar))

    return rules


def describeState(state):
    print state
    return str(state)


def describeRule(rule):
    print rule
    return str(rule)


def numMatchedChars(a, b):
    if len(a) == len(b):
        aList = list(a)
        bList = list(b)
        numMatches = 0
        for i in range(0, len(aList)):
            if aList[i] == bList[i]:
                numMatches += 1
        return numMatches
    else:
        return -1


def deadEnd(state):
    return False


def flailWildly(state):

    loops = 0
    while not (goal(state)):
        print "Executing loop " + str(loops)
        describeState(state)
        rules = generateRules(state)
        applyRuleToState(rules[randint(0, len(rules)-1)], state)
        print "The new state is " + state.currentState
        loops += 1


def backTrack(stateList):

    DEPTH_BOUND = 1000

    print "Executing backTrack() with list length" + str(len(stateList))

    currentState = stateList[-1]

    if stateList.count(currentState) > 1:
        return "FAILED-1"

    if deadEnd(currentState):
        return "FAILED-2"

    if goal(currentState):
        return None

    if len(stateList) > DEPTH_BOUND:
        return "FAILED-3"

    ruleSet = generateRules(currentState)
    print "\tEGenerated this many rules: " + str(len(ruleSet))

    if ruleSet == []:
        return "FAILED-4"

    for rule in ruleSet:
        ##newState = applyRule(rule, currentState)

        applyRuleToState(rule, currentState)

        stateList.append(currentState)
        path = backTrack(stateList)

        if type(path) == list:
            path.append(rule)
            return path

    return "FAILED-5"

# This is the entry point to the application
def main():

    state = State()
    stateList = []
    stateList.append(state)
    #flailWildly(state)
    backTrack(stateList)

    print "Final state is " + str(stateList[-1].currentState)


main()