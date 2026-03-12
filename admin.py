import supabase_connect as spc
import streamlit as st
import datetime
import io
from functools import *
from PIL import Image
from method import Game_Details
def load_admin():
    a=Admin()
    a.admin_menu()
class Games:
    def __init__(self):
        self.games_list=[]
        data=spc.supabase.table("games").select("*").execute().data
        for gno,gtype,gname,gprice,gsize,grate,grelease_date,gdescription,gimage,gdiscount in data:
            self.games_list.append(Game_Details(gno,gtype,gname,gprice,gsize,grate,grelease_date,gdescription,gimage,gdiscount))

class Admin:
    def admin_menu(self):
        st.title("Admin Dashboard")
        g=Games()
        Add,View,Update,Delete=st.tabs(["Add Games","View Games","Update Product", "Delete Product"])
        with Add:
            self.add_product()
        with View:
            self.view_products(g.games_list)
        with Update:
            self.update_product(g.games_list)
        with Delete:
            self.delete_product(g.games_list)

    def add_product(self):
        st.subheader("Add New Product")
        name = st.text_input("Product Name")
        price = st.number_input("Price", min_value=0.0, step=0.01)
        description = st.text_area("Description")
        rate = st.number_input("Rating", min_value=1, max_value=10, step=1)
        gtype = st.text_input("Genre")
        size = st.number_input("Size (GB)", min_value=0.0, step=0.1)
        discount = st.number_input("Discount (%)", min_value=0, max_value=100, step=1)
        image = st.text_input("Upload Product Image")
        if st.button("Add Product"):
            if name and price and description and image and rate and gtype and size is not None and discount is not None:
                spc.supabase.table("games").insert({
                    "gname": name,
                    "gprice": price,
                    "gdescription": description,
                    "grate": rate,
                    "gtype": gtype,
                    "gsize": size,
                    "gdiscount": discount,
                    "gimage": image
                }).execute()
                st.success("Product added successfully!")
                st.rerun()
            else:
                st.warning("Please fill in all fields and upload an image.")
    
    def view_products(self,games_list):
        st.subheader("View Products")
        c=0
        col1,col2=st.columns(2)
        for i in range(len(games_list)):
            target_col=[col1,col2,][c%2]
            with target_col:
                data,photo=st.columns(2)
                with data:
                    st.write("**Name:**", games_list[i].gname)
                    st.write("**Type:**", games_list[i].gtype)
                    st.write("**Price:**", games_list[i].gprice)
                    st.write("**Size:**", games_list[i].gsize)
                    st.write("**Discount:**", games_list[i].gdiscount)
                    st.write("**Release Date:**", games_list[i].grelease_date)
                    st.write("**Description:**", games_list[i].gdescription)
                    st.write("**Rate:**", games_list[i].grate)
                    
                with photo:
                    img=Image.open(io.BytesIO(games_list[i].gimage))    
                    img=img.resize((300, 175))
                    st.image(img)
                st.divider()
                c+=1
    def view_game(game):
        data,photo=st.columns(2)
        with data:
            st.write("**Name:**", game[0].gname)
            st.write("**Type:**", game[0].gtype)
            st.write("**Price:**", game[0].gprice)
            st.write("**Size:**", game[0].gsize)
            st.write("**Discount:**", game[0].gdiscount)
            st.write("**Release Date:**", game[0].grelease_date)
            st.write("**Description:**", game[0].gdescription)
            st.write("**Rate:**", game[0].grate)
        with photo:
            img=Image.open(io.BytesIO(game[0].gimage))    
            img=img.resize((300, 175))
            st.image(img)
        st.divider()

    def update_product(self,games_list):
        st.subheader("Update Product")
        if "edit" not in st.session_state:
            st.session_state.edit=True
        col1,col2,col3=st.columns(3)
        c=0
        for game in games_list:
            with [col1,col2,col3][c%3]:
                id,name=st.columns([0.15,0.85])
                with id:
                    st.write(f"**ID:** {game.gno}")
                with name:
                    st.write(f"**Name:** {game.gname}")
                c+=1
        game_id = st.number_input("Enter Game ID to Update", min_value=1, step=1)
        if st.button("Fetch Game Details"):
            game=[g for g in games_list if g.gno == game_id]
            Admin.view_game(game)
        if st.button("Edit Product"):
            st.session_state.edit=True
        if st.session_state.edit==True:
            data=st.selectbox("Select field to update", options=["g_rate", "g_type", "g_name", "g_price", "g_size", "description", "g_discount","g_image"])
            if data=="g_rate" or data=="_type" or data=="g_name" or data=="g_price" or data=="g_size" or data=="description" or data=="g_discount" :
                new_value=st.text_input("Enter New Value")
                if st.button("Update Product"):
                    spc.supabase.table("games").update({data: new_value}).eq("g_id", game_id).execute()
                    st.success("Product updated successfully!")
                    st.session_state.edit=False
                    st.rerun()
            elif data=="g_image":
                new_image=st.file_uploader("Upload New Product Image", type=["jpg"])
                if st.button("Update Product Image"):
                    spc.supabase.table("games").update({"gimage": new_image.read()}).eq("g_id", game_id).execute()
                    st.success("Product image updated successfully!")
                    st.session_state.edit=False
                    st.rerun()
            elif data!="":
                st.error("Invalid field name. Please enter a valid field to update.")
                st.write("Valid fields are: g_rate, g_type, g_name, g_price, g_size, description, g_discount")

    def delete_product(self,games_list):
        st.subheader("Delete Product")
        col1,col2,col3=st.columns(3)
        c=0
        for game in games_list:
            with [col1,col2,col3][c%3]:
                id,name=st.columns([0.15,0.85])
                with id:
                    st.write(f"**ID:** {game.gno}")
                with name:
                    st.write(f"**Name:** {game.gname}")
                c+=1
        product_id = st.number_input("Enter Product ID to Delete", min_value=1, step=1)
        if st.button("Fetch Product Details"):
            game=[g for g in games_list if g.gno == product_id]
            self.view_game(game)
        if st.button("Delete Product"):
            spc.supabase.table("games").delete().eq("g_id", product_id).execute()
            st.success("Product deleted successfully!")
            st.rerun()