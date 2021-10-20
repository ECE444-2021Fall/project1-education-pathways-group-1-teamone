import pandas as pd
import numpy as np
from modules.CourseImporter import CourseImporter


if __name__ == "__main__":
    importer = CourseImporter()
    df = pd.read_pickle('resources/df_processed.pickle').set_index('Code')
    df = df.replace(np.nan, "")
    
    num_courses = 20
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
        importer.create_course(params)
        