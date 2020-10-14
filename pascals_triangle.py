'''
Matt Parker's Math Puzzles: How odd is Pascal's Triangle?
https://www.youtube.com/watch?v=tjJ2qL9uaz4

What percentage of numbers in the first 128 rows of Pascal's Triangle are odd?
'''

import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--n', type=int, default=128,
        help='Number of rows to compute')

    return parser.parse_known_args()

def pascals_triangle(n):
    counter = 0
    row = [1]
    while counter < n:
        counter += 1
        yield row
        # generate new row
        new_row = [1]
        for i in range(len(row) - 1):
            new_row.append(row[i] + row[i + 1])
        new_row.append(1)
        row = new_row

def main():
    ARGS, unused = parse_args()

    total = 0
    percentages = []

    for row in pascals_triangle(ARGS.n):
        total += len(row)
        odds = sum(map(lambda x : x % 2 == 1, row))

        percentages.append(odds / total)

    print(percentages)

if __name__ == '__main__':
    main()
