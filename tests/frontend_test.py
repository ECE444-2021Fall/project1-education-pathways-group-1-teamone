from project.app import app


#Yuhui jiang
def make_search():
    """Search helper function"""
    data = {'faculty': 'Any', 'department': 'Any', 'campus': 'Any', 'keyword': '', 'course code': '', 'course year': '0'}
    return app.test_client().post(
        "/search",
        data=data,
        follow_redirects=True
    )
#Yuhui jiang
def test_index():
    """Test the GET/POST request to index page"""
    response = app.test_client().get("/", content_type="html/text")
    assert response.status_code == 200
#Yuhui jiang
def test_search():
    """Test the GET/POST request to search page"""
    res_get = app.test_client().get("/search", content_type="html/text")
    assert res_get.status_code  == 200
    res_post = make_search()
    assert res_post.status_code  == 200