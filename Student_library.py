'''
========================================Library Management System===================================================================
                        *Overview
The Library Management System is a robust application designed to streamline the management of a library's operations. The system provides functionalities for managing books, students, staff, and reports, while ensuring secure user authentication and comprehensive error handling. This system is implemented using Python and SQLite, ensuring a lightweight yet powerful solution for any library.

n                      *Functionalities*
Database Setup and Connection
Database Connection: Establishes a connection to the SQLite database named Student_library.db. If the connection fails, an error message is displayed.
Table Creation: Creates necessary tables (student, books, returnbook, staff, authentication, and reports) if they do not already exist, ensuring the database structure is in place.
                       *User Authentication*
Registration: Allows new users to register by providing a login_id and an 8-digit password. Checks for existing users to prevent duplicate registrations.
Login: Validates user credentials and grants access to the system if authentication is successful.
                      *Library Management*
Greeting: Welcomes users to the library with a custom message.
Display Books: Lists all the books available in the library, displaying detailed information about each book.
Student List: Displays a list of all registered students.
                       *Student Management*
Add Student: Allows the addition of new students to the library's database by collecting necessary information.
Return Book: Manages the process of returning books, updating the database accordingly.
Take Books: Handles the borrowing of books by students, updating the database and ensuring the book's status is tracked.
Issue Books: Manages the issuance of books, ensuring proper tracking and record maintenance.
                         *Book Management*
Add Book: Facilitates the addition of new books to the library's collection with detailed information about each book.
                          *Report Management*
Add Report: Allows the recording of transactions (issue, return, take) involving books, providing a comprehensive record of library activities.
View Reports: Displays a list of all reports, detailing the transactions involving students and books.
                           *Staff Management*
Add Staff: Enables the addition of new staff members to the library's database, collecting and storing relevant information.
View Staff: Displays detailed information about all library staff members.
                            *Error Handling*
The system employs robust error handling using Python's exception handling mechanism. Each database operation is wrapped in try-except blocks to catch and display any errors that occur, ensuring the system remains stable and user-friendly.



'''
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

    # issuing book table
    con.execute('''
    CREATE TABLE IF NOT EXISTS issuebook (
    s_i  integer  primary key autoincrement,
    student_id int not null,
    student_name varchar(50) ,
   book_name varchar(50),
   book_publication varchar(50) ,
   Date varchar(8) ,
   mode varchar(5)                                     
                                     
   )
    '''
   )



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
        n=int(input("Enter How many students you want to add : "))
        for i in range(n):
                 print("...................")
                 print(f"Add {i+1}th college student.")
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
        else:
            print("Students are Added successfully !")

    def return_book(self):
        try:
            
            id=int(input("Enter your book id : "))
            book_details = con.execute('SELECT * FROM returnbook WHERE book_id=?', (id,))
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
            k = con.execute('SELECT book_id FROM reports WHERE mode="take"')
            for j in k:
                con.execute('DELETE FROM books WHERE book_id=?', (j[0],))
                con.commit()
            print("Library Warning: your responsibility to keep this book safe and return within time-limit. Extra charge required if not returned on time. \nThanks!")
        except s.Error as e:
            print(f"Error taking book: {e}")

    def issue_books(self):
        try:
            print("Your book  has been issueing successfully .")       
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
        n=int(input("How many Books you want to store in Library : "))
        for i in range(n):
          print("...................")
          print(f"your {i+1}th book.")
          try:
             print("Add book data into library:")
             book_id = int(input("Enter book id: "))
             book_id1=book_id
             book_name = input("Enter book name: ")
             book_name1=book_name
             book_price = input("Enter book price: ")
             book_price1=book_price
             book_edition = input(f"Book {book_id} is which edition: ")
             book_edition1=book_edition
             book_category = input("Enter book category: ")
             book_category1=book_category
             publisher_name = input("Enter publisher name: ")
             publisher_name1=publisher_name
             publ_year = input("Enter year of publication: ")
             publ_year1=publ_year
        
             con.execute('''
            INSERT INTO books (book_id, book_name, book_price, book_edition, book_category, publisher_name, publication_year)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (book_id, book_name, book_price, book_edition, book_category, publisher_name, publ_year))
        
             con.commit()
             con.execute('''
            INSERT INTO returnbook (book_id, book_name, book_price, book_edition, book_category, publisher_name, publication_year)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (book_id1, book_name1, book_price1, book_edition1, book_category1, publisher_name1, publ_year1))
        
             con.commit()
          except s.Error as e:
            print(f"Error adding book: {e}")
          except ValueError as ve:
            print(f"Invalid input: {ve}")  
         
        else:
          print("Books is Added successfully !")   

class Reports:
    def take_reports(self):
        try:
            # print("List of students who take books from the Library.")
            st_id = int(input("Enter student id: "))
            name = input("Enter your name: ")
            mode = input("Enter mode (issue/return/take): ")
            date = input("Enter date in DD/MM/YYYY: ")
            if mode=="take":
                 book_id = int(input("Enter book id for take reports: "))
                 con.execute('''
                  INSERT INTO reports (user_id, st_name, book_id, mode, date)
                  VALUES (?, ?, ?, ?, ?)
              ''', (st_id, name, book_id, mode, date))
            if mode=="return":
                book_id = int(input("Enter book id for take reports: "))
                con.execute('''
                  INSERT INTO reports (user_id, st_name, book_id, mode, date)
                  VALUES (?, ?, ?, ?, ?)
              ''', (st_id, name, book_id, mode, date))

            if mode=="issue":
                  b=input("Enter your order book_name : ")
                  c=input("Enter book publication name : ")
                  con.execute('''insert into issuebook (student_id,student_name,book_name,book_publication,Date,mode)
                  values (?,?,?,?,?,?)
''',(st_id,name,b,c,date,mode))
                  con.commit()
            if mode == "return":
                k = con.execute("SELECT * FROM books WHERE book_id=?", (book_id,)).fetchone()
                if k:
                    con.execute('''
                        INSERT INTO returnbook (book_id, book_name, book_price, book_edition, book_category, publisher_name, publication_year)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', k)
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
            print("List of staff that works in the Library.")
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
                    check = int(input("Enter[0]:Display_Books, Enter[1]:College_student_List, Enter[2]:See Book Report, Enter[3]:Staff Details ,Enter[4]:see issued books. \nEnter: "))
                    if check == 0:
                        lib.display_books()
                    elif check == 1:
                        lib.college_student_list()
                    elif check == 2:
                        print("Name of students that take benefits from the library.\n")
                        rp.give_reports()
                    elif check == 3:
                        sf.give_staff_data()
                    elif check==4:
                        print("Students give issues for books.! please books provide to the Library.")
                        con.execute('''select * from issuebook''')
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
                    rp.take_reports()
                    std.issue_books()

            # Staff
            elif a == 2:
                sf.take_staff_data()
            else:
                print("Invalid User.")
    else:
        print("User registration failed.")

con.close()






















































# this below line written by me.



# import sqlite3 as s
# from datetime import datetime

# # Create database connection
# try:
#     con = s.connect("Student_library.db")
# except s.Error as e:
#     print(f"Error connecting to database: {e}")
#     exit()
# # Create tables if they do not exist
# try:
#     con.execute('''
#         CREATE TABLE IF NOT EXISTS student (
#             student_id INTEGER PRIMARY KEY NOT NULL,
#             student_reg_no VARCHAR(50),
#             first_name VARCHAR(50),
#             last_name VARCHAR(50),
#             phone_no VARCHAR(15),
#             address VARCHAR(50),
#             email TEXT
#         )
#     ''')

#     con.execute('''
#         CREATE TABLE IF NOT EXISTS books (
#             book_id INTEGER PRIMARY KEY NOT NULL,
#             book_name VARCHAR(50),
#             book_price VARCHAR(50),
#             book_edition VARCHAR(50),
#             book_category VARCHAR(70),
#             publisher_name VARCHAR(70),
#             publication_year VARCHAR(50)
#         )
#     ''')
#     # all books data present in returnbook table

#     con.execute('''
#         CREATE TABLE IF NOT EXISTS returnbook (
#             book_id INTEGER PRIMARY KEY NOT NULL,
#             book_name VARCHAR(50),
#             book_price VARCHAR(50),
#             book_edition VARCHAR(50),
#             book_category VARCHAR(70),
#             publisher_name VARCHAR(70),
#             publication_year VARCHAR(50)
#         )
#     ''')

#     con.execute('''
#         CREATE TABLE IF NOT EXISTS staff (
#             staff_name VARCHAR(50),
#             staff_id INTEGER PRIMARY KEY NOT NULL,
#             staff_salary INTEGER
#         )
#     ''')

#     con.execute('''
#         CREATE TABLE IF NOT EXISTS authentication (
#             si_no INTEGER PRIMARY KEY AUTOINCREMENT,
#             login_id VARCHAR NOT NULL,
#             password VARCHAR(8) NOT NULL,
#             date_time DATETIME
#         )
#     ''')

#     con.execute('''
#         CREATE TABLE IF NOT EXISTS reports (
#             user_id INTEGER NOT NULL,
#             st_name VARCHAR(50),
#             book_id INTEGER,
#             mode VARCHAR(50),
#             date VARCHAR(10),
#             PRIMARY KEY (user_id, book_id, mode)
#         )
#     ''')
# except s.Error as e:
#     print(f"Error creating tables: {e}")
#     exit()


# class Library:
#     def greet(self):
#         print('''*================Welcome to the world largest central library====================*\n''')
#     def displaybooks(self):
#         try:
#            books=con.execute( '''select * from books''')
#            print("List of books present in this library ............")
#            for i in books:
#                 print(f"\t  *  {i}")
#         except s.Error as e:
#             print(f"Error displaying books: {e}")        

#     def college_student_list(self):
#         try:
#             students = con.execute('SELECT * FROM student')
#             print("List of students:")
#             for student in students:
#                 print(f"\t* {student}")
#         except s.Error as e:
#             print(f"Error displaying students: {e}")


# class Student:
#     try:
#        def college_student(self):
#            st_id = int(input("Enter student id: "))
#            f_name = input("Enter First name: ")
#            l_name = input("Enter Last name: ")
#            s_phone = input("Enter your phone number: ")
#            st_registration = input("Enter Registration number: ")
#            s_address = input("Enter Address: ")
#            s_mail = input("Enter email_id: ")
        
#            con.execute('''
#                INSERT INTO student (student_id, first_name, last_name, phone_no, student_reg_no, address, email)
#                VALUES (?, ?, ?, ?, ?, ?, ?)
#            ''', (st_id, f_name, l_name, s_phone, st_registration, s_address, s_mail))
        
#            con.commit()
#     except s.Error as e:
#             print(f"Error adding student: {e}")
#     except ValueError as ve:
#             print(f"Invalid input: {ve}")

#     def return_book(self):
#         try:
            
#             id=int(input("Enter your book id : "))
#             book_details = con.execute('SELECT * FROM returnbook WHERE book_id=?', (id,))
#             for details in book_details:
#                     con.execute('''
#                         INSERT INTO books (book_id, book_name, book_price, book_edition, book_category, publisher_name, publication_year)
#                         VALUES (?, ?, ?, ?, ?, ?, ?)
#                     ''', details)
#                     con.commit()
#             print("Thanks for returning this book within the time limit.")
        
#         except s.Error as e:
#             print(f"Error returning book: {e}")


#     def takebooks(self):
#         try:
#            k=con.execute('''select book_id from reports where mode="take" ''')
#            for j in k:
#                ins='''delete from books where book_id="{}"'''.format(j) 
#                print("Library Warning : your responsiblity to keep this book safe and return within time-limit either extra charge required"+", 'Thanks'................")
#                con.execute(ins) 
#                con.commit()

#         except s.Error as e:
#             print(f"Error taking book: {e}")        
            
#     def issuebooks(self):
#       try:
#         k=con.execute('''select book_id from reports where mode="issue"  ''')
#         for j in k:
#             if j[0]=="issue":
#                  print("your book have been successfully issued. ") 
#       except s.Error as e:
#          print(f"Error issuing book: {e}")  

# class Authentication:

#     def add_user(self):
#      try:
#         login_id = input("Enter your login_id: ")
#         password = input("Enter your 8-digit password: ")
        
#         existing_user = con.execute('SELECT login_id FROM authentication WHERE login_id=?', (login_id,)).fetchone()
        
#         if existing_user:
#             print("User already exists. Please log in.")
#             return True
#         else:
#             date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#             con.execute('INSERT INTO authentication (login_id, password, date_time) VALUES (?, ?, ?)', (login_id, password, date_time))
#             con.commit()
#             print("You have successfully registered! Please log in.")
#             return True
#      except s.Error as e:
#             print(f"Error adding user: {e}")
#             return False  
    
#     def login(self):
#       try:
#         login_id = input("Enter your login_id: ")
#         password = input("Enter your 8-digit password: ")
        
#         user = con.execute('SELECT * FROM authentication WHERE login_id=? AND password=?', (login_id, password)).fetchone()
        
#         if user:
#             print("You have successfully logged into the central Library!")
#             return True
#         else:
#             print("Invalid login credentials. Please try again.")
#             return False                                 
#       except s.Error as e:
#             print(f"Error logging in: {e}")
#             return False
                 
       
                       
                 

    
# class Books:
#     def ins_book(self):
#      try:
#         print("Add book data into library:")
#         book_id = int(input("Enter book id: "))
#         book_id1=book_id
#         book_name = input("Enter book name: ")
#         book_name1=book_name
#         book_price = input("Enter book price: ")
#         book_price1=book_price
#         book_edition = input(f"Book {book_id} is which edition: ")
#         book_edition1=book_edition
#         book_category = input("Enter book category: ")
#         book_category1=book_category
#         publisher_name = input("Enter publisher name: ")
#         publisher_name1=publisher_name
#         publ_year = input("Enter year of publication: ")
#         publ_year1=publ_year
        
#         con.execute('''
#             INSERT INTO books (book_id, book_name, book_price, book_edition, book_category, publisher_name, publication_year)
#             VALUES (?, ?, ?, ?, ?, ?, ?)
#         ''', (book_id, book_name, book_price, book_edition, book_category, publisher_name, publ_year))
        
#         con.commit()
#         con.execute('''
#             INSERT INTO books (book_id, book_name, book_price, book_edition, book_category, publisher_name, publication_year)
#             VALUES (?, ?, ?, ?, ?, ?, ?)
#         ''', (book_id1, book_name1, book_price1, book_edition1, book_category1, publisher_name1, publ_year1))
        
#         con.commit()
#      except s.Error as e:
#             print(f"Error adding book: {e}")
#      except ValueError as ve:
#             print(f"Invalid input: {ve}")  
      
# class Reports:
 

#     def take_reports(self):
#      try:
#         print("List of student which take books from the Library.")
#         st_id = int(input("Enter student id: "))
#         name = input("Enter name: ")
#         book_id =int(input("enter book id for take reports: "))
#         mode = input("Enter mode (issue/return/take): ")
#         date = input("Enter date in DD/MM/YYYY: ")

#         con.execute('''
#             INSERT INTO reports (user_id, st_name, book_id, mode, date)
#             VALUES (?, ?, ?, ?, ?)
#         ''', (st_id, name, book_id, mode, date))
#         if mode=="return":
#             k=con.execute("select * from books where book_id={}").format(book_id)
#             for i in k:
#                  ins='''insert into returnbook  (book_id, book_name, book_price, book_edition, book_category, publisher_name, publication_year) values
#                  {},
#                  '''.format(i)
#             con.commit()
#             return True
#      except s.Error as e:
#             print(f"Error adding report: {e}")
#      except ValueError as ve:
#             print(f"Invalid input: {ve}")


#     def give_reports(self):
#       try: 
#        k=con.execute('''select * from reports
# ''')
       
#        for j in k:
#            print(j)
#       except s.Error as e:
#             print(f"Error fetching reports: {e}")

# class staff:
#     def take_staff_data(self):
#       try:
#         print("List of staff that works in the Library.")
#         id=int(input("Enter staff id : "))
#         name=input("Enter staff name : ")
#         name=f"'{name}'" 
#         salary=int(input("Enter current salary of staff : "))
#         ins='''
#         insert into staff (staff_name, staff_id ,staff_salary) values ({},{},{})
#         '''.format(name,id,salary)
#         con.execute(ins)
#         con.commit()
#       except s.Error as e:
#             print(f"Error adding staff data: {e}")
#       except ValueError as ve:
#             print(f"Invalid input: {ve}")      
   
#     def give_staff_data(self):
#      try:
#         k=con.execute("select * from staff ")
#         print("staffs details are below : \n")
#         for j in k:
#             print(j)
#      except s.Error as e:
#             print(f"Error fetching staff data: {e}")

#  # library objects.
# lib=Library() 
# std=Student()
# auth=Authentication()
# bk=Books()
# rp=Reports()
# sf=staff()
# lib.greet()
# n=100
# # working
# for i in range(n):
#       print("==========================================================================================================================================================")
#       print(F"this is your chance: {i+1} login.")
# # use
#       if auth.add_user():
#         print("Please log in now.")
#         if auth.login():
#           a=int(input("Enter[0]:Library manager, Enter[1]:Student , Enter[2]:Staff\nEnter: "))
#           # for library manager
          
#           if a==0:
#               print("======================Welcome Library Manager==========================\n")
#               enter=int(input("Enter[0]:Input-Data , Enter[1]:View data \nEnter: "))
#               if enter == 0:
#                   data_input = int(input("Enter [0]: Input Books Data, [1]: Enter College Student Data\nEnter: "))
            
#                   if data_input == 0:
#                       bk.ins_book()
#                   elif data_input == 1:
#                       std.college_student()
        

#               elif enter==1:
#                   check=int(input("Enter[0]:Display_Books ,Enter[1]:College_student_List , Enter[2]:See Book Report ,Enter[3]:Staff Details. \nEnter: "))
#                   if check==0:
#                       lib.displaybooks()
#                   elif check==1:
#                       lib.collegestudentlist()
#                   elif check==2:
#                       print("Name of students that take benefits from the library . \n")
#                       rp.give_reports()
#                   elif check==3:
#                       sf.give_staff_data()     
#            # for student that wants to take,return,issue books.
#           elif a==1:
#               print("======================Welcome Dear Student==========================\n")
#               enter=int(input("Enter[0]:Take_Book , Enter[1]:Return_Book , Enter[2]:Issue_Book\nEnter: "))
#               if enter==0:
#                   k= True
#                   if k==True:
#                     lib.displaybooks()
#                     rp.take_reports()
#                     std.takebooks()
#                   else:
#                      print("sorry : you can't take books from this Library.you are not from this college !")
           
#               elif enter==1:
#                   k=True
#                   if k==True:
#                      rp.take_reports()
#                      std.return_book()
#                      print("=============Thanks for choosing this Library.===================")
#                   else:
#                       pass  
#               elif enter==2:
#                   k= True
#                   if k==True:
#                      std.issuebooks()
#                      rp.take_reports()
#                   else:
#                       pass
#                   # staff 
#               print("======================Welcome Library staffs [piller of the central Library]==========================\n")     
#           elif a==2:
#               sf.take_staff_data()
#           else:
#               print("invalid User.")
#       else:
#           print("User registration failed.!")
 
# con.close()



