"""
Contains all partitioning logic

author: Ryan Howell
"""

import random

def Partition(submissions, settings):
    """Generates grading partition

    Args:
        submissions (list): list of lists of student names
        settings (dict): settings dictionary

    Returns:
        dict: Instructor:Student partition dictionary
    """
    number, solo, group = Count(submissions, settings)
    random.shuffle(solo)
    random.shuffle(group)
    partition = {}

    for instructor in number.keys():
        partition[instructor] = []

        if "solo" in number[instructor]:
            for _ in range(round(number[instructor]["solo"])):
                if len(solo) == 0:
                    break
                partition[instructor].append(solo.pop())

        if "group" in number[instructor]:
            for _ in range(round(number[instructor]["group"])):
                if len(group) == 0:
                    break
                partition[instructor].append(group.pop())

    return partition
    
def Count(submissions, settings):
    """Counts how many students each instructor should grade

    Args:
        submissions (list): list of lists of student names
        settings (dict): settings dictionary

    Returns:
        tuple: number, solo, group
    """
    solo, group = list(), list()

    for s in submissions:
        if len(s) == 1:
            solo.append(s)
        else:
            group.append(s)

    hours = list(settings["instructors"].values())
    highest = max(hours)

    divisor = sum(hour / highest for hour in hours)
    number = {}

    for instructor, hour in settings["instructors"].items():
        if hour == 0:
            continue
        number[instructor] = {}
        if len(solo) != 0:
            number[instructor]["solo"] = (len(solo) / divisor) * (hour / highest)
        if len(group) != 0:
            number[instructor]["group"] = (len(group) / divisor) * (hour / highest)

    return number, solo, group   

  


        
        

