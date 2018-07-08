import argparse
import json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    args = parser.parse_args()

    nominations_list = read_nominations_file(args.file)
    teams = create_team_objects(nominations_list)
    divisions = sort_teams(teams)
    for name, teams in sorted(divisions.items()):
        create_division_report(name, teams)


def read_nominations_file(filename):
    with open(filename, 'r') as nominations_file:
        nominations_list = nominations_file.readlines()

    nominations_list = [line.strip()
                        for line in nominations_list
                        if line != '\n' and line != '']

    return nominations_list


def create_team_objects(nominations_list):
    current_team = ''
    teams = {}

    for line in nominations_list:
        heading, data = tuple(line.split(':'))
        heading = heading.strip()
        data = data.strip()

        if 'Team Name' in heading:
            current_team = data
            teams[current_team] = {}
        elif 'Division' in heading:
            if 'open' in data.lower():
                teams[current_team]['division'] = 'open'
            if 'intermediate' in data.lower():
                teams[current_team]['division'] = 'intermediate'
            if 'prem' in data.lower():
                teams[current_team]['division'] = 'premier'
        elif 'Best Pocket Scout' in heading:
            teams[current_team]['scoutpocket'] = data
        elif 'Best Flank Scout' in heading:
            teams[current_team]['scoutflank'] = data
        elif 'Best Roaming' in heading:
            teams[current_team]['roamer'] = data
        elif 'Best Medic' in heading:
            teams[current_team]['medic'] = data
        elif 'Best Demoman' in heading:
            teams[current_team]['demo'] = data
        elif 'Best Utility' in heading:
            teams[current_team]['utility'] = data
        elif 'Most Improved' in heading:
            teams[current_team]['most improved'] = data

    return teams


def sort_teams(teams):
    divisions = {}
    for team_name, data in teams.items():
        team_division = data['division']
        if team_division not in divisions:
            divisions[team_division] = {}
        # del data['division']
        divisions[team_division][team_name] = data

    return divisions


def create_division_report(name, teams):
    awards = {
        'Best Pocket Scout': 'scoutpocket',
        'Best Pocket Scout': 'scoutflank',
        'Best Utility': 'utility',
        'Best Pocket': 'pocket',
        'Best Roamer': 'roamer',
        'Best Demoman': 'demo',
        'Best Medic': 'medic',
        'Most Improved Player': 'most improved',
        'Most Improved Team': 'team award',
        'Friendliest Team': 'team award'
    }

    mvp = []
    for award, designator in awards.items():
        if designator == 'team award':
            canidate_list = list(teams.keys())
        else:
            canidate_list = get_award_list(teams, designator)
            mvp += canidate_list
        awards[award] = canidate_list
    awards['Most Valuble Player'] = list(set(mvp))

    print(name.capitalize(), 'voting')
    print('=' * len(name + ' voting'))

    for award, canidate_list in sorted(awards.items()):
        print(award + ': ', end='')
        print(*sorted(canidate_list), sep=', ', end='\n')

    print()


def get_award_list(teams, designator):
    class_list = [team[designator]
                  for team in teams.values() if designator in team]

    if type(class_list[0]) is list:
        class_list = [
            scout for scout_list in class_list for scout in scout_list]
    return sorted(class_list)


def prettyprint(obj):
    print(json.dumps(obj, indent=4))

main()
