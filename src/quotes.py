from random import choice
import re

quotes = [
    "Everybody wants to be a bodybuilder, but don't nobody wanna lift no heavy ass weight.",
    "Ain't nuttin' to it, but ta do it!",
    "Hard work and training. There's no secret formula. I lift heavy, work hard and aim to be the\
    best.",
    "My biggest competition is always myself.",
    "Light weight ... Yeah buddy!",
    "Aint nuttin' but a peanut.",
    "When you hit failure your workout has just begun.",
    "It is important to have people believe in you. With this support, what you can achieve is\
    limitless.",
    "There's no secrets or magic tricks to being successful in life. It's plain and simple. Work harder than\
    everyone else and the only way to do that is to do it.",
    "I always say to myself right before a tough set in the gym, Ain't nothin' to it, but to do it.",
    "Women really do pay attention to a man's glutes. A tight, compact ass is often voted even more desirable than\
    muscular arms and chest. So, if you're lacking, start squatting!",
    "I loved challenging myself every day. The weight room was my therapy for everyday life stresses. No matter what\
    I was doing I always wanted to be the best.",
    "When you love something as much as I love bodybuilding you don't have to do much extra to push yourself, it just\
    happens.",
    "There were some tough times and when those came up I just used my mental strength to push through knowing\
    that my mind controlled everything.",
    "Thank god for pure natural strength.",
    "Never underestimate the power of wide-grip pull-ups to develop width and size.",
    "Everybody wants to be a bodybuilder.",
    "I never focus on contraction. I'm focusing on my muscle. I'm not focusing on a certain style of lifting or\
    contracting. I'm just trying to get the weight up. I'm trying to build muscle.",
    "I've attained my mass basically by training hard and very, very heavy.",
    "I know that in order for something to work for me it has to be extremely powerful.",
    "Just because your triceps have fallen behind your biceps, doesn't mean you should back off your triceps\
    workouts.",
    "I've been training so long, its second nature to push myself to the limit.",
    "If you take a hammer and hit something over and over again, it's gonna be destroyed.",
    "I don't wanna destroy my body cause I want my body to last me as long as it possible can. If you train hard and \
    push it everyday, your body is going to wear out.",
    "Bodybuilding is a hobby. At least for me it is. I've trained since i was 12 or 13 years old. It's a hobby I just\
    have so much fun with it. I get so much enjoyment from it.",
    "To have your job as your hobby - life don't get better than that.",
    "Your body produces a lot less testosterone each and every single year no matter who you are. We are all human,\
    nobody is super human.",
    "Train harder and grow bigger."
]


def get_random_quote():
    return re.sub(' +', ' ', choice(quotes)) + "\n"
