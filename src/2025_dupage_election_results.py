import pandas as pd
import seaborn as sns
import matplotlib as plt
import xmltodict
import xml.etree.ElementTree as ET


in_file = "/home/mike-rob/Development/Analytic_Dev/data/detail.xml"

tree = ET.parse(in_file)
root = tree.getroot()

timestamp = root.findtext("Timestamp") 
election_name = root.findtext("ElectionName")
election_date = root.findtext("ElectionDate")
region = root.findtext("Region")

# print(f"{timestamp=}, {election_name=}, {election_date=}, {region=}")

# Metadata for Election
metadata = {
        "Timestamp": timestamp,
        "Election Name" : election_name,
        "Election Date" : election_date,
        "Region" : region
    }

# print(metadata)

# Aggregated Voter Data
agg_root = root.find("VoterTurnout")

agg_voter_data = {
    "Total Voters": int(agg_root.attrib["totalVoters"]),
    "Ballots Cast": int(agg_root.attrib["ballotsCast"]),
    "Voter Turnout": float(agg_root.attrib["voterTurnout"])
}

# print(f"{agg_voter_data=}")

metadata["Total Voters"] = agg_voter_data['Total Voters']
metadata["Ballots Cast"] = agg_voter_data['Ballots Cast']
metadata["Voter Turnout"] = agg_voter_data['Voter Turnout']

print(f"{metadata=}")

# Precinct Turnout
precinct_turnout = []
for precinct in root.find("./VoterTurnout/Precincts"):
    precinct_turnout.append({
        "Precinct Name": precinct.attrib.get("name"),
        "Total Voters": precinct.attrib.get("totalVoters"),
        "Ballots Cast": precinct.attrib.get("ballotsCast"),
        "Voter Turnout": precinct.attrib.get("voterTurnout")
    })

print(f"{precinct_turnout[:4]=}")

# All Contests and All Vote types
contest = []
choice = []
vote_type = []
vote_errors = []

for con in root.find("./Contest"):
    contest.append({
        "Contest Key": con.attrib.get("Contest Key"),
        "Race Name": con.attrib.get("Race Name")    
    })

print(f"{contest=}")