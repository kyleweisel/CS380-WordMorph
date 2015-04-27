#
# CS 380 Homework 2
# April 27, 2015
# Kyle Weisel (weisel@drexel.edu)
#

# Execution settings
INITIAL_STATE = "beach"
FINAL_STATE = "shore"


class Rule:

    index = 0
    char = ""

    def __init__(self, index, char):
        self.index = index
        self.char = char

    def __str__(self):
        return "The rule will change the character at index " + str(self.index) + " to " + str(self.char)


class State:

    value = ""

    def isFinished(self):
        return self.value == FINAL_STATE

    def length(self):
        return len(self.value)

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        return self.value == other.value


class Dictionary:

    words = []

    def list(self):
        return self.words

    def length(self):
        return len(self.words)

    def __init__(self):
        with open('dict1000.txt') as f:
            self.words = [line.rstrip('\n') for line in f]

    def __str__(self):
        return "The dictionary has " + str(len(self.words)) + " words."


def apply_rule(rule, state):
    current_state_as_list = list(state.value)
    current_state_as_list[rule.index] = rule.char
    new_state = State(''.join(i for i in current_state_as_list))
    return new_state


def goal(state):
    return state.value == FINAL_STATE


def precondition(rule, state, dictionary):
    return True if (apply_rule(rule, state).value in dictionary.list) else False


def generate_rules(state, dictionary):

    rules = []

    for i in range(0, dictionary.length()):

        if num_matched_chars(state.value, dictionary.words[i]) == 4:

            #print "\tgenerate_rules() -> Identified possible next state: {}".format(dictionary.words[i])

            # Find the changed character
            state_as_list = list(state.value)
            match_as_list = list(dictionary.words[i])

            change_index = -1
            change_char = ""

            for j in range(0, len(state_as_list)):
                if state_as_list[j] != match_as_list[j]:
                    change_index = j
                    change_char = match_as_list[j]

            rules.append(Rule(change_index, change_char))

    #print "\tgenerate_rules() -> Generated {} rules this pass".format(len(rules))

    return rules


def describe_state(state):
    print state
    return str(state)


def describe_rule(rule):
    print rule
    return str(rule)


def num_matched_chars(a, b):
    if len(a) == len(b):
        a_list = list(a)
        b_list = list(b)
        num_matches = 0
        for i in range(0, len(a_list)):
            if a_list[i] == b_list[i]:
                num_matches += 1
        return num_matches
    else:
        return -1


def is_dead_end(state):
    return False


def flail_wildly(state):

    loops = 0
    while not (goal(state)):
        #print "Executing loop " + str(loops)
        describe_state(state)
        rules = generate_rules(state)
        #apply_rule_to_state(rules[randint(0, len(rules)-1)], state)
        #print "The new state is " + state.currentState
        loops += 1


def back_track(stateList, dictionary):

    #print "back_track() -> len(stateList) = {} ".format(len(stateList))
    #print "\tback_track() -> current state value is: {}".format(stateList[-1].value)

    DEPTH_BOUND = 1000

    currentState = stateList[-1]


    if stateList.count(currentState) > 1:
        #print '\tback_track() -> State exists more than once!  Returning FAILED-1'
        return "FAILED-1"

    if is_dead_end(currentState):
        #print '\tback_track() -> State is a dead end!  Returning FAILED-2'
        return "FAILED-2"

    if goal(currentState):
        #print '\tback_track() -> Reached goal!  Returning SUCCESS'
        return True

    if len(stateList) > DEPTH_BOUND:
        #print '\tback_track() -> State list exceeds depth bound!  Returning FAILED-3'
        return "FAILED-3"

    ruleSet = generate_rules(currentState, dictionary)

    if ruleSet == []:
        #print "\tback_track() -> Returned rule set was empty!  Returning FAILED-4"
        return "FAILED-4"

    for rule in ruleSet:
        newState = apply_rule(rule, currentState)
        #print "\tback_track() -> Generated new state value {}!".format(newState.value)
        newStateList = stateList[:]
        newStateList.append(newState)
        path = back_track(newStateList, dictionary)

        if type(path) == list:
            path.append(rule)
            return path

    #print "Returning from back_track() with FAILED-5"
    return "FAILED-5"


# This is the entry point to the application
def main():

    state = State(INITIAL_STATE)
    dictionary = Dictionary()

    stateList = []
    stateList.append(state)

    print back_track(stateList, dictionary)


main()