import supabase_connect as spc
import streamlit as st
import datetime
import random
import io
import requests
from functools import *
from PIL import Image
import time
st.set_page_config(layout="wide")
class Game_Details:
    def __init__(self, gno, gtype, gname, gprice, gsize, grate, grelease_date, gdescription, gimage, gdiscount):
        self.gno = gno
        self.gtype = gtype
        self.gname = gname
        self.gprice = gprice
        self.gsize = gsize
        self.grate = grate
        self.grelease_date = grelease_date
        self.gdescription = gdescription
        self.gimage = gimage
        self.gdiscount = gdiscount

class Methods:
    def get_random(games_list):
        if 'random' not in st.session_state:
            st.session_state.random=random.sample(range(len(games_list)), 15)
        x=st.session_state.get('random', [])
        return x
    def recomanded(games_list):
        col1, col2, col3 = st.columns(3)
        x=Methods.get_random(games_list)
        c=0
        for i in x:
            game=games_list[i]
            target_col=[col1, col2, col3][c % 3]
            c+=1
            with target_col:
                st.write("**Name:**",game.gname)
                response = requests.get(game.gimage)
                img = Image.open(io.BytesIO(response.content))
                img = img.resize((300, 200))
                st.image(img)
                if st.button("Show Details", key=f"{game.gname}_show"):
                    st.session_state.selected_game =game.gname
                if st.session_state.get("selected_game") ==game.gname:
                    Methods.display_details(game)                
                st.divider()
    def display_details(game):
        cart=Cart()
        wishlist=Wishlist()
        st.write("**Name:**",game.gname)
        st.write("**Type:**",game.gtype)
        if game.gprice==0:
            st.write("**Price:** Free")
        else:
            st.write("**Price:**",game.gprice)
        st.write("**Size:**",game.gsize)
        st.write("**Discount:**",game.gdiscount)
        st.write("**Description:**",game.gdescription)
        st.write("**Rating:**",game.grate)
        with st.container(horizontal=True):
            if st.button("Add To Cart", key=f"{game.gname}_display_cart"):
                cart.add_game(game)
            if st.button("Add To Wishlist", key=f"{game.gname}_display_wishlist"):
                wishlist.add_game(game)
    def browes(games_list):
        with st.container(horizontal=True):
            response = requests.get("https://djsrwvtvtkoctdywccxw.supabase.co/storage/v1/object/public/Games_image/newgames.jpg")
            img = Image.open(io.BytesIO(response.content))
            img = img.resize((800,110))
            st.image(img)
            if st.button("New Games"):
                st.session_state.newgames=True
                st.session_state.discount=False
        if "newgames" in st.session_state:
            if st.session_state.newgames:
                Methods.newgames(games_list)
        with st.container(horizontal=True):
            response = requests.get("https://djsrwvtvtkoctdywccxw.supabase.co/storage/v1/object/public/Games_image/discount.jpg")
            img = Image.open(io.BytesIO(response.content))
            img=img.resize((800,110))
            st.image(img)
            if st.button("Discount"):
                st.session_state.discount=True
                st.session_state.newgames=False
        if "discount" in st.session_state:
            if st.session_state.discount:
                    Methods.discount(games_list)
    def newgames(games_list):
        today = datetime.datetime.now().date()
        cart=Cart()
        wishlist=Wishlist()
        for i in range(len(games_list)):
            date_str=games_list[i].grelease_date
            date_obj=datetime.datetime.strptime(str(date_str), "%Y-%m-%d").date()
            difference=today - date_obj
            if difference.days <= 1095 and games_list[i].gprice!=0:
                data, photo = st.columns(2)
                with data:
                    st.write("**Name:**",games_list[i].gname)
                    st.write("**Type:**",games_list[i].gtype)
                    if games_list[i].gprice==0:
                        st.write("**Price:** Free")
                    else:
                        st.write("**Price:**",games_list[i].gprice)
                    st.write("**Size:**",games_list[i].gsize)
                    st.write("**Description:**",games_list[i].gdescription)
                    st.write("**Rate:**",games_list[i].grate)
                    with st.container(horizontal=True):
                        if st.button("Add To Cart", key=f"{games_list[i].gname}_newgame_cart"):
                            cart.add_game(games_list[i])
                        if st.button("Add To Wishlist", key=f"{games_list[i].gname}_newgame_wishlist"):
                            wishlist.add_game(games_list[i])
                with photo:
                    st.image(games_list[i].gimage,width=460)
                st.divider()
    def discount(games_list):
        cart=Cart()
        wishlist=Wishlist()
        for i in range(len(games_list)):
            if games_list[i].gdiscount!=0 and games_list[i].gprice!=0:
                data,photo=st.columns(2)
                with data:
                    st.write("**Name:**",games_list[i].gname)
                    st.write("**Type:**",games_list[i].gtype)
                    if games_list[i].gprice==0:
                        st.write("**Price:** Free")
                    else:
                        st.write("**Price:**",games_list[i].gprice)
                    st.write("**Discount:**",games_list[i].gdiscount)
                    st.write("**Description:**",games_list[i].gdescription)
                    st.write("**Size:**",games_list[i].gsize)
                    st.write("**Rate:**",games_list[i].grate)
                    with st.container(horizontal=True):
                        if st.button("Add To Cart", key=f"{games_list[i].gname}_discount_cart"):
                            cart.add_game(games_list[i])
                        if st.button("Add To Wishlist", key=f"{games_list[i].gname}_discount_wishlist"):
                            wishlist.add_game(games_list[i])
                with photo:
                    st.image(games_list[i].gimage,width=460)
                st.divider()
    def category(games_list):
        st.header("**Choose Category**")
        choice=st.radio("",["Action","Adventure","Racing","Simulator","Sports"],horizontal=True)
        if choice=="Action":
            st.header("**Action**")
            st.divider()
            Methods.cat_display(choice,games_list)
        elif choice=="Adventure":
            st.header("**Adventure**")
            st.divider()
            Methods.cat_display(choice,games_list)
        elif choice=="Racing":
            st.header("**Racing**")
            st.divider()
            Methods.cat_display(choice,games_list)
        elif choice=="Simulator":
            st.header("**Simulator**")
            st.divider()
            Methods.cat_display(choice,games_list)
        elif choice=="Sports":
            st.divider()
            Methods.cat_display(choice,games_list)
    def cat_display(typee,games_list):
        cat=[game for game in games_list if game.gtype == typee]
        c=0
        cart=Cart()
        wishlist=Wishlist()
        col1,col2=st.columns(2)
        for i in range(len(cat)):
            target_col=[col1,col2,][c%2]
            with target_col:
                data,photo=st.columns(2)
                with data:
                    st.write("**Name:**", cat[i].gname)
                    if cat[i].gprice==0:
                        st.write("**Price:** Free")
                    else:
                        st.write("**Price:**", cat[i].gprice)
                    st.write("**Size:**", cat[i].gsize)
                    st.write("**Description:**", cat[i].gdescription)
                    st.write("**Rate:**", cat[i].grate)

                with photo:
                    response = requests.get(cat[i].gimage)
                    img = Image.open(io.BytesIO(response.content))
                    img = img.resize((300, 175))
                    st.image(img)
                    with st.container(horizontal=True):
                        if st.button("Add To Cart", key=f"{cat[i].gname}_catagory_cart"):
                            cart.add_game(cat[i])
                        if st.button("Add To Wishlist", key=f"{cat[i].gname}_catagory_wishlist"):
                            wishlist.add_game(cat[i])
                st.divider()
                c+=1
    def free_games(games_list):
        st.header("Free Games:")
        st.divider()
        free=[game for game in games_list if game.gprice == 0]
        c=0
        cart=Cart()
        wishlist=Wishlist()
        col1,col2=st.columns(2)
        for i in range(len(free)):
            target_col=[col1,col2,][c%2]
            with target_col:
                data,photo=st.columns(2)
                with data:
                    st.write("**Name:**", free[i].gname)
                    st.write("**Type:**", free[i].gtype)
                    st.write("**Size:**", free[i].gsize,"GB")
                    st.write("**Description:**", free[i].gdescription)
                    st.write("**Rate:**", free[i].grate)

                with photo:
                    response = requests.get(free[i].gimage)
                    img = Image.open(io.BytesIO(response.content))
                    img = img.resize((300, 175))
                    st.image(img)
                    with st.container(horizontal=True):
                        if st.button("Add To Cart", key=f"{games_list[i].gname}_free_cart"):
                            cart.add_game(games_list[i])
                        if st.button("Add To Wishlist", key=f"{games_list[i].gname}_free_wishlist"):
                            wishlist.add_game(games_list[i])
                st.divider()
                c+=1
    def sort(games_list):
        st.header("**Choose Sorting Type**")
        choice=st.radio("",["Price","Rating","Size","Discount"],horizontal=True)
        if choice=="Price":
            st.header("**Sort By Price**")
            type=st.radio("Choose Order:",["Low To High","High To Low"],horizontal=True)
            glist=games_list
            if type=="Low To High":
                glist.sort(key=lambda Game_Details: Game_Details.gprice)
            elif type=="High To Low":
                glist.sort(key=lambda Game_Details: Game_Details.gprice, reverse=True)
            st.divider()
            Methods.sort_display("gprice",glist)
        elif choice=="Rating":
            st.header("**Sort By Rating**")
            st.divider()
            glist=games_list
            glist.sort(key=lambda Game_Details: Game_Details.grate, reverse=True)
            Methods.sort_display("grate",games_list)
        elif choice=="Size":
            st.header("**Sort By Size**")
            st.divider()
            type=st.radio("Choose Order:",["Low To High","High To Low"],horizontal=True)
            glist=games_list
            if type=="Low To High":
                glist.sort(key=lambda Game_Details: Game_Details.gsize)
            elif type=="High To Low":
                glist.sort(key=lambda Game_Details: Game_Details.gsize, reverse=True)
            Methods.sort_display("gsize",games_list)
        elif choice=="Discount":
            st.header("**Sort By Discount**")
            st.divider()
            glist=games_list
            glist.sort(key=lambda Game_Details: Game_Details.gdiscount, reverse=True)
            Methods.sort_display("gdiscount",games_list)
    def sort_display(choice,games_list):
        c=0
        cart=Cart()
        wishlist=Wishlist()
        col1,col2=st.columns(2)
        for glist in games_list:
            if glist.gprice!=0:
                target_col=[col1,col2,][c%2]
                with target_col:
                        data,photo=st.columns(2)
                        with data:
                            st.write("**Name:**", glist.gname)
                            if glist.gprice==0:
                                st.write("**Price:** Free")
                            else:
                                st.write("**Price:**",glist.gprice)
                            st.write("**Size:**", glist.gsize,"GB")
                            st.write("**Description:**", glist.gdescription)
                            st.write("**Rate:**", glist.grate)

                        with photo:
                            response = requests.get(glist.gimage)
                            img = Image.open(io.BytesIO(response.content))
                            img = img.resize((300, 175))
                            st.image(img)
                            with st.container(horizontal=True):
                                if st.button("Add To Cart", key=f"{glist.gname}_sort_cart"):
                                    cart.add_game(glist)
                                if st.button("Add To Wishlist", key=f"{glist.gname}_sort_wishlist"):
                                    wishlist.add_game(glist)
                        st.divider()
                        c+=1
    def library():
        if "email" in st.session_state:
            result = spc.supabase.table("user").select("purchase_list").eq("user_email", st.session_state.email).execute().data
        else:
            result = spc.supabase.table("user").select("purchase_list").eq("user_phone", st.session_state.phone).execute().data

        if not result or not result[0]:
            st.info("No Purchases Found Yet.")
            return

        # Convert string → list of game names
        raw_string = str(result[0]["purchase_list"]).strip()
        purchases = [g.strip() for g in raw_string.split(",") if g.strip()]

        # --- Supabase query instead of MySQL ---
        games_data = spc.supabase.table("games").select("*").in_("g_name", purchases).execute().data

        st.header("🎮 Your Purchased Games")

        col1, col2 = st.columns(2)
        c = 0

        for item in games_data:
            target_col = [col1, col2][c % 2]

            with target_col:
                data, photo = st.columns(2)

                with data:
                    st.write("**Name:**", item["g_name"])
                    st.write("**Type:**", item["g_type"])

                    if item["g_price"] == 0:
                        st.write("**Price:** Free")
                    else:
                        st.write("**Price:**", item["g_price"])

                    st.write("**Size:**", item["g_size"], "GB")
                    st.write("**Rating:**", item["g_rate"])

                with photo:
                    st.image(item["g_image"], width=300)

                st.divider()

            c += 1

    def account():
        st.header("Account Details")

        email = st.session_state.get("email")
        phone = st.session_state.get("phone")

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Email:**", email if email else "Not set")

        with col2:
            st.write("**Phone:**", phone if phone else "Not set")

        st.session_state.reset_password = False
        st.session_state.add_phone = False
        st.session_state.add_email = False

        if email and not phone:
            if st.button("Add Mobile Number", key="add_phone_btn"):
                st.session_state.add_phone = True

            if st.session_state.add_phone:
                phone_input = st.text_input("Enter 10-digit Phone Number:")

                if st.button("Save Phone", key="save_phone_btn"):

                    if phone_input.isdigit() and len(phone_input) == 10:

                        spc.supabase.table("user").update({"user_phone": phone_input}).eq("user_email", email).execute()
                        st.session_state.phone = phone_input
                        st.session_state.add_phone = False
                        st.success("Phone number added!")
                        st.rerun()

                    else:
                        st.error("Invalid phone number. Must be 10 digits.")

        if phone and not email:
            if st.button("Add Email", key="add_email_btn"):
                st.session_state.add_email = True

            if st.session_state.add_email:
                email_input = st.text_input("Enter Email:")

                if st.button("Save Email", key="save_email_btn"):

                    if email_input.endswith(("@gmail.com", "@yahoo.com")):

                        spc.supabase.table("user").update({"user_email": email_input}).eq("user_phone", phone).execute()
                        st.session_state.email = email_input
                        st.session_state.add_email = False
                        st.success("Email added!")
                        st.rerun()

                    else:
                        st.error("Invalid email. Must be from gmail.com or yahoo.com.")

        if st.button("Reset Password", key="reset_pw_toggle"):
            st.session_state.reset_password = True

        if st.session_state.reset_password:

            old_pw = st.session_state.password
            new_pw = st.text_input("Enter New Password: ", type="password")
            confirm_pw = st.text_input("Confirm New Password: ", type="password")

            if st.button("Update Password", key="update_pw_btn"):

                if old_pw != st.session_state.get("password"):
                    st.error("Old password is incorrect.")

                elif new_pw != confirm_pw:
                    st.error("New passwords do not match.")

                elif len(new_pw) < 8:
                    st.error("Password must be at least 8 characters.")

                else:

                    s, d = 0, 0

                    for i in new_pw:
                        if i in "@#!?$&":
                            s = 1
                        elif i.isdigit():
                            d = 1

                    if d == 0 or s == 0:
                        st.error("Password must contain at least one digit and one special character (@#$&?).")

                    else:

                        if email:
                            spc.supabase.table("user").update({"password": new_pw}).eq("user_email", email).execute()
                        else:
                            spc.supabase.table("user").update({"password": new_pw}).eq("user_phone", phone).execute()

                        st.success("Password updated successfully!")
                        st.session_state.password = new_pw
                        st.session_state.reset_password = False
                        st.rerun()

        if st.button("Logout", key="logout_btn"):
            Methods.update_user_lists()
            st.session_state.clear()
            st.session_state.page = "login"
            st.rerun()

            
    def list_set(list_type):
        if f"{list_type}_games" in st.session_state:
            return st.session_state[f"{list_type}_games"]

        if "cart_list" not in st.session_state:
            st.session_state.cart_list = []
        if "purchase_list" not in st.session_state:
            st.session_state.purchase_list = []
        if "wish_list" not in st.session_state:
            st.session_state.wish_list = []

        if "email" in st.session_state:
            result = spc.supabase.table("user").select(list_type).eq("user_email", st.session_state.email).execute().data
        else:
            result = spc.supabase.table("user").select(list_type).eq("user_phone", st.session_state.phone).execute().data

        if not result or not result[0]:
            return []

        raw_string = str(result[0][list_type]).strip()
        purchases = [g.strip() for g in raw_string.split(",") if g.strip()]

        if not purchases:
            return []

        games_data = spc.supabase.table("games").select("*").in_("g_name", purchases).execute().data

        games = []

        for item in games_data:
            games.append(
                Game_Details(
                    item["g_id"],
                    item["g_type"],
                    item["g_name"],
                    item["g_price"],
                    item["g_size"],
                    item["g_rate"],
                    item["g_date"],
                    item["g_description"],
                    item["g_image"],
                    item["g_discount"]
                )
            )
            return games
        

    def update_user_lists():

        cart_str = ",".join([g.gname for g in st.session_state.get("cart_list", [])])
        wish_str = ",".join([g.gname for g in st.session_state.get("wish_list", [])])
        purchase_str = ",".join([g.gname for g in st.session_state.get("purchase_list", [])])

        # --- Supabase UPDATE instead of MySQL ---
        if "email" in st.session_state:

            spc.supabase.table("user").update({
                "cart_list": cart_str,
                "wish_list": wish_str,
                "purchase_list": purchase_str
            }).eq("user_email", st.session_state.email).execute()

        else:

            spc.supabase.table("user").update({
                "cart_list": cart_str,
                "wish_list": wish_str,
                "purchase_list": purchase_str
            }).eq("user_phone", st.session_state.phone).execute()

        print("User lists synced to database.")
        
class Cart:
    def __init__(self):
        if "cart_list" not in st.session_state:
            st.session_state.cart_list = []
            st.session_state.cart_names = set()

        if "purchase_list" not in st.session_state:
            st.session_state.purchase_list = Methods.list_set("purchase_list") or []
        st.session_state.purchase_names = {g.gname for g in st.session_state.purchase_list}

        if "cart_loaded" not in st.session_state:
            db_cart = Methods.list_set("cart_list") or []
            if db_cart:
                st.session_state.cart_list = db_cart
                st.session_state.cart_names = {g.gname for g in db_cart}
            st.session_state.cart_loaded = True

    def add_game(self, game):
        if game.gname in st.session_state.purchase_names:
            msg=st.empty()
            msg.warning(f"⚠️ {game.gname} already purchased!")
            time.sleep(2)
            msg.empty()
            return

        if game.gname in st.session_state.cart_names:
            msg=st.empty()
            msg.info(f"⚠️ {game.gname} already in cart!")
            time.sleep(2)
            msg.empty()
            return

        st.session_state.cart_list.append(game)
        st.session_state.cart_names.add(game.gname)
        msg=st.empty()
        msg.success(f"✅ {game.gname} added to cart!")
        time.sleep(2)
        msg.empty()

        if "wish_list" in st.session_state:
            for w_game in st.session_state.wish_list[:]:
                if w_game.gname == game.gname:
                    st.session_state.wish_list.remove(w_game)
                    st.session_state.wish_names.remove(game.gname)  

        Methods.update_user_lists()
        time.sleep(1)
        st.rerun()

    def show_cart(self):
        Methods.update_user_lists()
        st.header("🛒 Your Shopping Cart")
        items = st.session_state.get("cart_list", [])
        st.subheader(f"Games in Cart: {len(items)}")

        if not items:
            st.info("Your cart is empty.")
            return

        total = sum(g.gprice - (g.gprice * g.gdiscount / 100) for g in items)
        st.session_state.total = total
        st.subheader(f"💰 Total: ₹{total:.2f}")
        st.divider()

        col1, col2 = st.columns(2)
        for idx, game in enumerate(items):
            target = [col1, col2][idx % 2]
            with target:
                data, photo = st.columns(2)
                with data:
                    st.write("**Name:**", game.gname)
                    st.write("**Type:**", game.gtype)
                    if game.gprice == 0:
                        st.write("**Price:** Free")
                    else:
                        st.write("**Price:** ₹", game.gprice)
                    st.write("**Discount:**", game.gdiscount, "%")
                    if st.button("Remove", key=f"{game.gname}_remove"):
                        st.session_state.cart_list.remove(game)
                        st.session_state.cart_names.remove(game.gname)
                        Methods.update_user_lists()
                        st.rerun()
                with photo:
                    response = requests.get(game.gimage)
                    img = Image.open(io.BytesIO(response.content))
                    img = img.resize((300, 175))
                    st.image(img)
                st.divider()

        with st.container(horizontal=True):
            if st.button("Buy Games"):
                st.session_state.page = "payment"
                st.session_state.cart_items = items
                st.rerun()
            if st.button("Clear Cart"):
                st.session_state.cart_list = []
                st.session_state.cart_names = set()
                Methods.update_user_lists()
                st.rerun()


class Wishlist:
    def __init__(self):
        if "wish_list" not in st.session_state:
            st.session_state.wish_list = []
        if "wish_names" not in st.session_state:
            st.session_state.wish_names = set()

        if "purchase_list" not in st.session_state:
            st.session_state.purchase_list = Methods.list_set("purchase_list") or []
        st.session_state.purchase_names = {g.gname for g in st.session_state.purchase_list}

        if "cart_list" not in st.session_state:
            st.session_state.cart_list = Methods.list_set("cart_list") or []    
        st.session_state.cart_names = {g.gname for g in st.session_state.cart_list}

        if "wishlist_loaded" not in st.session_state:
            db_wish = Methods.list_set("wish_list") or []
            if db_wish:
                st.session_state.wish_list = db_wish
                st.session_state.wish_names = {g.gname for g in db_wish}
            st.session_state.wishlist_loaded = True

    def add_game(self, game):
        if game.gname in st.session_state.purchase_names:
            msg=st.empty()
            msg.warning(f"⚠️ {game.gname} already purchased!")
            time.sleep(2)
            msg.empty()
            return

        if game.gname in st.session_state.wish_names:
            msg=st.empty()
            msg.info(f"⚠️ {game.gname} already in wishlist!")
            time.sleep(2)
            msg.empty()
            return

        if game.gname in st.session_state.cart_names:
            msg=st.empty()
            msg.info(f"⚠️ {game.gname} already in cart!")
            time.sleep(2)
            msg.empty()
            return

        st.session_state.wish_list.append(game)
        st.session_state.wish_names.add(game.gname)
        msg=st.empty()
        msg.success(f"✅ {game.gname} added to wishlist!")
        time.sleep(2)
        msg.empty()
        Methods.update_user_lists()
        time.sleep(1)
        st.rerun()

    def show_wishlist(self):
        Methods.update_user_lists()
        st.header("Your Wishlist")
        items = st.session_state.get("wish_list", [])
        st.subheader(f"Games in Wishlist: {len(items)}")
        st.divider()

        if not items:
            st.info("Your wishlist is empty.")
            return

        col1, col2 = st.columns(2)
        for idx, game in enumerate(items):
            target = [col1, col2][idx % 2]
            with target:
                data, photo = st.columns(2)
                with data:
                    st.write("**Name:**", game.gname)
                    st.write("**Type:**", game.gtype)
                    if game.gprice == 0:
                        st.write("**Price:** Free")
                    else:
                        st.write("**Price:** ₹", game.gprice)
                    st.write("**Discount:**", game.gdiscount, "%")
                    with st.container(horizontal=True):
                        if st.button("Remove", key=f"{game.gname}_wish_remove"):
                            st.session_state.wish_list.remove(game)
                            st.session_state.wish_names.remove(game.gname)
                            Methods.update_user_lists()
                            st.rerun()
                        if st.button("Add To Cart", key=f"{game.gname}_wish_to_cart"):
                            cart = Cart()
                            cart.add_game(game)
                            if game in st.session_state.wish_list:
                                st.session_state.wish_list.remove(game)
                                st.session_state.wish_names.remove(game.gname)
                            Methods.update_user_lists()
                            st.rerun()
                with photo:
                    response = requests.get(game.gimage)
                    img = Image.open(io.BytesIO(response.content))
                    img = img.resize((300, 175))
                    st.image(img)
                st.divider()

        if st.button("Clear Wishlist"):
            st.session_state.wish_list = []
            st.session_state.wish_names = set()
            Methods.update_user_lists()
            st.rerun()