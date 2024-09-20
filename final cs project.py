import sys
from tabulate import tabulate
import mysql.connector as c
co=c.connect(host='localhost',user='root',password='YA11**sh')
cuo=co.cursor()
cuo.execute('create database if not exists library_mry')
cuo.execute('use library_mry')
Query = ['create table if not exists books (Book_Code varchar(100) primary key , Book_Name varchar(100) , Shelf_No varchar(100) , Genre varchar(1000) , Author_Name varchar(100) , No_Copies int)',
         'create table if not exists issue (Name varchar(100), Reg_No varchar(100) , Book_Code varchar(100) , Issue_Date date )',
         'create table if not exists back (Name varchar(100) , Reg_No varchar(100) , Book_Code varchar(100) , return_Date date)']
cuo.execute(Query[0])
cuo.execute(Query[1])
cuo.execute(Query[2])
def searchC():
    try:
        d=input('Enter the book name you want to search: ')
        data=(d,)
        sql="select book_name,no_copies from books where book_name=(%s)"
        cuo.execute(sql,data)
        q=cuo.fetchall()
        if q==[]:
            sys.stderr.write("===================NO SUCH BOOK EXIST====================\n")
        else:
             for i in q:
                print('BOOK NAME: ',i[0])
                print('NUMBER OF COPIES: ',i[1])
    except:
        sys.stderr.write("=======================INVALID ENTRY======================\n")     
    main()
def searchB():
    try:
        d=input('Enter the book you want to search: ')
        data=(d,)
        sql="select book_name,genre,author_name from books where book_name=(%s)"
        cuo.execute(sql,data)
        q=cuo.fetchall()
        if q==[]:
            sys.stderr.write("===================NO SUCH BOOK EXIST====================\n")
        else:
             print('BOOK_NAME-----GENRE-----AUTHOR_NAME')
             for i in q:
                print(i)
    except:
        sys.stderr.write("===================INVALID ENTRY====================\n")     
    main()
def searchA():
    try:
        d=input('Enter the book author you want to search: ')
        data=(d,)
        sql="select book_name,genre,author_name from books where author_name=(%s)"
        cuo.execute(sql,data)
        q=cuo.fetchall()
        if q==[]:
            sys.stderr.write("===================NO SUCH AUTHOR EXIST====================\n")
        else:
            print('BOOK_NAME-----GENRE-----AUTHOR_NAME')
            for i in q:
                print(i)
            main()
    except:
        sys.stderr.write("===================INVALID ENTRY====================\n")
    main()
def searchG():
    try:
        d=input('Enter the book genre you want to search: ')
        data=(d,)
        sql="select book_name,genre,author_name from books where genre=(%s)"
        cuo.execute(sql,data)
        q=cuo.fetchall()
        if q==[]:
            sys.stderr.write("===================NO SUCH GENRE EXIST====================\n")
        else:
             print('BOOK_NAME-----GENRE-----AUTHOR_NAME')
             for i in q:
                print(i)
    except:
        sys.stderr.write("===================INVALID ENTRY====================\n")     
    main()
def xyz():
    print("""=====================REPORT MENU=====================
                                                        1. ISSUED BOOKS 
                                                        2. RETURNED BOOKS 
                                                        3. GO BACK TO MAIN MENU\n""")
    choice=input("Enter Task No:...")
    if(choice=="1"):
        report_issued_books()
    elif(choice=="2"):
        report_return_books()
    elif(choice=="3"):
        main()
    else:
        sys.stderr.write("====================Please try again====================\n")
        xyz()
def addbook():
    try:
        ge=input('Entre the genre of the book: ')
        bn=input("Enter Book Name: ")
        ba=input("Enter Author's Name: ")
        c=input("Enter Book Code: ")
        sn=input("Enter Shelf No. : ")
        n=int(input('Enter number of copies: '))
        data=(c,bn,sn,ge,ba,n)
        sql='insert into books values(%s,%s,%s,%s,%s,%s);'
        cuo.execute(sql,data)
        co.commit()
        print("Book Added Successfully.......")
        wait = input('Press enter to continue.....')
        main()
    except:
        sys.stderr.write("=====================BOOK CODE ALREADY EXISTS====================\n")
    main()
def issueb():
    try:
        n=input("Enter Student Name: ")
        r=input("Enter Reg No: ")
        c=int(input("Enter Book Code: "))
        d=input("Enter Date (YY/MM/DD): ")
        bata=(c,)
        cuo.execute('select no_copies from books where book_code=(%s)',bata)
        qu=cuo.fetchall()
        if qu[0]<(1,):
            print(qu[0])
            sys.stderr.write("====================INSUFFICIENT BOOKS======================\n")
            main()
        else:
            b='update books set no_copies=no_copies-1 where book_code=(%s)'
            bata=(c,)
            a="insert into issue values(%s,%s,%s,%s);"
            data=(n,r,c,d)
            cuo.execute(a,data)
            cuo.execute(b,bata)
            co.commit()
            dispbook()
            print("Book issued successfully to: ",n)
            wait = input('--------------------Press enter to continue--------------------')
        main()
    except:
        sys.stderr.write("========================BOOK DOESN'T EXISTS==========================\n")
        sys.stderr.write('=========================BOOK IS NOT ISSUED======================\n')
    main()
def returnb():
    try:
        n=input("Enter Student Name: ")
        r=input("Enter Reg No.: ")
        c=int(input("Enter Book Code: "))
        d=input("Enter Date (YY/MM/DD):  ")
        a="insert into back  values(%s,%s,%s,%s);"
        b='update books set no_copies=no_copies+1 where book_code=(%s)'
        bata=(c,)
        data=(n,r,c,d)
        cuo.execute(a,data)
        co.commit()
        cuo.execute(b,bata)
        co.commit()
        print(" Book returned by: ",n)
        wait = input('Press enter to continue.... ')
        main()
    except:
        sys.stderr.write("=================PLEASE ENTER THE CORRECT DATE=====================\n")
        sys.stderr.write('=======================BOOK IS NOT RETURNED======================\n')
    main()    
def dispbook():
    a="select * from books"
    cuo.execute(a)
    myresult=cuo.fetchall()
    if myresult==[]:
        sys.stderr.write('=====================DATABASE IS EMPTY====================\n')
        sys.stderr.write("================ENTER RECORDS IN DATABASE===================\n")
    else:
       print(tabulate(myresult,
               headers=('-----Code-----', '-----Name-----', '-----Shelf-----','-----Genre-----','-----Author_Name-----','-----No_Copies-----'),
                tablefmt='github'))
       wait = input ("--------------------Press enter to continue--------------------")
def report_issued_books():
    a="select * from issue"
    cuo.execute(a)
    myresult=cuo.fetchall()
    if myresult==[]:
        sys.stderr.write('======================DATABASE IS EMPTY====================\n')
        sys.stderr.write("===================ENTER RECORDS IN DATABASE===================\n")
    else:
        print(tabulate(myresult,
                      headers=('-----Name-----', '-----Reg_No-----','----------Book_code----------','-----Issue_Date-----'),
                 tablefmt='tsv'))
    wait = input('--------------------Press enter to continue-------------------------')
    xyz()
def report_return_books():
    a="select * from back"
    cuo.execute(a)
    myresult=cuo.fetchall()
    if myresult==[]:
        sys.stderr.write('=======================DATABASE IS EMPTY====================\n')
        sys.stderr.write("===================ENTER RECORDS IN DATABASE===================\n")
    else:
        print(tabulate(myresult,
                headers=('-----Name-----', '-----Reg_No-----','-----Book_code-----','-----Return_Date-----'),
                   tablefmt='tsv'))
    wait = input ("--------------------Press enter to continue--------------------")
    xyz()
def main():
        print("""----------------------LIBRARY MANAGEMENT APPLICATION----------------------
                                                            1.ADD BOOK 
                                                            2.ISSUE A BOOK 
                                                            3.RETURN A BOOK 
                                                            4.DISPLAY BOOKS 
                                                            5.REPORT MENU
                                                            6.GENRE SEARCH
                                                            7.AUTHOR SEARCH
                                                            7.BOOK SEARCH
                                                            9.NO. OF COPIES
                                                            10.EXIT PROGRAM""")
        choice=input("Enter Task No...... ")
        if(choice=="1"):
            addbook()
        elif(choice== "2"):
            issueb()
        elif(choice=="3"):
            returnb()
        elif(choice=="4"):
            dispbook()
            main()
        elif(choice=="4"):
            dispbook()
        elif(choice=="5"):
            xyz()
        elif(choice=="6"):
            searchG()
        elif(choice=='7'):
            searchA()
        elif(choice=='8'):
            searchB()
        elif(choice=='9'):
            searchC()
        elif(choice=='10'):
            print('------------------------------THANK YOU AND HAVE A GREAT DAY AHEAD-------------------------------\n')
        else:
            sys.stderr.write("---------------------------------PLEASE TRY AGAIN-----------------------------------\n")
            main()
main()
