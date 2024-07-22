import sqlite3 as s
# # create databse first
con=s.connect("Student_library.db")
# student table
con.execute(
    '''create table student(
    student_id int primary key not null,
    student_reg_no varchar(50),
    first name varchar(50),
    last name varchar(50),
    phone_no int,
    address varchar(50),
    email text 
    
    )
'''
)
# books
con.execute(
    '''
    create table books(
  book_id int primary key not null,  
  book_name varchar(50),
  book_price varchar(50),
  book_edition varchar(50),
  book_category varchar(70),
  publisher_name varchar(70),
  publication_year varchar(50)
)
'''
)
# allbook_before_delete
con.execute(
    '''
    create table returnbook(
  book_id int primary key not null,  
  book_name varchar(50),
  book_price varchar(50),
  book_edition varchar(50),
  book_category varchar(70),
  publisher_name varchar(70),
  publication_year varchar(50)
)
'''
)
# staff
con.execute(

    '''create table staff(
    staff_name varchar(50),
       staff_id int primary  key not null,
       staff_salary int)
'''
)
# Reserve date
con.execute('''
create table reservereturn(
            si_no int primary key not null,
            reserve_date varchar(50),
            return_date varchar(50),
            due_date varchar(50)
)
''')
# Authentication
con.execute('''create table authentication(
    login_id varchar primary key not null,
    password varchar(8) 
            )
'''
)


#  Reports
#  issue or return or take mode

con.execute(
    '''
    create table reports(
user_id int primary key not null,
st_name varchar(50),
book_id int,
reg_no varchar(50), 
mode varchar(50),
date varchar(8)
)

'''
)

con.close()