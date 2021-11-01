from project.app import app
import requests 

#Joshua Pius
def user_login(valid):
    """Test LogIn using helper function"""
    valid_user = {'username': 'Admin', 'password': 'CorrectPassword'}
    invalid_user = {'username': 'Admin', 'password': 'IncorrectPassword'}    
    if (valid):
    	return app.test_client().post(
        	"/login",
        	data=valid_usera,
        	follow_redirects=True
    	)
    else:
        return app.test_client().post(
                "/login",
                data=invalid_usera,
                follow_redirects=True
        )

#Joshua Pius
def test_logInIndex():
    """Test the GET/POST request to logIn page"""
    response = app.test_client().get("/login", content_type="html/text")
    assert response.status_code == 200

#Joshua Pius
def test_user_login():
    """Test valid user information is recognized"""
    res_post = user_login(true)
    assert res_get.status_code  == 200
    res_post = user_login(false)
    assert res_post.status_code  != 200
