import json


def main():
    votes = get_votes('votes.txt')
    prettyprint(votes)

def get_votes(filename):
    voting_divisions = {'premier':{}, 'intermediate':{}, 'open':{}, 'general': {}}

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


def prettyprint(obj):
    print(json.dumps(obj, indent=4))


def process_award_old(award_object):
    first_votes = {person: votes[0] for person, votes in award_object.items()}
    total = sum(first_votes.values())

    winner = None
    for person, vote in first_votes.items():
        if vote/total > 0.5:
            winner = person

    if winner is not None:
        return winner
    else:
        redistribute_votes(award_object)



def redistribute_votes(voting):
    first_votes = count_first_votes(voting)
    loser = min(first_votes, key=first_votes.get)

    # remove loser from voting
    for i, player_list in enumerate(voting):
        if loser in player_list:
            voting[i].remove(loser)
    return(voting)


def count_first_votes(voting):
    first_votes = {}
    print(voting)
    for vote in voting:
        if len(vote) > 0:
            first_vote = vote[0]
            if first_vote not in first_votes:
                first_votes[first_vote] = 1
            else:
                first_votes[first_vote] += 1

    for vote in voting:
        if len(vote) > 1:
            for later_vote in vote[1:]:
                if later_vote not in first_votes:
                    first_votes[later_vote] = 0
    return first_votes

def process_award(voting):
    votes = count_first_votes(voting)

    winner = max(votes, key=votes.get)
    winning_votes = votes[winner]
    total = sum(votes.values())

    if winning_votes / total < 0.5:
        return process_award(redistribute_votes(voting))
    else:
        return winner



main()
