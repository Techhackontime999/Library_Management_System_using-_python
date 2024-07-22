import sqlite3 as s

# Create the database connection
con = s.connect("Student_library.db")

# Create tables
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
    CREATE TABLE IF NOT EXISTS reservereturn (
        si_no INTEGER PRIMARY KEY NOT NULL,
        reserve_date VARCHAR(50),
        return_date VARCHAR(50),
        due_date VARCHAR(50)
    )
''')

con.execute('''
    CREATE TABLE IF NOT EXISTS authentication (
        login_id VARCHAR PRIMARY KEY NOT NULL,
        password VARCHAR(8)
    )
''')

con.execute('''
    CREATE TABLE IF NOT EXISTS reports (
        user_id INTEGER PRIMARY KEY NOT NULL,
        st_name VARCHAR(50),
        book_id INTEGER,
        reg_no VARCHAR(50),
        mode VARCHAR(50),
        date VARCHAR(8)
    )
''')

class Library:
    def greet(self):
        print("*================Welcome to the world's largest central library====================*\n")
    
    def display_books(self):
        books = con.execute('SELECT * FROM books')
        print("List of books present in this library:")
        for book in books:
            print(f"\t* {book}")

    def college_student_list(self):
        students = con.execute('SELECT * FROM student')
        print("List of students:")
        for student in students:
            print(f"\t* {student}")

class Student:
    def college_student(self):
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

    def return_book(self):
        book_ids = con.execute('SELECT book_id FROM reports WHERE mode="return"')
        for book_id in book_ids:
            book_details = con.execute('SELECT * FROM returnbook WHERE book_id=?', (book_id,))
            for details in book_details:
                con.execute('''
                    INSERT INTO books (book_id, book_name, book_price, book_edition, book_category, publisher_name, publication_year)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', details)
                con.commit()
        print("Thanks for returning this book within the time limit.")

    def take_books(self):
        book_ids = con.execute('SELECT book_id FROM reports WHERE mode="take"')
        for book_id in book_ids:
            con.execute('DELETE FROM books WHERE book_id=?', (book_id,))
            con.commit()

    def issue_books(self):
        book_ids = con.execute('SELECT book_id FROM reports WHERE mode="issue"')
        for book_id in book_ids:
            if book_id:
                print("Your book has been successfully issued.")

class Authentication:
    def add_user(self):
        login_id = input("Enter your login_id: ")
        password = input("Enter your 8-digit password: ")
        
        con.execute('INSERT INTO authentication (login_id, password) VALUES (?, ?)', (login_id, password))
        con.commit()
        return True

class Books:
    def ins_book(self):
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

class Reports:
    def take_reports(self):
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
    
    def give_reports(self):
        reports = con.execute('SELECT * FROM reports')
        for report in reports:
            print(report)

class Staff:
    def take_staff_data(self):
        print("List of staff that works in the Library.")
        staff_id = int(input("Enter staff id: "))
        staff_name = input("Enter staff name: ")
        staff_salary = int(input("Enter current salary of staff: "))

        con.execute('''
            INSERT INTO staff (staff_name, staff_id, staff_salary)
            VALUES (?, ?, ?)
        ''', (staff_name, staff_id, staff_salary))
        
        con.commit()

    def give_staff_data(self):
        staff = con.execute('SELECT * FROM staff')
        print("Staff details are below:")
        for member in staff:
            print(member)

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
    print("You have successfully logged into the central Library!")
    user_type = int(input("Enter [0]: Library Manager, [1]: Student, [2]: Staff\nEnter: "))
    
    if user_type == 0:
        action = int(input("Enter [0]: Input Data, [1]: View Data\nEnter: "))
        
        if action == 0:
            data_input = int(input("Enter [0]: Input Books Data, [1]: Enter College Student Data\nEnter: "))
            
            if data_input == 0:
                bk.ins_book()
            elif data_input == 1:
                std.college_student()
        
        elif action == 1:
            view_data = int(input("Enter [0]: Display Books, [1]: College Student List, [2]: See Book Report, [3]: Staff Details\nEnter: "))
            
            if view_data == 0:
                lib.display_books()
            elif view_data == 1:
                lib.college_student_list()
            elif view_data == 2:
                print("Names of students who have benefited from the library:")
                rp.give_reports()
            elif view_data == 3:
                sf.give_staff_data()
    
    elif user_type == 1:
        student_action = int(input("Enter [0]: Take Book, [1]: Return Book, [2]: Issue Book\nEnter: "))
        
        if student_action == 0:
            std.take_books()
            rp.take_reports()
        elif student_action == 1:
            rp.give_reports()
            std.return_book()
            rp.take_reports()
            print("Thanks for choosing this library.")
        elif student_action == 2:
            std.issue_books()
            rp.take_reports()
    
    elif user_type == 2:
        sf.take_staff_data()
    
    else:
        print("Invalid User.")
else:
    print("You are not a logged user.\nError: Kindly Try again!")

print("Thanks for visiting!")
con.close()
