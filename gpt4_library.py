import sqlite3 as s
from datetime import datetime

# Create database connection
try:
    con = s.connect("Student_library.db")
except s.Error as e:
    print(f"Error connecting to database: {e}")
    exit()

# Create tables if they do not exist
try:
    con.execute('''
        CREATE TABLE IF NOT EXISTS student (
            student_id INTEGER PRIMARY KEY NOT NULL,
            student_reg_no VARCHAR(50),
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            phone_no VARCHAR(15),
            address VARCHAR(50),
            email TEXT
        )
    ''')

    con.execute('''
        CREATE TABLE IF NOT EXISTS books (
            book_id INTEGER PRIMARY KEY NOT NULL,
            book_name VARCHAR(50),
            book_price VARCHAR(50),
            book_edition VARCHAR(50),
            book_category VARCHAR(70),
            publisher_name VARCHAR(70),
            publication_year VARCHAR(50)
        )
    ''')

    con.execute('''
        CREATE TABLE IF NOT EXISTS returnbook (
            book_id INTEGER PRIMARY KEY NOT NULL,
            book_name VARCHAR(50),
            book_price VARCHAR(50),
            book_edition VARCHAR(50),
            book_category VARCHAR(70),
            publisher_name VARCHAR(70),
            publication_year VARCHAR(50)
        )
    ''')

    con.execute('''
        CREATE TABLE IF NOT EXISTS staff (
            staff_name VARCHAR(50),
            staff_id INTEGER PRIMARY KEY NOT NULL,
            staff_salary INTEGER
        )
    ''')

    con.execute('''
        CREATE TABLE IF NOT EXISTS authentication (
            si_no INTEGER PRIMARY KEY AUTOINCREMENT,
            login_id VARCHAR NOT NULL,
            password VARCHAR(8) NOT NULL,
            date_time DATETIME
        )
    ''')

    con.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            user_id INTEGER NOT NULL,
            st_name VARCHAR(50),
            book_id INTEGER,
            mode VARCHAR(50),
            date VARCHAR(10),
            PRIMARY KEY (user_id, book_id, mode)
        )
    ''')
except s.Error as e:
    print(f"Error creating tables: {e}")
    exit()


class Library:
    def greet(self):
        print('''*================Welcome to the world largest central library====================*\n''')

    def display_books(self):
        try:
            books = con.execute('SELECT * FROM books')
            print("List of books present in this library ............")
            for book in books:
                print(f"\t  *  {book}")
        except s.Error as e:
            print(f"Error displaying books: {e}")

    def college_student_list(self):
        try:
            students = con.execute('SELECT * FROM student')
            print("List of students:")
            for student in students:
                print(f"\t* {student}")
        except s.Error as e:
            print(f"Error displaying students: {e}")


class Student:
    def college_student(self):
        try:
            st_id = int(input("Enter student id: "))
            f_name = input("Enter First name: ")
            l_name = input("Enter Last name: ")
            s_phone = input("Enter your phone number: ")
            st_registration = input("Enter Registration number: ")
            s_address = input("Enter Address: ")
            s_mail = input("Enter email_id: ")

            con.execute('''
                INSERT INTO student (student_id, first_name, last_name, phone_no, student_reg_no, address, email)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (st_id, f_name, l_name, s_phone, st_registration, s_address, s_mail))

            con.commit()
        except s.Error as e:
            print(f"Error adding student: {e}")
        except ValueError as ve:
            print(f"Invalid input: {ve}")

    def return_book(self):
        try:
            book_id = int(input("Enter your book id: "))
            book_details = con.execute('SELECT * FROM books WHERE book_id=?', (book_id,)).fetchone()

            if book_details:
                con.execute('''
                    INSERT INTO returnbook (book_id, book_name, book_price, book_edition, book_category, publisher_name, publication_year)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', book_details)

                con.execute('DELETE FROM books WHERE book_id=?', (book_id,))
                con.commit()
                print("Thanks for returning this book within the time limit.")
            else:
                print("Book not found in books.")
        except s.Error as e:
            print(f"Error returning book: {e}")

    def take_books(self):
        try:
            k = con.execute('SELECT book_id FROM reports WHERE mode="take"')
            for j in k:
                con.execute('DELETE FROM books WHERE book_id=?', (j[0],))
                con.commit()
            print("Library Warning: your responsibility to keep this book safe and return within time-limit. Extra charge required if not returned on time. Thanks!")
        except s.Error as e:
            print(f"Error taking book: {e}")

    def issue_books(self):
        try:
            k = con.execute('SELECT book_id FROM reports WHERE mode="issue"')
            for j in k:
                print("Your book has been successfully issued.")
        except s.Error as e:
            print(f"Error issuing book: {e}")


class Authentication:
    def add_user(self):
        try:
            login_id = input("Enter your login_id: ")
            password = input("Enter your 8-digit password: ")

            existing_user = con.execute('SELECT login_id FROM authentication WHERE login_id=?', (login_id,)).fetchone()

            if existing_user:
                print("User already exists. Please log in.")
                return True
            else:
                date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                con.execute('INSERT INTO authentication (login_id, password, date_time) VALUES (?, ?, ?)', (login_id, password, date_time))
                con.commit()
                print("You have successfully registered! Please log in.")
                return True
        except s.Error as e:
            print(f"Error adding user: {e}")
            return False

    def login(self):
        try:
            login_id = input("Enter your login_id: ")
            password = input("Enter your 8-digit password: ")

            user = con.execute('SELECT * FROM authentication WHERE login_id=? AND password=?', (login_id, password)).fetchone()

            if user:
                print("You have successfully logged into the central Library!")
                return True
            else:
                print("Invalid login credentials. Please try again.")
                return False
        except s.Error as e:
            print(f"Error logging in: {e}")
            return False


class Books:
    def ins_book(self):
        try:
            print("Add book data into library:")
            book_id = int(input("Enter book id: "))
            book_name = input("Enter book name: ")
            book_price = input("Enter book price: ")
            book_edition = input(f"Book {book_id} is which edition: ")
            book_category = input("Enter book category: ")
            publisher_name = input("Enter publisher name: ")
            publ_year = input("Enter year of publication: ")

            con.execute('''
                INSERT INTO books (book_id, book_name, book_price, book_edition, book_category, publisher_name, publication_year)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (book_id, book_name, book_price, book_edition, book_category, publisher_name, publ_year))

            con.commit()
        except s.Error as e:
            print(f"Error adding book: {e}")
        except ValueError as ve:
            print(f"Invalid input: {ve}")


class Reports:
    def take_reports(self):
        try:
            print("List of students who take books from the Library.")
            st_id = int(input("Enter student id: "))
            name = input("Enter name: ")
            book_id = int(input("Enter book id for take reports: "))
            mode = input("Enter mode (issue/return/take): ")
            date = input("Enter date in DD/MM/YYYY: ")

            con.execute('''
                INSERT INTO reports (user_id, st_name, book_id, mode, date)
                VALUES (?, ?, ?, ?, ?)
            ''', (st_id, name, book_id, mode, date))

            if mode == "return":
                book_details = con.execute('SELECT * FROM books WHERE book_id=?', (book_id,)).fetchone()
                if book_details:
                    con.execute('''
                        INSERT INTO returnbook (book_id, book_name, book_price, book_edition, book_category, publisher_name, publication_year)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', book_details)
                    con.execute('DELETE FROM books WHERE book_id=?', (book_id,))
                    con.commit()
            return True
        except s.Error as e:
            print(f"Error adding report: {e}")
        except ValueError as ve:
            print(f"Invalid input: {ve}")

    def give_reports(self):
        try:
            k = con.execute('SELECT * FROM reports')
            for j in k:
                print(j)
        except s.Error as e:
            print(f"Error fetching reports: {e}")


class Staff:
    def take_staff_data(self):
        try:
            print("Please enter the information about the staff of Central Library.")
            id = int(input("Enter staff id: "))
            name = input("Enter staff name: ")
            salary = int(input("Enter current salary of staff: "))

            con.execute('''
                INSERT INTO staff (staff_name, staff_id, staff_salary)
                VALUES (?, ?, ?)
            ''', (name, id, salary))

            con.commit()
        except s.Error as e:
            print(f"Error adding staff data: {e}")
        except ValueError as ve:
            print(f"Invalid input: {ve}")

    def give_staff_data(self):
        try:
            k = con.execute("SELECT * FROM staff")
            print("Staff details are below:\n")
            for j in k:
                print(j)
        except s.Error as e:
            print(f"Error fetching staff data: {e}")


# Library objects
lib = Library()
std = Student()
auth = Authentication()
bk = Books()
rp = Reports()
sf = Staff()
lib.greet()
n = 100

# Working
for i in range(n):
    print("==========================================================================================================================================================")
    print(f"This is your chance: {i+1} login.")

    # User registration and login
    if auth.add_user():
        print("Please log in now.")
        if auth.login():
            a = int(input("Enter[0]:Library manager, Enter[1]:Student, Enter[2]:Staff\nEnter: "))

            # Library manager
            if a == 0:
                print("======================Welcome Library Manager==========================\n")
                enter = int(input("Enter[0]:Input-Data, Enter[1]:View data \nEnter: "))
                if enter == 0:
                    data_input = int(input("Enter [0]: Input Books Data, [1]: Enter College Student Data\nEnter: "))

                    if data_input == 0:
                        bk.ins_book()
                    elif data_input == 1:
                        std.college_student()

                elif enter == 1:
                    check = int(input("Enter[0]:Display_Books, Enter[1]:College_student_List, Enter[2]:See Book Report, Enter[3]:Staff Details. \nEnter: "))
                    if check == 0:
                        lib.display_books()
                    elif check == 1:
                        lib.college_student_list()
                    elif check == 2:
                        print("Name of students that take benefits from the library.\n")
                        rp.give_reports()
                    elif check == 3:
                        sf.give_staff_data()

            # Student
            elif a == 1:
                print("======================Welcome Dear Student==========================\n")
                enter = int(input("Enter[0]:Take_Book, Enter[1]:Return_Book, Enter[2]:Issue_Book\nEnter: "))
                if enter == 0:
                    lib.display_books()
                    rp.take_reports()
                    std.take_books()
                elif enter == 1:
                    rp.take_reports()
                    std.return_book()
                    print("=============Thanks for choosing this Library.===================")
                elif enter == 2:
                    std.issue_books()
                    rp.take_reports()

            # Staff
            elif a == 2:
                sf.take_staff_data()
            else:
                print("Invalid User.")
    else:
        print("User registration failed.")

con.close()
