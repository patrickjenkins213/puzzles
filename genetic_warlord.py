'''
FiveThirtyEight Riddler: Are You The Best Warlord?
https://fivethirtyeight.com/features/are-you-the-best-warlord/

In a distant, war-torn land, there are 10 castles. There are two warlords:
you and your archenemy. Each castle has its own strategic value for a would-be
conqueror. Specifically, the castles are worth 1, 2, 3, …, 9, and 10 victory
points. You and your enemy each have 100 soldiers to distribute, any way you
like, to fight at any of the 10 castles. Whoever sends more soldiers to a
given castle conquers that castle and wins its victory points. If you each
send the same number of troops, you split the points. You don’t know what
distribution of forces your enemy has chosen until the battles begin. Whoever
wins the most points wins the war.

Implementation of a genetic algorithm to find the strongest warlord.
'''

import argparse
import random

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--population', type=int, default=100,
        help='size of population per generation')
    parser.add_argument('--generations', type=int, default=10,
        help='number of generations')
    parser.add_argument('--mutation', type=float, default=.05,
        help='percent chance a mutation will occur during reproduction')
    parser.add_argument('--cull', type=float, default=0.2,
        help='percent of population that is culled each generation')
    parser.add_argument('--soldiers', type=int, default=100,
        help='number of soldiers to distribute')
    parser.add_argument('--castles', type=int, default=10,
        help='number of castles owned by each warlord')

    return parser.parse_known_args()

def battle(warlord1, warlord2):
    score1 = 0
    score2 = 0
    for points, (castle1, castle2) in enumerate(zip(warlord1, warlord2), start=1):
        if castle1 > castle2:
            score1 += points
        elif castle1 < castle2:
            score2 += points
        else:
            score1 += points / 2
            score2 += points / 2

    return score1 > score2

def reproduce(warlord1, warlord2):
    soldiers = sum(warlord1)
    new_warlord = []
    for castle1, castle2 in zip(warlord1, warlord2):
        new_warlord.append(int((castle1 + castle2) / 2))

    new_warlord[random.randint(0, len(new_warlord) - 1)] += (soldiers - sum(new_warlord))

    return new_warlord

def swap_mutate(warlord):
    '''
    Mutates by swapping two adjacent (with wrap around) castles
    '''
    i = random.randint(0, len(warlord) - 1)
    j = (i + 1) % len(warlord)
    warlord[i] = warlord[i] + warlord[j]
    warlord[j] = warlord[i] - warlord[j]
    warlord[i] = warlord[i] - warlord[j]

def random_warlord(soldiers, castles):
    warlord = []
    for i in range(castles):
        if i == castles - 1:
            warlord.append(soldiers)
        else:
            s = random.randint(0, soldiers)
            warlord.append(s)
            soldiers -= s

    random.shuffle(warlord)

    return warlord

def main():
    ARGS, unused = parse_args()

    warlords = [random_warlord(ARGS.soldiers, ARGS.castles) for _ in range(ARGS.population)]

    for _ in range(ARGS.generations):
        scores = []
        for warlord in warlords:
            score = 0
            for enemy in warlords:
                score += battle(warlord, enemy)
            scores.append(score)

        # sort by scores
        # https://stackoverflow.com/a/9764364
        scores, warlords = (list(t) for t in zip(*sorted(zip(scores, warlords))))

        # cull weak warlords
        warlords = warlords[int((len(warlords) * ARGS.cull)):]

        # reproduce to fill population
        while len(warlords) < ARGS.population:
            new_warlord = reproduce(*random.sample(warlords, 2))
            if random.random() < ARGS.mutation:
                swap_mutate(new_warlord)
            warlords.append(new_warlord)

    scores, warlords = (list(t) for t in zip(*sorted(zip(scores, warlords))))
    print(f'{warlords[-1]} won with a score of {scores[-1]} in the final round.')

if __name__ == '__main__':
    main()
