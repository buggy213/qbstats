import wget
import os
from openpyxl import load_workbook
from collections import namedtuple
from enum import Enum

# SQBS File Format
# https://www.qbwiki.com/wiki/SQBS_data_file
# sqbs_file_format

Team = namedtuple('Team', 'team_name division')

class Division(Enum):
    JV
    VARSITY

def strip_team_name(team_name):
    varsity = Division.VARSITY if "(V)" in team_name else Division.JV
    stripped_name = team_name.strip()
    stripped_name = stripped_name.rstrip("(JV)")
    stripped_name = stripped_name.strip()
    return Team(stripped_name, varsity)

# Checks if SQBS file exists; if it does, overwrite
# Writes team names and team members to the file
def write_rosters(filename, rosters):
    if os.path.isfile(filename):
        os.remove(filename)

    f = open(filename, 'w')

    write_line(f, len(rosters))
    for team_name, members in rosters:
        write_line(f, len(members) + 1)
        write_line(f, team_name)
        for member in members:
            write_line(f, member)

    return f

# Helper function to write a string followed by a newline
# (why isn't this a builtin?!?!?)
def write_line(f, content):
    f.write(str(content) + '\n')

def main():
    while True:
        url = input("URL of published aggregate spreadsheet: ")
        try:
            wget.download(url)
        except ValueError:
            print("Invalid URL, try again")
            continue
        break
    
    xlsx_files = [f for f in os.listdir('.') if f.endswith('.xlsx')]
    if len(xlsx_files) != 1:
        raise ValueError('should be only one txt file in the current directory')

    spreadsheet = xlsx_files[0]

    workbook = load_workbook(filename = spreadsheet)
    
    # Support for double division tournaments
    jv_teams = dict()
    v_teams = dict()

    rosters_worksheet = workbook["Rosters"]
    for row in rosters_worksheet.values()
        team = strip_team_name(row[0])
        members = row[1:]
        if team.division is Division.VARSITY:
            v_teams[team.team_name] = members
        elif team.division is Division.JV:
            jv_teams[team.team_name] = members
    
    write_rosters("Varsity", v_teams)
    write_rosters("JV", jv_teams)

    for worksheet_name in workbook.sheetnames:
        if worksheet_name is "Rosters":
            continue

        worksheet = workbook[worksheet_name]
        for row in worksheet.values():
            # Check if this is a new game by looking at team names
            # if team names are empty, then this is not a game -- skip parsing until next row,
            # if one team is present but not the other, assume a forfeit
            # otherwise, begin parsing and putting into sqbs file




if __name__ == '__main__':
    main()