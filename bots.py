import responses
import random
import re

# Reactions
u = 'neutral'
p = 'positive'
n = 'negative'
r = [u, p, n]

# Placeholder to actions in responses (see responses.py)
keyword_to_replace1 = kwtr1 = responses.kwtr1
keyword_to_replace2 = kwtr2 = responses.kwtr2

# Suggested actions
extracted_actions = []
# New set of actions suggested by the bot
new_actions = []


# This bot method can be reused
# You can create multiple clients with the method
# as long as the alias given is not used by other clients
# There are 3 predefined 'bots' [steven, arthur, andrea]
# As long as these predefined aliases are available,
# when running client.py and the bot option is not specified,
# these bots are connected automatically
# If all bots are all in use, the user is asked if they want to connect
# if yes, a bot name is requested
# If no, their connected is terminated

def bot(alias, actions, reaction):
    global extracted_actions
    extracted_actions = actions
    reply = ''

    if len(actions) > 0:
        reply += generate_reply(reaction)
    else:
        return format_replies(alias, "I don't know how to respond to that.", actions, random.choice(r))

    return format_replies(alias, reply, new_actions, random.choice(r))


# Formats the bot reply to a valid json format
def format_replies(sender, message, actions, reaction):
    return {
        "sender": sender,
        "message": message,
        "actions": actions,
        "reaction": reaction
    }


# Bot generates a reply coming from
# responses.py depending on the expected reaction

def generate_reply(reaction):

    # Uses only actions mentioned from the previous reply
    new_actions.clear()

    if reaction == p:
        sentence = random.choice(responses.positive_replies)
    elif reaction == n:
        sentence = random.choice(responses.negative_replies)
    else:
        sentence = random.choice(responses.neutral_replies)

    return formulate_sentence(sentence, reaction)


def formulate_sentence(sentence, reaction):
    # Counts the number of placeholders needed to be replaced
    count_keyword_1 = count(sentence, keyword_to_replace1)
    count_keyword_2 = count(sentence, keyword_to_replace2)
    number_of_actions = len(extracted_actions)

    # Number of actions must be greater than the number of placeholders
    if count_keyword_1 > number_of_actions:
        while count_keyword_1 > number_of_actions:
            sentence = generate_reply(reaction)
            count_keyword_1 = count(sentence, keyword_to_replace1)
            if number_of_actions >= count_keyword_1:
                break

        return replace_placeholder(sentence, keyword_to_replace1, count_keyword_1)

    # if the number of actions is enough to replace the number of placeholders
    else:
        if count_keyword_1 > 0:
            sentence = replace_placeholder(sentence, keyword_to_replace1, count_keyword_1)

        if count_keyword_2 > 0:

            # all actions from previous reply is ignored
            # while new suggested actions are the only ones sent back

            new_actions.clear()
            sentence = replace_placeholder(sentence, keyword_to_replace2, count_keyword_2)

    return sentence


# Generates actions from the actions list (responses.py)
def suggest_new_action():
    action = responses.actions.pop(random.choice(range(len(responses.actions))))
    if action not in new_actions:
        new_actions.append(action)
    return action


# Generates actions suggested by other clients
def get_action():
    action = extracted_actions.pop(random.choice(range(len(extracted_actions))))

    # Prevents bot from suggesting the same action as the previous bot
    if action in responses.actions:
        responses.actions.remove(action)

    # Prevents duplicates
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

    # If placeholder replacement needs to be from actions
    # (actions this client want to suggest)
    if keyword == kwtr2:
        for i in range(limit):
            action = suggest_new_action()
            sentence = re.sub(kwtr2, action, sentence, 1)
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
def count(sentence, word_to_replace):
    counter = 0
    for _ in re.finditer(word_to_replace, sentence):
        counter += 1
    return counter
