import pytest
from util import upload_courses

class MockedDataFrame:
    def __init__(self, rows=10):
        self.rows = [
            (f'TEST00{i}', {
                'Name': f'Test Course {i}',
                'Division': 'TEST division',
                'Course Description': 'TEST description',
                'Department': 'TEST department',
                'Course Level': 0,
                'Pre-requisites': [f'TEST00{i+1}'],
                'Campus': 'TEST campus',
                'Term': 'Fall',
                'MajorsOutcomes': [],
                'MinorsOutcomes': []
            }) for i in range(rows)
        ]

    def iterrows(self):
        return self.rows

    def replace(self, *args, **kwargs):
        pass

class MockedTable:
    def add_item(self, item):
        print("Mocked add item")
        pass

@pytest.fixture
def course_table_mock():
    return MockedTable()

@pytest.fixture
def discussion_table_mock():
    return MockedTable()

# Written by Gurmehar Sandhu
def test_upload_one_courses(mocker, course_table_mock, discussion_table_mock):
    df = MockedDataFrame(rows=1)
    courses_add_item_spy = mocker.spy(course_table_mock, 'add_item')
    discussion_add_item_spy = mocker.spy(discussion_table_mock, 'add_item')
    
    upload_courses.upload_courses(
        df, course_table_mock, discussion_table_mock, num_courses=5)
    
    assert courses_add_item_spy.call_count == 1
    discussion_add_item_spy.assert_called_once_with(df.iterrows()[0][0])

# Written by Gurmehar Sandhu
def test_upload_courses_limit(mocker, course_table_mock, discussion_table_mock):
    df = MockedDataFrame(rows=20)
    courses_add_item_spy = mocker.spy(course_table_mock, 'add_item')
    discussion_add_item_spy = mocker.spy(discussion_table_mock, 'add_item')
    
    upload_courses.upload_courses(
        df, course_table_mock, discussion_table_mock, num_courses=5)
    
    assert courses_add_item_spy.call_count == 5
    assert discussion_add_item_spy.call_count == 5

# Written by Gurmehar Sandhu
def test_upload_courses_main(mocker, course_table_mock, discussion_table_mock):
    courses_add_item_spy = mocker.spy(course_table_mock, 'add_item')
    discussion_add_item_spy = mocker.spy(discussion_table_mock, 'add_item')
    mocker.patch('util.upload_courses.get_pickle_df', return_value=MockedDataFrame(rows=10))
    mocker.patch('util.upload_courses.get_courses_table', return_value=course_table_mock)
    mocker.patch('util.upload_courses.get_discussion_table', return_value=discussion_table_mock)

    upload_courses.main()

    assert courses_add_item_spy.call_count == 10
    assert discussion_add_item_spy.call_count == 10