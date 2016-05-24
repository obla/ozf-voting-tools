import json


def main():
    votes = get_votes('votes_test.txt')
    for division, voting in votes.items():
        produce_division_report(division, voting)


def get_votes(filename):
    voting_divisions = {
        'premier': {},
        'intermediate': {},
        'open': {},
        'general': {}
    }

    with open(filename, 'r') as votes_file:
        raw_votes = votes_file.read().split('\n')

    raw_votes = [vote.strip() for vote in raw_votes if vote not in ['\n', '']]

    for vote_line in raw_votes:
        heading, votes = tuple(vote_line.split(':'))
        heading = heading.strip()
        votes = [vote.strip() for vote in votes.split(',')]
        if heading == 'Your team division':
            current_division = votes[0]
        elif heading == 'Your team name':
            pass
        else:
            if heading in ['Premier MVP', 'Best Caster']:
                current_division, temp_division = 'general', current_division

            if heading not in voting_divisions[current_division]:
                voting_divisions[current_division][heading] = []
            voting_divisions[current_division][heading] += [votes]

            if current_division == 'general':
                current_division = temp_division

    return voting_divisions


def produce_division_report(division, voting):
    print(division)
    print('=' * len(division))

    for vote_category, voting_log in voting.items():
        winner = process_award(voting_log)
        print(vote_category + ':', winner)


def redistribute_votes(voting, winner):
    first_votes = count_first_votes(voting)
    loser = min(first_votes, key=first_votes.get)
    # remove loser from voting
    for i, player_list in enumerate(voting):
        if loser in player_list:
            voting[i].remove(loser)
    return(voting)


def tie_is_unbreakable(voting):
    vote_positions = 0
    for vote_set in voting:
        vote_positions = max(len(vote_set), vote_positions)

    print(vote_positions)
    if vote_positions == 2:
        return True
    else:
        return False


def count_first_votes(voting):
    first_votes = {}

    for vote_set in voting:
        if len(vote_set) > 0:
            for i, vote in enumerate(vote_set):
                if vote not in first_votes:
                    first_votes[vote] = 0
                if i == 0:
                    first_votes[vote] += 1

    return first_votes


def process_award(voting):
    votes = count_first_votes(voting)

    winner = max(votes, key=votes.get)
    winning_votes = votes[winner]
    total = sum(votes.values())
    percentage = winning_votes / total

    if percentage > 0.5:
        return winner
    if percentage == 0.5 and tie_is_unbreakable(voting):
        winners = [winner for votelist in votes for winner in votelist]
        return ' and '.join(winners)

    return process_award(redistribute_votes(voting, winner))


def prettyprint(thing):
    print(json.dumps(thing, indent=4))

main()
