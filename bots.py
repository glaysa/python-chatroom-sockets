import random
import re

# Reactions
u = 'neutral'
p = 'positive'
n = 'negative'
r = [u, p, n]

# Actions from other clients
extracted_actions = []
# Actions the bot can suggest
bot_actions = ['fish', 'code', 'bowl', 'club', 'shop', 'dance', 'chill', 'picture take']
# New set of actions sent to other clients
new_actions = []


def andrea(alias, actions, reaction):
    global extracted_actions
    extracted_actions = actions
    reply = ''

    if len(actions) > 0:
        reply += generate_reply(reaction)
    else:
        return format_replies(alias, "I don't know how to respond to that.", actions, random.choice(r))

    return format_replies(alias, reply, new_actions, random.choice(r))


def steven(alias, actions, reaction):
    global extracted_actions
    extracted_actions = actions
    reply = ''

    if len(actions) > 0:
        reply += generate_reply(reaction)
    else:
        return format_replies(alias, "I don't know how to respond to that.", actions, random.choice(r))

    return format_replies(alias, reply, new_actions, random.choice(r))


def arthur(alias, actions, reaction):
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


# char to replace with an action from extracted actions
# shorthand version, used in sentences (wtr1)
# long version (word_to_replace1) is used for functions for better readability
word_to_replace1 = wtr1 = '@'

# char to replace with an action from bot actions
# shorthand version, used in sentences (wtr2)
# long version (word_to_replace2) is used for functions for better readability
word_to_replace2 = wtr2 = '&'


def generate_reply(reaction):
    if reaction == p:
        sentence = random.choice([
            f"Your timing is impeccable. {wtr1}ing and {wtr1}ing are perfect!",
            f"{wtr1}ing and {wtr1}ing are my specialties.",
            f"I miss {wtr1}ing and {wtr1}ing. Count me in!",
            f"I am mentally and financially prepared to {wtr1} and {wtr1}.",
            f"{wtr1}ing and {wtr1}ing? You just suggested something very fun.",
            f"Finally someone with ideas! {wtr1}ing sounds really fun! Count me in!",
            f"It's the perfect timing for {wtr1}ing!",
            f"It's been a while since we went {wtr1}ing. Let's do that guys!",
            f"My mood says YES! to {wtr1}ing!",
            f"Hmm... {wtr1}ing you say ... I thought you'd never ask!"
        ])

    elif reaction == n:
        sentence = random.choice([
            f"{wtr1}ing is giving me deja vu. Let's do {wtr2}ing instead.",
            f"Activities like {wtr1}ing is not compatible with {wtr1}ing. {wtr2}ing sounds better!",
            f"Why don't we do {wtr2}ing, instead of those not so fun activities?",
            f"Friends don't do {wtr1}ing and {wtr1}ing, they go {wtr2}ing instead.",
            f"I guess you couldn't think of something better. Pandas {wtr1} and {wtr1}, I do {wtr2}ing.",
            f"Just when I started liking you, {wtr1}ing really? Think of something better like {wtr2}ing.",
            f"My dog can think of something better than {wtr1}ing. It barks {wtr2}ing.",
            f"To be frank, no one {wtr1}s during this time of the day. I'd rather go {wtr2}ing.",
            f"I'm the type of person who does {wtr2}ing, not {wtr1}ing.",
            f"I think no one would like to {wtr1}. Doesn't {wtr2}ing sound a lot more fun?",
            f"Never mind that, let's {wtr2} and {wtr2} instead."
        ])

    else:
        sentence = random.choice([
            f"It's been a while since we went {wtr1}ing and {wtr1}ing anyway. I'll come.",
            f"{wtr1}ing and {wtr1}ing are not the best activities, but they're not bad either.",
            f"I'm bad at {wtr1}ing, but {wtr1}ing sounds okay.",
            f"If I can improve my skills in {wtr1}ing, I don't mind {wtr1}ing as well.",
            f"{wtr1}ing and {wtr1}ing is not up to my alley, but I'll still come.",
            f"I don't mind {wtr1}ing.",
            f"Introverts like me don't get to choose. {wtr1}ing it is!",
            f"{wtr1}ing sounds okay.",
            f"If the weather is good, then so is my mood for {wtr1}ing.",
            f"I woke up today and got the feeling that I would {wtr1}."
        ])

    return formulate_sentence(sentence, reaction)


def formulate_sentence(sentence, reaction):
    count_keyword_1 = count(sentence, word_to_replace1)
    count_keyword_2 = count(sentence, word_to_replace2)
    number_of_actions = len(extracted_actions)

    # Number of actions must be greater than the number of words needed to be replaced
    if count_keyword_1 > number_of_actions:
        while count_keyword_1 > number_of_actions:
            sentence = generate_reply(reaction)
            count_keyword_1 = count(sentence, word_to_replace1)
            if number_of_actions >= count_keyword_1:
                break

        return replace_word(sentence, word_to_replace1, count_keyword_1)

    # If number of actions is sufficient, word replacing will run as usual
    else:
        if count_keyword_1 > 0:
            new_actions.clear()
            sentence = replace_word(sentence, word_to_replace1, count_keyword_1)
        if count_keyword_2 > 0:
            new_actions.clear()
            sentence = replace_word(sentence, word_to_replace2, count_keyword_2)

    return sentence


# Generates actions from the bot actions list
def generate_new_action():
    action = bot_actions.pop(random.choice(range(len(bot_actions))))
    if action not in new_actions:
        new_actions.append(action)
    return action


# Generates actions coming other clients
def generate_action():
    action = extracted_actions.pop(random.choice(range(len(extracted_actions))))
    if action not in new_actions:
        new_actions.append(action)
    return action


# Replace (wtr*) with random actions
def replace_word(text, keyword, limit):
    if keyword == wtr1:
        for i in range(limit):
            text = re.sub(wtr1, generate_action(), text, 1)
    if keyword == wtr2:
        for i in range(limit):
            text = re.sub(wtr2, generate_new_action(), text, 1)

    return text


# Counts how many chars needs to be replaced
def count(text, word_to_replace):
    counter = 0
    for _ in re.finditer(word_to_replace, text):
        counter += 1
    return counter
