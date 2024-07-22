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
            reg_no VARCHAR(50),
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
        print("*================Welcome to the world's largest central library====================*\n")
    
    def display_books(self):
        try:
            books = con.execute('SELECT * FROM books')
            print("List of books present in this library:")
            for book in books:
                print(f"\t* {book}")
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
            book_ids = con.execute('SELECT book_id FROM reports WHERE mode="return"')
            for book_id in book_ids:
                book_details = con.execute('SELECT * FROM returnbook WHERE book_id=?', (book_id[0],))
                for details in book_details:
                    con.execute('''
                        INSERT INTO books (book_id, book_name, book_price, book_edition, book_category, publisher_name, publication_year)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', details)
                    con.commit()
            print("Thanks for returning this book within the time limit.")
        except s.Error as e:
            print(f"Error returning book: {e}")

    def take_books(self):
        try:
            book_ids = con.execute('SELECT book_id FROM reports WHERE mode="take"')
            for book_id in book_ids:
                con.execute('DELETE FROM books WHERE book_id=?', (book_id[0],))
                con.commit()
        except s.Error as e:
            print(f"Error taking book: {e}")

    def issue_books(self):
        try:
            book_ids = con.execute('SELECT book_id FROM reports WHERE mode="issue"')
            for book_id in book_ids:
                if book_id:
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
                return False
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
            st_id = int(input("Enter student id: "))
            name = input("Enter name: ")
            reg_no = input("Enter your Registration number: ")
            book_id = int(input("Enter book id: "))
            mode = input("Enter mode (issue/return/take): ")
            date = input("Enter date in DD/MM/YYYY: ")

            con.execute('''
                INSERT INTO reports (user_id, st_name, book_id, reg_no, mode, date)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (st_id, name, book_id, reg_no, mode, date))
            
            con.commit()
        except s.Error as e:
            print(f"Error adding report: {e}")
        except ValueError as ve:
            print(f"Invalid input: {ve}")
    
    def give_reports(self):
        try:
            reports = con.execute('SELECT * FROM reports')
            for report in reports:
                print(report)
        except s.Error as e:
            print(f"Error fetching reports: {e}")

class Staff:
    def take_staff_data(self):
        try:
            print("List of staff that works in the Library.")
            staff_id = int(input("Enter staff id: "))
            staff_name = input("Enter staff name: ")
            staff_salary = int(input("Enter current salary of staff: "))

            con.execute('''
                INSERT INTO staff (staff_name, staff_id, staff_salary)
                VALUES (?, ?, ?)
            ''', (staff_name, staff_id, staff_salary))
            
            con.commit()
        except s.Error as e:
            print(f"Error adding staff data: {e}")
        except ValueError as ve:
            print(f"Invalid input: {ve}")

    def give_staff_data(self):
        try:
            staff = con.execute('SELECT * FROM staff')
            print("Staff details are below:")
            for member in staff:
                print(member)
        except s.Error as e:
            print(f"Error fetching staff data: {e}")

# Library objects
lib = Library()
std = Student()
auth = Authentication()
bk = Books()
rp = Reports()
sf = Staff()

# Working
lib.greet()
if auth.add_user():
    if auth.login():
        user_type = int(input("Enter [0]: Library manager, [1]: Student, [2]: Staff\nEnter: "))
        
        if user_type == 0:
            enter = int(input("Enter [0]: Input Data, [1]: View Data\nEnter: "))
            if enter == 0:
                data_entry = int(input("Enter [0]: Input Books data, [1]: Enter College student data\nEnter: "))
                if data_entry == 0:
                    bk.ins_book()
                elif data_entry == 1:
                    std.college_student()
            elif enter == 1:
                view_data = int(input("Enter [0]: Display Books, [1]: College Student List, [2]: See Book Report, [3]: Staff Details\nEnter: "))
                if view_data == 0:
                    lib.display_books()
                elif view_data == 1:
                    lib.college_student_list()
                elif view_data == 2:
                    print("Name of students that benefit from the library:")
                    rp.give_reports()
                elif view_data == 3:
                    sf.give_staff_data()
        
        elif user_type == 1:
            enter = int(input("Enter [0]: Take Book, [1]: Return Book, [2]: Issue Book\nEnter: "))
            if enter == 0:
                if rp.take_reports():
                    lib.display_books()
                    std.take_books()
            elif enter == 1:
                if rp.take_reports():
                    std.return_book()
            elif enter == 2:
                if rp.take_reports():
                    std.issue_books()
        
        elif user_type == 2:
            sf.take_staff_data()
        else:
            print("Invalid User.")
else:
    print("User registration failed.")

con.close()
