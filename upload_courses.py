# This file reads the course info pickle, processes the data, and call the course importer
# to upload the courses to the AWS tables.
import pandas as pd
import numpy as np
from modules.CourseTable import CourseTable
from modules.DiscussionTable import DiscussionTable


if __name__ == "__main__":
    course_table = CourseTable()
    discussion_table = DiscussionTable()
    # Read the pickle containing the course data 
    df = pd.read_pickle('resources/df_processed.pickle').set_index('Code')
    # Replace any NaN's with empty strings
    df = df.replace(np.nan, "")
    # Only upload 20 courses for now 
    num_courses = 20
    i = 0
    # Read each course, save the nessecary fields, and call the CourseImporter
    for index, course in df.iterrows():
        i += 1
        if i > num_courses:
            break
        
        params = {
            "CourseID": index,
            "Name": course['Name'],
            "Division": course['Division'],
            "Description": course['Course Description'],
            "Department": course['Department'],
            "Level": course['Course Level'],
            "Prerequisites": list(course['Pre-requisites']),
            "Campus": course['Campus'],
            "Term": list(course['Term']),
            "MajorOutcomes": list(course['MajorsOutcomes']),
            "MinorOutcomes": list(course['MinorsOutcomes'])
        }

        print(f"Creating {index}")
        course_table.add_course(params)
        discussion_table.add_discussion_board(params["CourseID"])
        