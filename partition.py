"""
Contains all partitioning logic

author: Ryan Howell
"""

import random

class PartitionData:
    def __init__(self, submissions, settings):
        self.solo_submissions = []
        self.group_submissions = []
        for s in submissions:
            if len(s) == 1:
                self.solo_submissions.append(s)
            else:
                self.group_submissions.append(s)

        self.instructor_data = settings["instructors"]
        
        hours = list(self.instructor_data.values())
        self.highest_amount_worked = max(hours)
        self.divisor = sum(hour / self.highest_amount_worked for hour in hours)

    def solo_grade_count(self, instructor):
        hours_worked = self.instructor_data[instructor]
        return (len(self.solo_submissions) / self.divisor) * (hours_worked /self.highest_amount_worked)
    
    def group_grade_count(self, instructor):
        hours_worked = self.instructor_data[instructor]
        return (len(self.group_submissions) / self.divisor) * (hours_worked /self.highest_amount_worked)
    
    def get_solo_submissions(self):
        return list(self.solo_submissions)
    
    def get_group_submissions(self):
        return list(self.group_submissions)
    
    def instructors(self):
        """
        Returns
        -------
        list
            list of instructor names who work 
        """
        return [key for key, value in self.instructor_data.items() if value > 0]

def Partition(submissions, settings):
    """Generates grading partition

    Args:
        submissions (list): list of lists of student names
        settings (dict): settings dictionary

    Returns:
        dict: Instructor:Student partition dictionary
    """
    data = PartitionData(submissions, settings)
    solo_submissions = data.get_solo_submissions()
    group_submissions = data.get_group_submissions()

    instructors = data.instructors()
    partition = {i: [] for i in instructors}

    for submission in group_submissions: 
        instructor = next_instructor(partition, data, False)
        partition[instructor].append(submission)

    for submission in solo_submissions: 
        instructor = next_instructor(partition, data, True)
        partition[instructor].append(submission)

    return partition

def next_instructor(partition, data:PartitionData, solo:bool):
    """
    Returns the instructor with the biggest difference between
    calculated number of submissions they should grade,
    and the amount of submissions they actually have assigned
    in partition.

    Parameters
    ----------
    partition : dict
    data : PartitionData
    solo: bool

    Returns
    -------
    str
    """
    def assigned_solo_count(instructor):
        return sum(len(submission) == 1 for submission in partition[instructor])
    def assigned_group_count(instructor):
        return sum(len(submission) > 1 for submission in partition[instructor])

    maxInstructor = None
    maxDiff = -1

    for instructor in partition.keys():
        if solo:
            currDiff = data.solo_grade_count(instructor) - assigned_solo_count(instructor)
        else:
            currDiff = data.group_grade_count(instructor) - assigned_group_count(instructor)

        if currDiff > maxDiff:
            maxDiff = currDiff
            maxInstructor = instructor

    return maxInstructor