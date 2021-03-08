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


# Bot that can be reused using different aliases
# With this, there is no need for multiple bots
# because it has a variety of responses (responses.py)

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
    if reaction == p:
        sentence = random.choice(responses.positive_replies)
    elif reaction == n:
        sentence = random.choice(responses.negative_replies)
    else:
        sentence = random.choice(responses.neutral_replies)

    return formulate_sentence(sentence, reaction)


# Replies from responses.py uses placeholders (kwtr1 and kwtr2) for actions
# This method replaces those placeholders with valid actions

def formulate_sentence(sentence, reaction):
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

        return replace_keyword(sentence, keyword_to_replace1, count_keyword_1)

    # if the number of actions is enough to replace the number of placeholders
    else:
        if count_keyword_1 > 0:
            new_actions.clear()
            sentence = replace_keyword(sentence, keyword_to_replace1, count_keyword_1)
        if count_keyword_2 > 0:
            new_actions.clear()
            sentence = replace_keyword(sentence, keyword_to_replace2, count_keyword_2)

    return sentence


# Generates actions from the bot actions list
def suggest_new_action():
    action = responses.actions.pop(random.choice(range(len(responses.actions))))
    if action not in new_actions:
        new_actions.append(action)
    return action


# Generates actions coming other clients
def get_action():
    action = extracted_actions.pop(random.choice(range(len(extracted_actions))))
    if action not in new_actions:
        new_actions.append(action)
    return action


# Replace (wtr*) with random actions
def replace_keyword(text, keyword, limit):

    # If placeholder replacement should be from extracted actions
    if keyword == kwtr1:
        for i in range(limit):
            text = re.sub(kwtr1, get_action(), text, 1)

    # If placeholder replacement should be from bots actions
    if keyword == kwtr2:
        for i in range(limit):
            text = re.sub(kwtr2, suggest_new_action(), text, 1)

    return text


# Counts how many placeholders needs to be replaced
def count(text, word_to_replace):
    counter = 0
    for _ in re.finditer(word_to_replace, text):
        counter += 1
    return counter
