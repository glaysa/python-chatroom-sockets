# Placeholders
# kwtr abbreviation -> (keyword to replace)
# kwtr1 = this placeholder is replaced with an action found in the previous response of a client
# kwtr2 = this placeholder is replaced with an action found in the client actions array below

kwtr1 = '@1'
kwtr2 = '@2'

# Some actions need to change when becoming an ing action
# F.eks rob becomes robbing
# to indicate the action needs double letters,
# the variable 'duo_letters' is introduced

duo_letters = d = '@d'
bot_actions = ['cook', 'drink', 'eat', 'clean', 'play']

'''bot_actions = ['cook', 'drink', 'eat', 'bowl', 'fight', 'draw', 'hike', 'code', 'study', 'skate', 'fish', 'party',
               'kick', 'drive', 'climb', 'clean', 'learn', 'ski', 'sculpt', 'sing', 'paint', 'carve', 'race',
               'code', 'flower pick', 'story tell', 'game build', 'train', 'play', 'shoot', 'exercise']'''

# You can easily add new responses below
# When adding new responses, use placeholders
# That way, the placeholder will be replaced with a dynamic action
# When placeholders are not used, the action isn't read by other clients

negative_replies = [
    f"{kwtr1}ing is giving me deja vu. Let's do {kwtr2}ing instead.",
    f"Activities like {kwtr1}ing is not compatible with {kwtr1}ing. {kwtr2}ing sounds better!",
    f"Why don't we do {kwtr2}ing, instead of those not so fun activities?",
    f"Friends don't do {kwtr1}ing and {kwtr1}ing, they go {kwtr2}ing instead.",
    f"I guess you couldn't think of something better. Pandas {kwtr1} and {kwtr1}, I do {kwtr2}ing.",
    f"Just when I started liking you, {kwtr1}ing really? Think of something better like {kwtr2}ing.",
    f"My dog can think of something better than {kwtr1}ing. It barks {kwtr2}ing.",
    f"To be frank, no one {kwtr1}s during this time of the day. I'd rather go {kwtr2}ing.",
    f"I'm the type of person who does {kwtr2}ing, not {kwtr1}ing.",
    f"I think no one would like to {kwtr1}. Doesn't {kwtr2}ing sound a lot more fun?",
    f"Never mind that, let's {kwtr2} and {kwtr2} instead."
]

positive_replies = [
    f"Your timing is impeccable. {kwtr1}ing and {kwtr1}ing are perfect!",
    f"{kwtr1}ing and {kwtr1}ing are my specialties.",
    f"I miss {kwtr1}ing and {kwtr1}ing. Count me in!",
    f"I am mentally and financially prepared to {kwtr1} and {kwtr1}.",
    f"{kwtr1}ing and {kwtr1}ing? You just suggested something very fun.",
    f"Finally someone with ideas! {kwtr1}ing sounds really fun! Count me in!",
    f"It's the perfect timing for {kwtr1}ing! What about {kwtr2}ing?",
    f"It's been a while since we went {kwtr1}ing. Let's do that guys!",
    f"My mood says YES! to {kwtr1}ing!",
    f"Hmm... {kwtr1}ing you say ... I thought you'd never ask!",
    f"I'm in! Let's {kwtr2} too!"
]

neutral_replies = [
    f"It's been a while since we went {kwtr1}ing and {kwtr1}ing anyway. I'll come.",
    f"{kwtr1}ing and {kwtr1}ing are not the best activities, but they're not bad either.",
    f"I'm bad at {kwtr1}ing, but {kwtr1}ing sounds okay.",
    f"If I can improve my skills in {kwtr1}ing, I don't mind {kwtr1}ing as well.",
    f"{kwtr1}ing and {kwtr1}ing is not up to my alley, but I'll still come.",
    f"I don't mind {kwtr1}ing. I heard {kwtr2}ing is fun too!",
    f"Introverts like me don't get to choose. {kwtr1}ing it is!",
    f"{kwtr1}ing sounds okay. Let's start {kwtr2}ing as well to make it more fun.",
    f"If the weather is good, then so is my mood for {kwtr1}ing.",
    f"I woke up today and got the feeling that I would go {kwtr1}.",
    f"May it be {kwtr1}ing or {kwtr1}ing, {kwtr2}ing should always be a part of today's activities."
]

# Data used by the host bot ============================================================================================

# kwtr3 = this placeholder is replaced with an action found in the server actions array below
# Just like above, you can add more host suggestion using the placeholder kwtr3 for dynamic action

kwtr3 = '@3'
host_identities = ['Grumpy Friend', 'Sassy Friend', 'Troublemaker Friend', 'Sweet Friend']
host_actions = ['eat', 'cook']
# 'fight', 'paint', 'complain', f'swim{d}', 'party', 'camp', f'jog{d}', 'dive', 'craft', f'rob{d}']

suggestions = [
    #f"Wanna {kwtr3} or {kwtr3}, maybe {kwtr3}? Anything's fine ... just pick and save me from boredom!",
    f"Hey! I'm free this weekend, wanna {kwtr3} and {kwtr3}? Invite the others.",
    f"This is out of nowhere, but wanna {kwtr3}?",
    f"I heard {kwtr3}ing and {kwtr3}ing can deepen our friendship. You guys up for it?",
    f"No matter what you guys say, you're coming. We're gonna {kwtr3} together!"
]
