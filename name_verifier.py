def main():
    nominations = load_nominations()
    votes = load_votes()

    invalid_votes = {vote for vote in votes if vote not in nominations}

    # print(*invalid_votes, sep='\n')
    print(invalid_votes)


def load_votes():
    with open('votes.txt') as votes_file:
        lines = [line.strip().split(':')[1].strip().split(',')
                 for line in votes_file.readlines()
                 if line not in ['', '\n']]

        lines = [player.strip().lower() for line in lines for player in line]
    return lines


def load_nominations():
    with open('noms.txt', 'r') as nominations_file:
        nominations = [nom.split(':')[1].strip().lower()
                       for nom in nominations_file.readlines()
                       if 'Division' not in nom]
    return nominations

main()
