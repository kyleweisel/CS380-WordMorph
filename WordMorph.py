class Rule:

    index = 0
    char = ""

    def __init__(self, index, char):
        self.index = index
        self.char = char

    def __str__(self):
        return "foo"


class State:

    INITIAL_STATE = "chase"
    FINAL_STATE = "catch"

    currentState = ""
    dictionary = []

    def __init__(self):
        self.currentState = self.INITIAL_STATE
        with open('dict1000.txt') as f:
            self.dictionary = [line.rstrip('\n') for line in f]
            self.currentState = self.INITIAL_STATE

    def isFinished(self):
        return self.currentState == self.FINAL_STATE


def goal(state):
    return state.isFinished()


def applyRule(rule, state):
    currentStateList = list(state.currentState)
    currentStateList[rule.index] = rule.char
    newState = ''.join(i for i in currentStateList)
    # state.currentState = newState
    return newState


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
                if stateAsList[j] == matchAsList[j]:
                    changeIndex = j
                    changeChar = matchAsList[j]

            rules.append(Rule(changeIndex, changeChar))

    return rules


def describeState(state):
    print "The current state is the word: " + str(state.currentState)


def describeRule(rule):
    print "The rule will change the character at index " + str(rule.index) + " to " + str(rule.char)


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


def main():

    state = State()
    describeState(state)

    print "New state is: " + applyRule(Rule(1, "e"), state)

main()