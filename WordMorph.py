#
# CS 380 Homework 2
# April 27, 2015
# Kyle Weisel (weisel@drexel.edu)
#

# Execution settings
DEBUG = False
FINAL_STATE = "shore"
INITIAL_STATE = "beach"

from random import randint


class Rule:

    index = 0
    char = ""

    def __init__(self, index, char):
        self.index = index
        self.char = char

    def __str__(self):
        return "(" + str(self.index) + " , " + str(self.char) + ")"


class State:

    value = ""

    def is_finished(self):
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


#
# Applies a rule to a current state and then returns the new state.
#
# @type     rule:   Rule object
# @type     state:  State object
# @param    rule:   The rule to be applied to a given state.
# @param    state:  The "original" state to apply the rule to.
#
# @rtype:   State object
# @return:  A new state that is the state of the rule applied to the original state.
#
def apply_rule(rule, state):
    current_state_as_list = list(state.value)
    current_state_as_list[rule.index] = rule.char
    new_state = State(''.join(i for i in current_state_as_list))
    return new_state


#
# Implements the backtrack algorithm to find a set of rules which transform a state into the final state.
#
# @type     state_list:   A list of State objects
# @type     dictionary:  Dictionary object
# @param    state_list:   A list of state objects that represent the previous state "path".
# @param    dictionary:  An initialized dictionary object which contains words in the knowledge base.
#
# @rtype:   List of Rule objects
# @return:  A list of rule objects that need to be applied to a state in order to transform the state into the final
#           state.
#
def back_track(state_list, dictionary):

    if DEBUG:
        print "back_track() -> len(stateList) = {} ".format(len(state_list))

    path_to_here = ""
    for state in state_list:
        path_to_here += state.value + " --> "

    if DEBUG:
        print "\tback_track() -> current state list is: {}".format(path_to_here)
        print "\tback_track() -> current state value is: {}".format(state_list[-1].value)

    DEPTH_BOUND = 1000

    current_state = state_list[-1]

    if state_list.count(current_state) > 1:
        if DEBUG:
            print '\tback_track() -> State exists more than once!  Returning FAILED-1'
        return "FAILED-1"

    if is_dead_end(current_state):
        if DEBUG:
            print '\tback_track() -> State is a dead end!  Returning FAILED-2'
        return "FAILED-2"

    if goal(current_state):
        if DEBUG:
            print '\tback_track() -> Reached goal!  Returning SUCCESS'
        return []

    if len(state_list) > DEPTH_BOUND:
        if DEBUG:
            print '\tback_track() -> State list exceeds depth bound!  Returning FAILED-3'
        return "FAILED-3"

    rule_set = generate_rules(current_state, dictionary)

    if not rule_set:
        if DEBUG:
            print "\tback_track() -> Returned rule set was empty!  Returning FAILED-4"
        return "FAILED-4"

    for rule in rule_set:
        new_state = apply_rule(rule, current_state)
        if DEBUG:
            print "\tback_track() -> Generated new state value {}!".format(new_state.value)
        new_state_list = state_list[:]
        new_state_list.append(new_state)
        path = back_track(new_state_list, dictionary)

        if type(path) == list:
            path.append(rule)
            return path

    if DEBUG:
        print "Returning from back_track() with FAILED-5"
    return "FAILED-5"


#
# Describes a path of rules.
#
# @type     path:   List of Rule objects
# @param    path:   The list of rule objects to describe.
#
# @rtype:   string
# @return:  A pretty string that shows rule progression in a human-readable format.
#
def describe_path(path):

    rules_string = ""
    for rule in path:
        rules_string += describe_rule(rule) + " --> "

    rules_string += "END"

    return rules_string


#
# Describes a rule.
#
# @type     rule:   Rule object
# @param    rule:   The rule to describe.
#
# @rtype:   string
# @return:  A pretty string that describes the rule in a human-readable format.
#
def describe_rule(rule):
    if DEBUG:
        print rule
    return str(rule)


#
# Describes a state.
#
# @type     state:   State object
# @param    state:   The state to describe.
#
# @rtype:   string
# @return:  A pretty string that describes the state in a human-readable format.
#
def describe_state(state):
    if DEBUG:
        print state
    return str(state)


#
# "Flails wildly" by randomly applying rules to a state until the goal state is reached.
#
# @type     state:   State object
# @param    state:   The initial state.
#
# @rtype:   None
# @return:  None
#
def flail_wildly(state):

    loops = 0
    while not (goal(state)):
        if DEBUG:
            print "Executing loop " + str(loops)
        describe_state(state)
        rules = generate_rules(state)
        state = apply_rule(rules[randint(0, len(rules)-1)], state)
        if DEBUG:
            print "The new state is " + state.currentState
        loops += 1


#
# Checks if the passed state has reached the goal.
#
# @type     state:   State object
# @param    state:   The state to check.
#
# @rtype:   bool
# @return:  True if the state is at the goal, False otherwise.
#
def goal(state):
    return state.value == FINAL_STATE


#
# Generates a list of possible rules that can be applied to the state legally.
#
# @type     state:          State object
# @type     dictionary:     Dictionary object
# @param    state:          State for which we are to analyze possible rules.
# @param    dictionary:     An initialized dictionary object which contains words in the knowledge base.
#
# @rtype:   List of Rule objects
# @return:  A list of rule objects that can be applied to a state in order to form a new, valid state.
#
def generate_rules(state, dictionary):

    rules = []

    for i in range(0, dictionary.length()):

        if num_matched_chars(state.value, dictionary.words[i]) == 4:

            if DEBUG:
                print "\tgenerate_rules() -> Identified possible next state: {}".format(dictionary.words[i])

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

    if DEBUG:
        print "\tgenerate_rules() -> Generated {} rules this pass".format(len(rules))

    return rules


#
# Determines if we're at a dead end from the passed state.
#
# @type     state:          State object
# @param    state:          State for which we are to analyze if we are at a dead end.
#
# @rtype:   bool
# @return:  True if there are no more possible valid states, False otherwise.
#
def is_dead_end(state):
    return False


#
# Determines the number of mached characters in string a and b.
#
# @type     a:  string
# @type     b:  string
# @param    a:  String to compare.
# @param    b:  String to compare.
#
# @rtype:   number
# @return:  The number of matching characters between strings a and b.
#
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


#
# Determines the legality of a rule as applied to a state.
#
# @type     rule:       Rule object
# @type     state:      State object
# @type     dictionary: Dictionary object
# @param    rule:       The rule to be applied to a given state.
# @param    state:      The "original" state to apply the rule to.
# @param    dictionary: An initialized dictionary object which contains words in the knowledge base.
#
# @rtype:   bool
# @return:  True if the new state is legal, False otherwise.
#
def precondition(rule, state, dictionary):
    return True if (apply_rule(rule, state).value in dictionary.list) else False


#
# !!! This is the entry point to the application !!!
#
def main():

    state = State(INITIAL_STATE)
    dictionary = Dictionary()

    state_list = [state]

    path = back_track(state_list, dictionary)

    print describe_path(path)


main()