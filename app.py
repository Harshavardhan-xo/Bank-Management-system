import streamlit as st
import mysql.connector
from streamlit_option_menu import option_menu
from datetime import date
import pandas as pd

st.title("Bank")

# mysql connector
con = mysql.connector.connect(host = "localhost",user = "root", password = "1721", database = "bank")
res = con.cursor()


def register(data):
    qry = """insert into details(first_name,last_name,father_or_gardien,phone_number,date_of_birth,age,
        occupation,account_type,aadhar,pan,password_,deposite_amt,balance,address) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    res.execute(qry,data)
    con.commit()      

#function to view        
def view_passbook(phone_number):
    qry = "select account_number,concat(first_name,' ',last_name),deposite_amt,withdarwal_amt,balance from details where phone_number=%s"
    res.execute(qry,(phone_number,))
    data =  res.fetchall()
    table_ = pd.DataFrame(data,columns=["Account No","Name","Credit","Debit","Balance"])
    return st.table(table_)

#function to update
def update(data,Account_no):
    qry = "update details set first_name=%s, last_name=%s, phone_number=%s, occupation=%s, account_type=%s, password_=%s where account_number=%s"
    res.execute(qry, (*data,Account_no))
    con.commit()

        

#function to deposite
def deposite(data,password):
    qry = "update details set deposite_amt=%s,balance=%s where password_=%s"
    res.execute(qry, (*data,password))
    con.commit()

#function to withdarwal
def withdarwal(data,password):
    qry = "update details set withdarwal_amt=%s,balance=%s where password_=%s"
    res.execute(qry, (*data,password))
    con.commit()
    
#function to delete account
def delete_account(Phone_number):
    qry = "delete from details where phone_number=%s"
    res.execute(qry, (Phone_number,))
    con.commit()
    
# function to get phone_number, password, balance and Details
def phone_no():
    phone_no_lst=[]
    Phone_no_qry="select phone_number from details"
    res.execute(Phone_no_qry)
    data1=res.fetchall()
    for i in data1:     
        phone_no_lst.append(i[0])
    return phone_no_lst   

def pas():
    pas=[]
    qry="select password_ from details"
    res.execute(qry)
    data1=res.fetchall()
    for i in data1:
        pas.append(i[0])
    return pas

def bal(password):
    qry="select balance from details where password_=%s"
    res.execute(qry,(password,))
    data1=res.fetchone()
    if data1 is None:
        return 0
    return int(data1[0])

def get_details(old_no):
    qry = "select account_number,first_name,last_name,phone_number,occupation,account_type,password_ from details where phone_number=%s"
    res.execute(qry,(old_no,))
    data =  res.fetchall()
    table_ = pd.DataFrame(data,columns=["Account no","First name","last name","Phone number","occupation","account type","password"])
    return st.table(table_)

# Whole code for the bank app

menu = option_menu(
        menu_title="Navigation",
        options=["registeration","login"],
        icons=["person-plus","eye"],
        menu_icon="bank",
        default_index=0,
        orientation="horizontal"
        )

# st.image("side_bar.jpg")
st.sidebar.title("Core Bank")
    
    
if menu == "registeration":
    
    st.subheader("Add person")
    
    col0,col1, col2 = st.columns(3)
    col3, col4 ,col5 = st.columns(3) 
    col6, col7 = st.columns(2) 
    col8, col9, col10 = st.columns(3)
    col11, col12, col13 = st.columns(3)
    col0.image("image/reg.jpg",width=200)
    first_name = col1.text_input("First Name",placeholder="Enter Your First Name").capitalize()
    last_name = col2.text_input("Last Name",placeholder="Enter Your Last Name").capitalize()
    phone_number = col3.text_input("Mobile no",max_chars=10,placeholder="Enter Your Mobile Number")
    date_of_birth = col4.date_input("DOB",date(1999,12,31))
    age = col5.number_input("AGE",min_value=18,max_value=60)
    father_or_gardien = col8.text_input("Father / Gardien",placeholder="Enter father / Gardien Name").capitalize()
    aadhar = col6.text_input("Aadhar Number",max_chars=18,placeholder="Enter Your Aadhar Number")
    pan = col7.text_input("PAN",max_chars=10,placeholder="Enter Your PAN Number").upper()
    occupation = col9.radio("Occupation",["Self Employed","Salaried"])
    account_type = col10.radio("Account Type",["Savings A/C","Current A/C"])
    deposite_amt = col11.number_input("Deposite Amount",min_value=500,step=100,placeholder="Enter the Amount")
    password_ = col12.text_input("Password",type="password")
    re = col13.text_input("Re enter password",type="password")
    address = st.text_input("Address",placeholder="Enter your current Address").title()
    balance = deposite_amt
    
    if password_ == re:
        pass   
        
    else:
        st.error("Plese Check The Password")
            
    if st.button("Add"):
            register((first_name,last_name,father_or_gardien,phone_number,date_of_birth,age,occupation,account_type,aadhar,pan,password_,deposite_amt,balance,address))
            st.success("Registered successfully")
# condition for login

elif menu == "login":
    st.image("image/Login.jpg")
    if "login_" not in st.session_state:
        st.session_state.login_ = False
    
    m_n = st.text_input("Mobile no",max_chars=10,placeholder="Ente the Registered Mobile NO")
    pass2= st. text_input("Password",type="password",placeholder="Enter the password")
    
        
    if st.button("login"):
        if m_n in phone_no() and pass2 in pas():
            
            st.success("Successfully logined")
            st.session_state.m_n = m_n
            st.session_state.pass2 = pass2
            st.session_state.login_ = True
            
        else:
            st.warning("wrong Number or Password")
            
    if st.session_state.login_:
        
        with st.sidebar:
            login_ = option_menu (None,
            options=["view A/C details","A/C Update","Deposite","Withdarwal","A/C Close"],
            icons=["eye","pencil-square","piggy-bank","cash-coin","journal-x"],
            menu_icon="bank",
            default_index=0, 
        )
            
        if login_ == "view A/C details":
            st.subheader("Pass Book")
            view_passbook(m_n)
                    

        elif login_ == "A/C Update":

            get_details(m_n)

            col1, col2, col3 = st.columns(3)
            col4, col5, col6 = st.columns(3)

            ac_no = st.text_input("Account no",placeholder="enter the account number shown above")
            first_name = col1.text_input("First Name",key="ufirst").capitalize()
            last_name = col2.text_input("Last Name",key="ulast").capitalize()
            phone_number = col3.text_input("New no",max_chars=10,key="uphone")
            occupation = col4.radio("Occupation",["Self Employed","Salaried"])
            account_type = col5.radio("Account Type",["Savings A/C","Current A/C"])
            password_ = col6.text_input("New Password",type="password",key="upass")

            if st.button("Update"):
                update((first_name, last_name, phone_number, occupation, account_type, password_),ac_no)
                st.success("Update successfully")

        elif login_ == "Deposite":

            debit = int(st.number_input("Depostie",step=100,placeholder="Enter The Deposite Amount"))
            password = st.text_input("Password",type="password",placeholder="Enter The Password")
            current_balance = bal(password)
            bal1 = current_balance + debit
            if st.button("Done"):
                if password in pas():
                    deposite((debit,bal1),password)
                    st.success("The Amount Deposited Sucessfully")
                else:
                    st.warning("Check the password")
                    
                    
        elif login_ == "Withdarwal":
            
            Withdarwal_ = st.number_input("Withdarwal",step=100,placeholder="Enter The Withdarwal Amount")
            password = st.text_input("Password",type="password",placeholder="Enter The Password")
            c_b1 = bal(password) 
            bal2 = c_b1 - Withdarwal_
            if st.button("Done"):
                if password in pas():
                    withdarwal((Withdarwal_,bal2),password)
                    st.success("The Amount Credited sucessfully")
                else:
                    st.warning("Check the password")
                    

        else:
            mobile_no = st.text_input("Mobile No", max_chars=10)
            passw = st.text_input("Password", type="password")

            if st.button("Done"):
                if mobile_no in phone_no() and passw in pas():
                    st.session_state.confirm_close = True
                else:
                    st.warning("Invalid mobile number or password")

            if st.session_state.get("confirm_close", False):
                st.warning("Are you sure you want to close your account?")
                passw1 = st.text_input("Re-enter Password", type="password")

                if st.button("Submit"):
                    if passw1 in pas():
                        delete_account(mobile_no)
                        st.success("Your account was closed successfully")
                        st.session_state.confirm_close = False
                    else:

                        st.warning("Password mismatch")
