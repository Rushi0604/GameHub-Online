import supabase_connect as spc
import streamlit as st
from functools import *
import time
import datetime
from fpdf import FPDF
from io import BytesIO
import pandas as pd
from method import Methods
def load_payment():
    Pay=Payment_methods()
    Pay.call_type()
class Payment_methods:
    @st.fragment
    def call_type(self):
        if "email" in st.session_state or "phone" in st.session_state:    
            total=st.session_state.get("total")
            if int(total)==0:
                st.subheader("Your Bill Is 0:")
                Payment_methods.update_purchase_list(st.session_state.cart_list)
                pdf_file = Payment_methods.generate_invoice(" ",[(game.gname, game.gprice) for game in st.session_state.cart_list])
                if st.download_button(
                    label="⬇️ Download Invoice",
                    data=pdf_file,
                    file_name=f"invoice_{st.session_state.email if 'email' in st.session_state else st.session_state.phone}.pdf",
                    mime="application/pdf"):
                    st.rerun()
            else:
                choice=st.radio("Choose payment method:",["Credit Card","Debit Card", "UPI"])
                st.subheader(st.session_state.total)
                if choice=="Credit Card":
                    Payment_methods.credit_card(int(total))
                elif choice=="Debit Card":
                    Payment_methods.debit_card(int(total))
                elif choice=="UPI":
                    Payment_methods.upi(int(total))
            if st.button("Back to Cart"):
                st.session_state.page="webpage"
                st.rerun()

    def credit_card(total):
        name = " "
        st.subheader(f"Total Amount to be Paid: ₹{total}")
        cnum = st.text_input("Enter Credit Card Number")
        st.session_state.payment = False
        
        if cnum:
            if len(cnum) != 16 or not cnum.isdigit():
                st.error("Enter a valid 16-digit card number")
            else:
                if Payment_methods.check_num(cnum):
                    data=spc.supabase.table("details").select("*").eq("c_num", cnum).execute().data
                    if data:
                        exp_month = data[3]
                        exp_year = data[4]
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            user_month = st.number_input("Expiry Month (MM)", min_value=1, max_value=12, step=1)
                        with col2:
                            user_year = st.number_input("Expiry Year (YYYY)", min_value=datetime.datetime.now().year, step=1)
                        
                        cvv = st.number_input("Enter CVV", step=1)
                        
                        if st.button("Confirm Payment"):
                            if cvv != data[5]:
                                st.error("CVV Doesn't Match")
                            elif user_month != exp_month:
                                st.error("Expiration Month does not match")
                            elif user_year != exp_year:
                                st.error("Expiration Year does not match")
                            elif (user_year < datetime.datetime.now().year) or \
                                (user_year == datetime.datetime.now().year and user_month < datetime.datetime.now().month):
                                st.error("Card has expired")
                            elif data[7] < total:
                                st.error("Insufficient Balance")
                            else:
                                Payment_methods.update_balance(total, data[7], cnum, "credit")
                                st.session_state.payment = True
                                st.session_state.payment_method = "Credit Card"
                                name = data[0]
                                st.success("Payment Successful")
                    else:
                        st.error("Credit Card Number Not Found")
                else:
                    st.error("Enter Valid Credit Card Number")
        
        if st.session_state.payment:
            Payment_methods.update_purchase_list(st.session_state.cart_list)
            pdf_file = Payment_methods.generate_invoice(name,[(game.gname, game.gprice) for game in st.session_state.cart_list])
            if st.download_button(
                label="⬇️ Download Invoice",
                data=pdf_file,
                file_name=f"invoice_{st.session_state.email if 'email' in st.session_state else st.session_state.phone}.pdf",
                mime="application/pdf"):
                st.rerun()
            st.session_state.cart_list = []
            st.session_state.page = "webpage"
            Payment_methods.clear_cart()
            Methods.update_user_lists()


    def debit_card(total):
        name = " "
        st.subheader(f"Total Amount to be Paid: ₹{total}")
        
        dnum = st.text_input("Enter Debit Card Number")
        st.session_state.payment = False
        
        if dnum:
            if len(dnum) != 16 or not dnum.isdigit():
                st.error("Enter A Valid 16-Digit Card Number")
            else:
                if Payment_methods.check_num(dnum):
                    data=spc.supabase.table("details").select("*").eq("d_num", dnum).execute().data
                    if data:
                        exp_month = data[3]
                        exp_year = data[4]
                        col1, col2 = st.columns(2)
                        with col1:
                            user_month = st.number_input("Expiry Month (MM)", min_value=1, max_value=12, step=1)
                        with col2:
                            user_year = st.number_input("Expiry Year (YYYY)", min_value=datetime.datetime.now().year, step=1)
                        
                        cvv = st.number_input("Enter CVV", step=1)
                        
                        if st.button("Confirm Payment"):
                            if cvv != data[5]:
                                st.error("CVV Doesn't Match")
                            elif user_month != exp_month:
                                st.error("Expiration Month does not match")
                            elif user_year != exp_year:
                                st.error("Expiration Year does not match")
                            elif (user_year < datetime.datetime.now().year) or \
                                (user_year == datetime.datetime.now().year and user_month < datetime.datetime.now().month):
                                st.error("Card has expired")
                            elif data[7] < total:
                                st.error("Insufficient Balance")
                            else:
                                Payment_methods.update_balance(total, data[7], dnum, "debit")
                                st.session_state.payment = True
                                st.session_state.payment_method = "Debit Card"
                                name = data[0]
                                st.success("Payment Successful")
                    else:
                        st.error("Debit Card Number Not Found")
                else:
                    st.error("Enter Valid Debit Card Number")
        
        if st.session_state.payment:
            Payment_methods.update_purchase_list(st.session_state.cart_list)
            pdf_file = Payment_methods.generate_invoice(name,[(game.gname, game.gprice) for game in st.session_state.cart_list])
            if st.download_button(
                label="⬇️ Download Invoice",
                data=pdf_file,
                file_name=f"invoice_{st.session_state.email if 'email' in st.session_state else st.session_state.phone}.pdf",
                mime="application/pdf"
            ):
                st.session_state.page="webpage"
                st.rerun()
            st.session_state.cart_list = []
            st.session_state.page = "webpage"
            Payment_methods.clear_cart()
            Methods.update_user_lists()

    def check_num(num):
        total=0
        for i in range(16):
            if i%2!=0:
                total+=int(num[i])
            else:
                x=(int(num[i]))*2
                if x>9:
                    total+=x-9
                else:
                    total+=x
        if total%10==0:
            return True
        else:
            return False
        
    def upi(total):
        eupi=st.text_input("Enter UPI ID")
        result=spc.supabase.table("details").select("*").eq("upi_id", eupi).execute().data
        st.session_state.payment=False
        if eupi and len(eupi)>0:
            if result:
                if int(result[7])>total:
                    if st.button("Confirm Payment"):
                        msg=st.empty()
                        msg.success("Payment Successfull")
                        time.sleep(2)
                        msg.empty()
                        Payment_methods.update_balance(total,result[7],eupi,"upi_id")
                        st.session_state.payment=True
                        st.session_state.payment_method = "UPI"
                else:
                    st.error("Insufficient Balance")
            else:
                st.error("UPI ID Not Found")
            if st.session_state.payment==True:
                Payment_methods.update_purchase_list(st.session_state.cart_list)
                pdf_file = Payment_methods.generate_invoice(result[0], [(game.gname,game.gprice) for game in st.session_state.cart_list])
                if st.download_button(label="⬇️ Download Invoice",data=pdf_file,file_name=f"invoice_{st.session_state.email if 'email' in st.session_state else st.session_state.phone}.pdf",mime="application/pdf"):
                    st.rerun()
                st.session_state.cart_list=[]
                st.session_state.page="webpage"
                Payment_methods.clear_cart()
                Methods.update_user_lists()
            
    def clear_cart():
        if "email" in st.session_state:
            spc.supabase.table("user").update({"cart_list": " "}).eq("user_email", st.session_state.email).execute()
        else:
            spc.supabase.table("user").update({"cart_list": " "}).eq("user_phone", st.session_state.phone).execute()

    def update_purchase_list(new_games):
        if "purchase_list" not in st.session_state:
            st.session_state.purchase_list = []

        existing_games = [g.gname for g in st.session_state.purchase_list]

        for game in new_games:
            if game.gname not in existing_games:
                st.session_state.purchase_list.append(game)
        updated_string = ",".join([g.gname for g in st.session_state.purchase_list])

        if "email" in st.session_state:
            spc.supabase.table("user").update({"purchase_list": updated_string}).eq("user_email", st.session_state.email).execute()
        else:
            spc.supabase.table("user").update({"purchase_list": updated_string}).eq("user_phone", st.session_state.phone).execute()

    def update_balance(total,balance,id,payment_type):
        if payment_type == "credit":
            spc.supabase.table("details").update({"balance": balance - total}).eq("c_num", id).execute()
        elif payment_type == "debit":
            spc.supabase.table("details").update({"balance": balance - total}).eq("d_num", id).execute()
        msg=st.empty()
        msg.success("Payment Successfull")
        time.sleep(2)
        msg.empty()

    def generate_invoice(username, games):
        if not games or len(games) == 0:
            st.warning("No purchase found to generate an invoice.")
            return None

        user_email = st.session_state.email if "email" in st.session_state else "N/A"
        total_amount = st.session_state.total if "total" in st.session_state else 0
        payment_method = st.session_state.payment_method if "payment_method" in st.session_state else "Unknown"

        now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        # --- Create PDF ---
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "Game Hub Invoice", ln=True, align="C")

        pdf.set_font("Arial", "", 12)
        pdf.ln(10)
        pdf.cell(0, 10, f"Customer Name: {username}", ln=True)
        pdf.cell(0, 10, f"Customer Email: {user_email}", ln=True)
        pdf.cell(0, 10, f"Date & Time: {now}", ln=True)
        pdf.cell(0, 10, f"Payment Method: {payment_method}", ln=True)
        pdf.ln(10)

        # Table header
        pdf.set_font("Arial", "B", 12)
        pdf.cell(120, 10, "Game Name", 1)
        pdf.cell(60, 10, "Price ()", 1, ln=True)

        # Table rows
        pdf.set_font("Arial", "", 12)
        for game, price in games:
            pdf.cell(120, 10, str(game), 1)
            pdf.cell(60, 10, str(price), 1, ln=True)

        pdf.set_font("Arial", "B", 12)
        pdf.cell(120, 10, "Total", 1)
        pdf.cell(60, 10, f"{total_amount:.2f}", 1, ln=True)

        pdf.ln(10)
        pdf.set_font("Arial", "I", 11)
        pdf.cell(0, 10, "Thank you for your purchase! Enjoy your games!", ln=True, align="C")
        pdf_bytes = pdf.output(dest='S')

        pdf_output = BytesIO(pdf_bytes)

        return pdf_output