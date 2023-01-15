<h1 align="center"><u>REPORT</u></h1>

***Author:***

- *<u>Name</u>* - Akhil Vashistha
- *<u>Roll Number</u>* - 21f3001417
- *<u>Student Email</u>* - 21f3001417@student.onlinedegree.iitm.ac.in
- *<u>Details</u>* - I am a diploma level student in this Online BS degree program. I have a keen interest in exploring the different realms of Technology and thus I wish to accomplish this degree with utmost dedication and hard work. I am very thankful to IIT Madras for providing me this opportunity to develop such an interesting web application and making my journey interesting!

***Description:***

In this project, I have designed a **blogging application**. It is a multiple user application that allows users to create, edit and delete posts, search, follow and unfollow other users. Each user will have a **My Dashboard** page to check their feed that will display blog posts from the users followed by them sorted by newer to older. There is a **My Profile** page for each user where they can edit or delete a blog posted by them. Moreover, each user will also have a **Public Profile** page to display user details (follower count, following count, post count, followers list and following list) and user activity (blogs posted by them). On this page, there is an option to follow/unfollow the user. Also, there is a search utility inside the application that allows a user to search for other users based on their first names, last names, email ids or usernames. 

***Libraries Used:***

1. *<u>Flask</u>* - developing web applications using python.
2. *<u>Flask-sqlalchemy</u>* - used to create database schema and tables using SQLAlchemy with Flask by providing defaults and helpers.
3. *<u>Datetime</u>* - a python module which supplies classes to work with date and time. Here, datetime module to create timestamp in the application.
4. *<u>render_template</u>* - used to render html templates based on the Jinja2 engine that is found in the application's templates folder.
5. *<u>request</u>* - used to handle HTTP requests and responses.
6. *<u>redirect</u>* - used to redirect a user to another endpoint using a specified URL and assign a specified status code.
7. *<u>session</u>* - Flask extension supports Server-side session to our application.
8. *<u>before_first_request</u>* - helps us to execute the code at least once before a user arrives, before the first request arrives
9. *<u>route</u>* - used to bind the specific URL with the associated function that is intended to perform some tasks.
10. *<u>Image(PIL)</u>* - used the image module inside pillow package to save the blog images posted by users.

***Database Schema:***

- **Relation**- A user can have many posts and thus we have one-to-many relationship between **User** and **Post**. A secondary table- **UserPosts** is used to establish one-to-many relationship with User and Post.

***Architecture and Features:***

The project code is organised based on its utility in different files and directories. I have named the root directory of my project as **Blog_Lite**. Inside this directory there is a python file **app.py**; **Blog_Lite/static** containing all the files required  for the application; **Blog_Lite/templates** contains all the HTML (Jinja) files; **Blog_Lite/report** containing the pdf report file(a short description of the application) and; **Blog_Lite/Database** containing a python file **module.py** (used to develop the databases). The following are the html pages used in the application: login, signup, result, dashboard, pub_profile,pvt_profile and edit_post.

***Flowchart of Tracker App:***

- @app.before_first_request
- @app.route('/', methods=['POST', 'GET'])
- @app.route('/signup', methods=['POST', 'GET'])
- @app.route('/login', methods=['POST', 'GET'])
- @app.route('/<string:current_user>', methods=['POST', 'GET'])
- @app.route('/<string:current_user>/search', methods=['POST'])
- @app.route('/<string:current_user>/search?name=<string:user_query>', methods=['GET'])
- @app.route('/<string:current_user>/<string:user_profile>/profile', methods=['POST', 'GET'])
- @app.route('/<string:current_user>/account', methods=['POST', 'GET'])
- @app.route('/<string:current_user>/<string:user_profile>/follow', methods=['GET'])
- @app.route('/<string:current_user>/<string:user_profile>/unfollow', methods=['GET'])
- @app.route('/<string:current_user>/<int:post_id>/edit_post', methods=['GET', 'POST'])
- @app.route('/<string:current_user>/<int:post_id>/delete_post', methods=['GET'])

***Video***