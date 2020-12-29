"""Note to self:

It took me ~2 hours to find a bug where I was getting the correct
results on test runs but failing to get the right answer. I had
`round_key = tuple(p1 + p2)`, which made is so that I would end the
game incorrectly if, for example p1 = [1, 2, 3] and p2 = [4] has been
encountered before (stored as round_key = (1, 2, 3, 4)), but round_key
is also (1, 2, 3, 4) if p1 = [1, 2] and p2 = [3, 4].

It was still preventing infinite games and giving the correct results
on the test case.

I think if I'd have organized the code so that a function was getting
called ("check_for_previous_round") I might have been more careful to
think "what do I need to do to check if this exact round happened
before", or at least while debugging I would have more intentionally
thought about whether that function was correct. Without splitting it
into a function, it was all too easy to gloss over how that check was
accomplished.

So, basically, split things into functions!

"""
import sys

GAME_COUNT = 0


def read_cards(filename):

    with open(filename) as infile:
        text = infile.read().strip()

    player1, player2 = text.split("\n\n")
    play1 = []
    for line in player1.splitlines()[1:]:
        sline = line.strip()
        if sline:
            play1.append(int(line))
    play2 = []
    for line in player2.splitlines()[1:]:
        sline = line.strip()
        if sline:
            play2.append(int(line))

    return play1, play2


def one_round(p1, p2, recursive=True, parent=None):

    global GAME_COUNT
    GAME_COUNT += 1

    if parent:
        game_number = GAME_COUNT
    else:
        game_number = 1

    print("=== Game {} ===".format(game_number))

    round_number = 0
    previous_rounds = set()
    while p1 and p2:

        round_number += 1

        print("\n-- Round {} (Game {}) --".format(round_number, game_number))
        print("Player 1's deck: {}".format(", ".join(str(i) for i in p1)))
        print("Player 2's deck: {}".format(", ".join(str(i) for i in p2)))

        round_key = tuple(p1 + ["|"] + p2)
        if round_key in previous_rounds:
            return 1, {1: p1, 2: p2}

        previous_rounds.add(round_key)

        card1 = p1.pop(0)
        card2 = p2.pop(0)

        print("Player 1 plays: {}".format(card1))
        print("Player 2 plays: {}".format(card2))

        if recursive and len(p1) >= card1 and len(p2) >= card2:
            print("Playing a sub-game to determine the winner...\n")
            winner, _ = one_round(
                p1[:card1], p2[:card2], recursive=recursive, parent=game_number
            )
        elif card1 > card2:
            winner = 1
        elif card2 > card1:
            winner = 2
        else:
            raise "wut"

        print(
            "Player {} wins round {} of game {}!".format(
                winner, round_number, game_number
            )
        )
        if winner == 1:
            p1.extend([card1, card2])
        else:
            p2.extend([card2, card1])

    print("The winner of game {} is player {}!".format(game_number, winner))
    if parent:
        print("\n...anyway, back to game {}.".format(parent))

    return winner, {1: p1, 2: p2}


def part1(filename):

    deck1, deck2 = read_cards(filename)

    winner, result = one_round(deck1, deck2, recursive=False)
    score = sum(i * v for i, v in enumerate(reversed(result[winner]), 1))

    print("== Post-game results ==")
    print("Player 1's deck: {}".format(", ".join(str(i) for i in result[1])))
    print("Player 2's deck: {}".format(", ".join(str(i) for i in result[2])))

    print("\nPart one: {}".format(score), file=sys.stderr)


def part2(filename):

    deck1, deck2 = read_cards(filename)

    winner, result = one_round(deck1, deck2, recursive=True)
    score = sum(i * v for i, v in enumerate(reversed(result[winner]), 1))

    print("\n\n== Post-game results ==")
    print("Player 1's deck: {}".format(", ".join(str(i) for i in result[1])))
    print("Player 2's deck: {}".format(", ".join(str(i) for i in result[2])))

    print("\nPart two: {}".format(score), file=sys.stderr)


if __name__ == "__main__":

    filename = "input-22.txt"
    part1(filename)
    part2(filename)
