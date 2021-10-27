# This file reads the course info pickle, processes the data, and call the course importer
# to upload the courses to the AWS tables.
import pandas as pd
import numpy as np
import sys
sys.path.append('./modules')
from CourseTable import CourseTable
from DiscussionTable import DiscussionTable

def get_pickle_df(pickle_file, index):
    # Read the pickle containing the course data 
    df = pd.read_pickle(pickle_file).set_index(index)
    # Replace any NaN's with empty strings
    df = df.replace(np.nan, "")
    return df

def get_courses_table():
    return CourseTable()

def get_discussion_table():
    return DiscussionTable()

def upload_courses(df, course_table, discussion_table, num_courses=20):
    # Read each course, save the nessecary fields, and call the CourseImporter
    i = 0
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
        course_table.add_item(params)
        discussion_table.add_item(params["CourseID"])

def main():
    course_table = get_courses_table()
    discussion_table = get_discussion_table()
    df = get_pickle_df('resources/df_processed.pickle', 'Code')
    
    upload_courses(df, course_table, discussion_table, num_courses=20)

if __name__ == "__main__":
    main()
    