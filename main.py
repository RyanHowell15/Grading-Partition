"""
Main script the user interacts with.
Error checks input and settings.json.
See partition.py for partitioning logic

author: Ryan Howell
"""
import json
import sys
import csv
import partition
import os.path
from os import path
  
def Process_CSV(filepath, settings):
    """
    Turns a CSV file of submissions into a list of
    names

    Args:
        filepath (str): path to csv file
        settings (dict): settings dictionary

    Returns:
        list: list of lists, each containing names 
            of each partner (or 1 name if solo)
    """
    with open(filepath, 'r') as csvfile: 
        csv_reader = csv.DictReader(csvfile)
        visited = {}
        for row in csv_reader:
            if row["Status"] != "Missing":
                studentName = row["First Name"]

                if row["Last Name"]:
                    studentName += ' ' + row["Last Name"]

                if studentName.upper() not in settings["instructors"]: 
                    subID = row["Submission ID"]
                    if subID not in visited:
                        visited[subID] = []
                    visited[subID].append(studentName)

    return list(visited.values())
    
def Get_Settings():
    """
    Reads settings.json into a dict

    Returns:
        dict: dictionary with various settings fields,
            such as "instructors" and "output"
    """
    if not path.exists('settings.json'):
        print("ERROR: settings.json file not found. Try running the setup command and refer to the README.")
        exit()

    settings = {}
    with open('settings.json') as json_file:
        settings = json.load(json_file)

    if "instructors" not in settings:
        print("ERROR: no \"instructors\" field found in settings.json")
        exit()

    if min(settings["instructors"].values(), default = 0) < 0:
        print("ERROR: at least 1 instructor that works more than 0 hours must be defined")
        exit()

    if "output" not in settings:
        print("ERROR: no \"output\" field found in settings.json")
        exit()

    possible_outputs = ["txt", "json", "googlesheets"]

    output = settings["output"]
    if output not in possible_outputs:
        print(f"ERROR: output setting of {output} not valid.")
        print(f"Must be one of: {possible_outputs} only.")
        exit()

    if output == "googlesheets":
        if "sheetUrl" not in settings:
            print("ERROR: googlesheets output specified but no \"sheetUrl\" setting found.")
            exit()
        if not path.exists('client_key.json'):
            print("ERROR: googlesheets output specified but no client_key.json found in current directory")
            exit()


    return settings

def Output(partition, settings):
    """
    Outputs the partition based on the method
    described in the "output" field in settings.json

    Args:
        partition (dict): Instructor:Student partition dictionary
        settings (dict): settings dictionary
    """
    method = settings["output"]
    
    if method == "json":
        json_object = json.dumps(partition)

        with open("partition.json", "w") as outfile:
            outfile.write(json_object)
            
    if method == "txt":
        with open("partition.txt", "w") as outfile:
            for i in sorted(partition.keys()):               
                outfile.write(i + "\n")
                outfile.write("\n")
                for s in partition[i]:
                    outfile.write("\t".join(s)+ "\n")
                outfile.write("\n")
    
    if method == "googlesheets":
        import googlesheets
        googlesheets.Create_Sheet(partition, settings)

if __name__ == "__main__":
    error_message = "ERROR: Only input filepath to a .csv file or setup command. For example:\n python3 main.py setup\nor\npython3 main.py ./Assignment_7_Scores.csv"
    if len(sys.argv) != 2:
        print(error_message)
        exit()

    command = sys.argv[1]

    if command.endswith(".csv"):
        settings = Get_Settings()

        submissions = Process_CSV(sys.argv[1], settings)
        p = partition.Partition(submissions, settings)
        
        Output(p, settings)
    elif command == "setup":
        if path.exists('settings.json'):
            print("ERROR: existing settings.json detected. Setup command not ran")
            exit()

        settingsTemplate = {
            "instructors":{
                "John Doe":20,
                "Jane Doe":15,
            },
            "output":"txt"
        }
        json_object = json.dumps(settingsTemplate, indent=4)

        with open("settings.json", "w") as outfile:
            outfile.write(json_object)
    else:
        print(error_message)
        exit()
