import streamlit as st
import supabase_connect as spc
class Verify_User:
    def login():
        data=st.text_input("Enter Email/Phone Number: ")
        password=st.text_input("Enter Password: ",type="password")
        phone,email=False,False
        if data=="Admin@123" and password=="Admin@123":
            st.success("Admin Login Successful")
            st.session_state.page="admin"
            st.rerun()
        if data.endswith("@gmail.com") or data.endswith("@yahoo.com"):
            user_info=spc.supabase.table("user").select("*").execute().data
            email=True
        else:
            user_info=spc.supabase.table("user").select("*").execute().data
            phone=True
        d,p=0,0
        for i in user_info:
            if data==str(i["user_email"]) or data==str(i["user_phone"]):
                d=1
                if password==i["password"]:
                    p=1
                    if st.button("Login"):
                        st.success("Login Successfull")
                        if email:
                            st.session_state.email=data
                            if data[1]!=0:
                                st.session_state.phone=i["user_phone"]
                        if phone:
                            st.session_state.phone=data
                            if data[0]!=" ":
                                st.session_state.email=i["user_email"]
                        st.session_state.password=password
                        st.session_state.page="webpage"
                        st.rerun()
        if data and password:
            if d==0:
                st.error("Invalid Email/Phone Number")
            if p==0:
                st.error("Invalid Password")

    def register():
        data=st.text_input("Enter Email/Phone Number: ")
        password=st.text_input("Enter Password: ",type="password")
        user_info = spc.supabase.table("user").select("*").execute().data
        for i in user_info:
            if i["user_email"]==data or i["user_phone"]==data:
                st.error("User All Ready Exists")
                if st.button("Go To Login"):
                    st.session_state.page="login"
        if data.endswith("@gmail.com") or data.endswith("@yahoo.com"):
            if password and data:
                if Verify_User.verify_password(password):
                    spc.supabase.table("user").insert({"user_email":data,"user_phone":" ","password":password}).execute()
                    if st.button("Register"):
                        st.success("Registration Successful")    
                        st.session_state.email=data
                        st.session_state.password=password
                        st.session_state.page="webpage"
                        st.rerun()
                elif password!="":
                    st.error("Password must be at least 8 characters long and contain at least one special character (@#!?$&)xxxxx")
        else:
            if data.isdigit() and len(data)==10:
                if Verify_User.verify_password(password):
                    spc.supabase.table("user").insert({"user_email":" ","user_phone":data,"password":password}).execute()
                    if st.button("Register"):
                        st.success("Registration Successful")
                        st.session_state.email=data
                        st.session_state.password=password
                        st.session_state.page="webpage"
                        st.rerun()
                elif password!="":
                    st.error("Password must be at least 8 characters long and contain at least one special character (@#!?$&)")
            elif data!="":
                st.error("Invalid Phone Number")

    def verify_password(password):
        s,d=0,0
        for i in password:
            if i in "@#!?$&":
                s+=1
            elif i.isdigit():
                d+=1
        if s>0 and d>0 and len(password)>8:
            return True