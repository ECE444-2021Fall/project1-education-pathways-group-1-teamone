# project1-education-pathways-group-1-teamone

project1-education-pathways-group-1-teamone created by GitHub Classroom

# Project description and purpose

The objective of the application is to provide both students and course coordinators at the University of Toronto (U of T) with course-related insights and guidance. This will be achieved by implementing an intuitive user interface, creating an intelligent course searching algorithm, displaying course-specific information, providing a venue for course-related discussions, and tracking course selections with enrolment paths all in one platform. The primary benefit of the application is to save users time and effort during the course selection and curriculum planning process.

# Project Management Tool

The team will follow [Agile](https://www.atlassian.com/agile) development life cycle. For the project management tool, the team will utilize [Zenhub](https://www.zenhub.com/) as an add-on to raise issues, assign tasks and track work progress inside this repository. Here is the link to our board: [ECE444-Team1-Board](https://github.com/ECE444-2021Fall/project1-education-pathways-group-1-teamone/blob/develop/Contribution.md#workspaces/onecourse-development-615b3fecc87d88001751a0c0/board?repos=406422636)

# Built With

- [Flask](https://flask.palletsprojects.com/en/2.0.x/)
- [Jinja](https://jinja.palletsprojects.com/en/3.0.x/)
- [AWS](https://aws.amazon.com/)

# Backend

The project backend is split up into two overarching sections: **modules** and **lambdas**.

The modules (located in the `modules` directory) act as a data abstraction layer for this project. The modules mainly consist of Python classes that wrap interactions with AWS DynamoDB (DDB) tables. The interactions are wrapped to enable usage of coding best practices, providing more consistent and concise behaviour pertaining to the use to DDB tables.

The lambdas (located in the `lambdas` directory) make up the backend API, enabling abstracted interactions between the frontend application and the project's data layer. The lambdas expose endpoints that can be used to perform CRUD operations on AWS DynamoDB tables (i.e. lambdas utilize the aforementioned modules), as well as trigger more complex operations; such as the utilization of AWS OpenSearch (formerly ElasticSearch) to perform searches on the courses database(s).
