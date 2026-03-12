import streamlit as st
from user_verify import Verify_User as V
from webpage import load_webpage,Cart
from payment import load_payment
from admin import load_admin
import streamlit as st

st.set_page_config(layout="wide")
if "page" not in st.session_state:
    st.session_state.page = "login"
    
if st.session_state.page == "admin":
    load_admin()
elif st.session_state.page == "login":
    st.header("Login")
    V.login()
    if st.button("Sign Up"):
        st.session_state.page="register"
        st.rerun()
elif st.session_state.page=="register":
    st.header("Register")
    V.register()
    if st.button("Login"):
        st.session_state.page="login"
        st.rerun()

elif st.session_state.page=="webpage":
    load_webpage()
elif st.session_state.page=="payment":
    load_payment()
elif st.session_state.page=="cart":
    cart=Cart()
    cart.show_cart()