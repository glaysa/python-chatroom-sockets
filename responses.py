
# Placeholders
kwtr1 = '@1'
kwtr2 = '@2'

actions = ['cook', 'drink', 'eat', 'bowl', 'fight', 'draw', 'hike', 'code', 'study', 'skate', 'fish', 'party',
           'kick', 'out', 'drive', 'climb', 'clean', 'learn', 'ski', 'sculpt', 'sing', 'paint', 'carve', 'race',
           'code', 'flower pick', 'story tell', 'game build', 'train', 'play', 'video game']

# Can easily add new responses
# When adding a dynamic actions, just use the placeholder to generate a random action

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
    f"It's the perfect timing for {kwtr1}ing!",
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
    f"I don't mind {kwtr1}ing.",
    f"Introverts like me don't get to choose. {kwtr1}ing it is!",
    f"{kwtr1}ing sounds okay.",
    f"If the weather is good, then so is my mood for {kwtr1}ing.",
    f"I woke up today and got the feeling that I would {kwtr1}.",
    f"May it be {kwtr1}ing or {kwtr1}ing, {kwtr2}ing should always be a part of today activities."
]