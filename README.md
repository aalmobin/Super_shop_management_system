# Super_shop_management_system
Basic functionality of a super shop management system

## Python version: 3.9+

## Instructions to run the Project

1. Goto the directory where you want to store your project.
2. Clone the git repository to the project directory.
3. Open the terminal and navigate to the project directory from the terminal.
4. Create virtual environment from the terminal by typing ```virtualenv venv``` and activate it by typing `source venv/bin/activate`(for Linux), `venv\Scripts\activate`(for Windows).
    * If you don't have `virtualenv` installed then install it by typing `pip install virtualenv`.
5. Install the project dependencies by typing `pip install -r requirements.txt` on the terminal. 
6. Create a file named .env and paste the following 
   * `SECRET_KEY = django-insecure-g^43cl^05x03*!#jgk1j7r2)^c$sx0uaay^(%=5djn!=5!-5$l`
7. Migrate the database by typing `python manage.py makemigrations` and then `python manage.py migrate` on the terminal.
8. Create admin user if you want by typing `python manage.py createsuperuser` and give the required credentials on the terminal.
9. Now, Run the project from your **localhost** by typing `python manage.py runserver`
10. Navigate to the URL [127.0.0.1:8000](127.0.0.1:8000) or [localhost:8000](localhost:8000) from your browser.
11. Please log in to the admin panel and create Category and Products as you like by the following link
    * `127.0.0.1:8000/admin`    
12. You can terminate the server anytime by **CTRL+c**.