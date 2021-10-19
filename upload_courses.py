import pandas as pd
from modules.CourseImporter import CourseImporter

if __name__ == "__main__":
    importer = CourseImporter()
    df = pd.read_pickle('resources/df_processed.pickle').set_index('Code')
    num_courses = 20
    i = 0
    for index, course in df.iterrows():
        i += 1
        if i > num_courses or index=="CDPD01H3":
            print(course)
            print(type (course['Course Description']))
            break
            
        # TODO: NULL CHECK HERE
        params = {
            "CourseID": index,
            "Name": course['Name'],
            "Division": course['Division'],
            "Description": course['Course Description'],
            "Department": course['Department'],
            "Level": course['Course Level']
        }
        
        print(f"Creating {index}")
        # importer.create_course(params)
        