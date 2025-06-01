import xml.etree.ElementTree as ET
import pandas as pd
import os

root_dir = "D:\\Home\\Documents\\Data Analysis Projects\\Analytics-Practice\\data\\"
in_file = "2024_election.xml"
out_file = "2024_election.csv"

# Parse the XML file (update the file name as needed)
tree = ET.parse(os.path.join(root_dir, in_file))

root = tree.getroot()

# List to store normalized rows
rows = []

# Process each Contest element (if you have multiple contests)
for contest in root.findall("Contest"):
    # Extract contest-level attributes
    contest_attrs = contest.attrib
    contest_key = contest_attrs.get("key")
    contest_text = contest_attrs.get("text")
    contest_voteFor = contest_attrs.get("voteFor")
    contest_isQuestion = contest_attrs.get("isQuestion")
    contest_precinctsReporting = contest_attrs.get("precinctsReporting")
    contest_precinctsReported = contest_attrs.get("precinctsReported")
    
    # --- Part 1: Process direct VoteType children of Contest
    for vote_type in contest.findall("VoteType"):
        vote_type_name = vote_type.attrib.get("name")
        vote_type_total_votes = vote_type.attrib.get("votes")
        # Loop through each Precinct within the VoteType
        for precinct in vote_type.findall("Precinct"):
            row = {
                "ContestKey": contest_key,
                "ContestText": contest_text,
                "ContestVoteFor": contest_voteFor,
                "ContestIsQuestion": contest_isQuestion,
                "ContestPrecinctsReporting": contest_precinctsReporting,
                "ContestPrecinctsReported": contest_precinctsReported,
                "Choice": None,  # No candidate for these vote types
                "VoteTypeName": vote_type_name,
                "VoteTypeTotalVotes": vote_type_total_votes,
                "PrecinctName": precinct.attrib.get("name"),
                "PrecinctVotes": precinct.attrib.get("votes"),
            }
            rows.append(row)
    
    # --- Part 2: Process Choice elements (nested vote types for candidates)
    for choice in contest.findall("Choice"):
        # Extract candidate-level attributes
        choice_key = choice.attrib.get("key")
        choice_text = choice.attrib.get("text")
        choice_total_votes = choice.attrib.get("totalVotes")
        
        # Loop through each VoteType within this Choice
        for vote_type in choice.findall("VoteType"):
            vote_type_name = vote_type.attrib.get("name")
            vote_type_total_votes = vote_type.attrib.get("votes")
            # Loop through each Precinct within the nested VoteType
            for precinct in vote_type.findall("Precinct"):
                row = {
                    "ContestKey": contest_key,
                    "ContestText": contest_text,
                    "ContestVoteFor": contest_voteFor,
                    "ContestIsQuestion": contest_isQuestion,
                    "ContestPrecinctsReporting": contest_precinctsReporting,
                    "ContestPrecinctsReported": contest_precinctsReported,
                    "Choice": choice_text,  # Candidate or option from the <Choice> element
                    "VoteTypeName": vote_type_name,
                    "VoteTypeTotalVotes": vote_type_total_votes,
                    "PrecinctName": precinct.attrib.get("name"),
                    "PrecinctVotes": precinct.attrib.get("votes"),
                }
                rows.append(row)

# Create a DataFrame from the list of rows
df = pd.DataFrame(rows)

df.to_csv(os.path.join(root_dir, out_file), index=False)