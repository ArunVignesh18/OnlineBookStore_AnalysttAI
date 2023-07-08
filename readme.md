BooksEra - A BookStore Application

The project is built in Python using Django Framework and javascript for frontend. The API used for the project is Django REST API

The website has admin and user login. The admin and user have different powers alloted for them. Running the project gets you to login page in which there is a option to signUp for new account. Creating a new account using the SignUp option, will create the account as a user only. To create a admin account, you can do it only through the terminal using the django command 'python manage.py createsuperuser'.

For test purpose, I have created a admin account and a user account.

ADMIN
username: anadmin
password: anad321
email-id: analyst@123.com

NORMAL USER
user: ksera
password: dobby

You can create as much as user accounts through the SignUp Option.

List of Pages available in the application - Login - Signup - Dashboard/Home - Add Book - Add Genre - View Book - Cart

The books are displayed in the Dashboard/Home Page with with search and filter options for details of the books. To view a particular book's details, there is button called 'View Book' in below each book.

ADMIN
    1. The admin can add new books to the application with its details such as - title - author - description - Price - Rating - Genres - Publication Date
This can be done in 'Add Book' page.

    2. The admin can also add new genres to the genres list which is not available before, and this can be done in the 'Add Genre' page.

    3. The admin can remove any existing book, and doing this will remove the book permanently. i.e. It remove the book from the cart too, if someone added to the cart before. This can be done by clicking the 'Remove Book' button in the dashboard page.

USER
    1. The user can go through the books in the dashboard and do the searches and filters for their requirements.

    2. The user can add a book to the cart for buying, which can be done by clicking 'Add To Cart' button below each book in the dashboard page.

    3. The user can see the books they have added to the cart before in the 'Cart' page.

    4. The user can remove a book from cart, if they don't want it.

    5. There is a 'Buy Now' button in cart page at the bottom, which don't have any functionality. Since we can't buy books in this project, I didn't place any function for that buttom.

This is the web application called BooksEra and it have all functions of a Book Store Application and user-friendly.
