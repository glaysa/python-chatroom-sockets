import responses
import random
import re

# Reactions
u = 'neutral'
p = 'positive'
n = 'negative'
r = [u, p, n]

debug = False

# Placeholder that is replaced with an action suggested by other clients
keyword_to_replace1 = kwtr1 = responses.kwtr1
# Placeholder that is replaced with an action suggested by the current bot
keyword_to_replace2 = kwtr2 = responses.kwtr2
# Placeholder that is replaced with an action suggested by the host
keyword_to_replace3 = kwtr3 = responses.kwtr3

# Actions suggested by other clients
suggested_actions = []
# New set of actions suggested by the current bot
new_actions = []
# Alias of a bot
alias = ''

# var choices = actions the bot can suggest,
# manipulated so that the current bot doesn't suggest the same action as the previous suggested action
# List manipulation necessary because all 'bots' are sharing the same list of actions (see responses.py -> bot_actions[])
choices = [x for x in responses.bot_actions]

# The bot() function can be reused
# You can create multiple clients with this bot
# as long as the alias given is not already used by other clients

# There are 3 predefined 'bots' [steven, arthur, andrea]
# As long as these predefined aliases are available,
# when running client.py and the bot option is not specified,
# a bot is connected automatically with the available predefined alias

# If all bots are all in use, the user is asked if they want to still connect
# if yes, a bot name is requested
# If no, their connection is terminated

# The host can also use this bot
# however it doesn't use the same dialogs as the regular bots (see responses.py)


def bot(bot_name, actions, reaction):
    global suggested_actions, alias
    suggested_actions = actions
    alias = bot_name
    reply = ''

    # Shows which actions are extracted from previous reply
    if alias != 'Host' and debug:
        print(f'\t-> Suggested action(s) found from previous reply: {suggested_actions}')

    # These extracted actions are temporarily removed so that
    # the current bot don't suggest it again
    for a in suggested_actions:
        if a in choices:
            choices.remove(a)
            if debug:
                print(f"\t-> [{a}] is temporarily removed from actions to prevent bot from suggesting the same action.")
                print(f"\t-> Bot can still agree to action: [{a}]")

    # Shows which actions the current bot can suggest
    # if alias != 'Host' and debug:
    #    print(f'\t-> Action(s) left to suggest: {choices}')

    # The bot response is formulated
    if len(actions) > 0:
        reply += generate_reply(reaction)
    else:
        return format_replies(alias, "I don't know how to respond to that.", actions, random.choice(r))

    # Shows which actions are used in the formulated sentence
    if alias != 'Host' and debug:
        print(f'\t-> Bot used this action(s) in its sentence: {new_actions}\n')

    # Just makes the host name more dynamic
    if alias == 'Host':
        alias = random.choice(responses.host_identities)

    # Returns the formulated sentence
    return format_replies(alias, reply, new_actions, random.choice(r))


# Formats the bot reply to a valid json format
def format_replies(sender, message, actions, reaction):
    return {
        "sender": sender,
        "message": message,
        "actions": actions,
        "reaction": reaction
    }


# generate_reply() = bots generate replies coming from responses.py
# depending on the expected reaction and depending who the bot is

# the host has a different set of responses,
# rather they're suggestions that initiates the conversation between the regular bots

def generate_reply(reaction):

    # By clearing the new_actions list,
    # it uses only actions mentioned from the previous reply
    new_actions.clear()

    # If the bot is the host, use the host suggestion responses (see responses.py)
    if alias == 'Host':
        suggestion = random.choice(responses.suggestions)
        return formulate_sentence(suggestion, reaction)

    # If the bot is a regular client, use the client replies (see responses.py)
    else:
        if reaction == p:
            sentence = random.choice(responses.positive_replies)
        elif reaction == n:
            sentence = random.choice(responses.negative_replies)
        else:
            sentence = random.choice(responses.neutral_replies)

    return formulate_sentence(sentence, reaction)


def formulate_sentence(sentence, reaction):
    global choices

    # These are placeholder counters
    # With the help of these, all placeholder in a sentence are replaced with a random action
    count_keyword_1 = count(sentence, keyword_to_replace1)
    count_keyword_2 = count(sentence, keyword_to_replace2)
    count_keyword_3 = count(sentence, keyword_to_replace3)

    # Length of suggested action list
    number_of_suggested_actions = len(suggested_actions)

    # If host keyword is greater than 0, formulate the sentence
    # This occurs only once, it's when the server starts
    if count_keyword_3 > 0:
        sentence = replace_placeholder(sentence, keyword_to_replace3, count_keyword_3)
    else:

        # Number of suggested actions must be greater than the number of placeholders
        if count_keyword_1 > number_of_suggested_actions:

            # While the number of placeholder is greater than the number of suggested actions,
            # generate another sentence that can accommodate the number of suggested actions
            while count_keyword_1 > number_of_suggested_actions:
                sentence = generate_reply(reaction)
                count_keyword_1 = count(sentence, keyword_to_replace1)
                if number_of_suggested_actions >= count_keyword_1:
                    break

            return replace_placeholder(sentence, keyword_to_replace1, count_keyword_1)

        # if the number of actions is enough to replace the number of placeholders
        else:
            if count_keyword_1 > 0:
                sentence = replace_placeholder(sentence, keyword_to_replace1, count_keyword_1)

            if count_keyword_2 > 0:
                # new_actions.clear() = used so that all actions from previous reply is ignored
                # except for the new suggested actions
                new_actions.clear()
                sentence = replace_placeholder(sentence, keyword_to_replace2, count_keyword_2)

                if debug:
                    print(f'\t-> Action(s) left to suggest: {choices}')

            choices.clear()
            choices = [x for x in responses.bot_actions]

    return sentence


# Generates actions from the host actions list (responses.py)
def suggest_host_action():
    action = responses.host_actions.pop(random.choice(range(len(responses.host_actions))))
    if action not in new_actions:
        new_actions.append(action)
    return action


# Generates actions from the bots actions list (responses.py)
def suggest_new_action(array):
    action = array.pop(random.choice(range(len(array))))
    if debug:
        print(f'\t-> New action the bot want to suggest: {action}')

    if action not in new_actions:
        new_actions.append(action)
    return action


# Generates actions suggested by other clients
def get_action():
    global choices
    action = suggested_actions.pop(random.choice(range(len(suggested_actions))))

    if action not in new_actions:
        new_actions.append(action)
    return action


# Replies from responses.py uses placeholders (kwtr1 and kwtr2) for actions
# This method replaces those placeholders with valid actions

def replace_placeholder(sentence, keyword, limit):

    # If placeholder replacement needs to be from extracted actions
    # (actions suggested by other clients)
    if keyword == kwtr1:
        for i in range(limit):
            action = get_action()
            sentence = re.sub(kwtr1, action, sentence, 1)
            sentence = grammar_fixer(sentence, action)

    # If placeholder replacement needs to be from bots actions
    # (actions this client want to suggest)
    elif keyword == kwtr2:
        for i in range(limit):
            action = suggest_new_action(choices)
            sentence = re.sub(kwtr2, action, sentence, 1)
            sentence = grammar_fixer(sentence, action)

    # If placeholder replacement needs to be from host actions
    # (actions this client want to suggest)
    elif keyword == kwtr3:
        for i in range(limit):
            action = suggest_host_action()
            sentence = re.sub(kwtr3, action, sentence, 1)
            sentence = grammar_fixer(sentence, action)

    return sentence


# Fixes the form of actions
def grammar_fixer(sentence, action):
    ing_counter = count(sentence, (action + 'ing'))

    if ing_counter > 0:

        # F.eks action ends with an 'e' but
        # the sentence needs it to end with an 'ing'

        if str(action).endswith('e'):

            # If        action = 'drive'
            # then      a2 = 'driv'
            # action becomes 'driving' in the sentence

            a2 = str(action).rsplit('e', 1)[0]
            sentence = re.sub(action, a2, sentence, 1)

        # F.eks action needs double letters when changed to an ing action
        # F.eks rob becomes robbing
        # (b needs to be doubled)
        # @d indicates that the action needs a double letter

        if str(action).endswith('@d'):

            # If        action = 'rob@d'
            # then      a2 = 'rob'
            # and       last_char = 'b'
            # then      a3 = 'robb'
            # action becomes 'robbing' in the sentence

            a2 = str(action).rsplit('@d', 1)[0]
            last_char = a2[len(a2) - 1:]
            a3 = str(a2 + last_char)
            sentence = re.sub(action, a3, sentence, 1)

    else:

        # If action does not need to change to an ing action
        # but has the @d, remove the @d

        try:
            a2 = str(action).rsplit('@d', 1)[0]
            sentence = re.sub(action, a2, sentence, 1)

        # If action does not need to change to an ing action
        # and there are no placeholders, send the sentence back

        except:

            # When no grammar is needed to be fixed
            return sentence

    return sentence


# Counts how many placeholders needs to be replaced
def count(sentence, placeholder):
    counter = 0
    for _ in re.finditer(placeholder, sentence):
        counter += 1
    return counter
