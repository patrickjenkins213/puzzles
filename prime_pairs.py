'''
Matt Parker's Math Puzzles: Prime Pairs Puzzle
https://www.youtube.com/watch?v=AXfl_e33Gt4

Find a permutation of the numbers 1 through 9 such that
the sum of each consecutive pair of numbers is prime.
'''

import argparse
import itertools
import math

primes = []

def is_prime(n):
    if n in primes:
        return True

    for i in range(2, int(math.sqrt(n) + 1)):
        if n % i == 0:
            return False
    primes.append(n)
    return True

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--n', type=int, default=9,
        help='Find prime pair sequences for [1, 2, ..., n]')

    return parser.parse_known_args()

def is_prime_pairs_seq(p):
    for i in range(len(p) - 1):
        if not is_prime(p[i] + p[i + 1]):
            return False
    return True

def is_prime_pairs_strong_seq(p, n):
    '''
    Finds "strong" wrap around prime pair sequences
    '''
    for i in range(len(p)):
        if not is_prime(p[i] + p[(i + 1) % n]):
            return False
    return True

def rotations(p):
    r = []
    for i in range(len(p)):
        r.append(p[i:] + p[:i])

    return r

def main():
    ARGS, unused = parse_args()

    seqs = []
    strong_seqs = []
    for p in itertools.permutations([_ for _ in range(1, ARGS.n + 1)]):
        if is_prime_pairs_seq(p) and list(reversed(p)) not in seqs:
            seqs.append(list(p))

        if is_prime_pairs_strong_seq(p, ARGS.n):
            for q, r in zip(rotations(p), rotations(list(reversed(p)))):
                if q in strong_seqs or r in strong_seqs:
                    break
            else:
                strong_seqs.append(list(p))

    for s in seqs:
        print(s)
    print(f'Found {len(seqs)} unique prime pair permutations of length {ARGS.n}')

    for s in strong_seqs:
        print(s)
    print(f'Found {len(strong_seqs)} unique wrap around prime pair permutations of length {ARGS.n}')

if __name__ == '__main__':
    main()
