import supabase_connect as spc
import streamlit as st
from method import Methods,Wishlist,Cart,Game_Details
st.set_page_config(layout="wide")

def load_webpage():
    w=Webpage()
    w.home()

class Games(Game_Details):
    def __init__(self):
        self.games_list=[]
        games_data = spc.supabase.table("games").select("*").execute().data
        for game in games_data:
            self.games_list.append(Game_Details(
                gno=game["g_id"],
                gtype=game["g_type"],
                gname=game["g_name"],
                gprice=game["g_price"],
                gsize=game["g_size"],
                grate=game["g_rate"],
                grelease_date=game["g_date"],
                gdescription=game["g_description"],
                gimage=game["g_image"],
                gdiscount=game["g_discount"]
            ))

class Webpage():
    def home(self):
        g=Games()
        st.image("https://djsrwvtvtkoctdywccxw.supabase.co/storage/v1/object/public/Games_image/gamehub.jpg",width=1550)
        Recommended,Browes,Categories,Sort,Free,Wishlists,Carts,Library,Account=st.tabs(["Recommended","Browes","Categories","Sort","Free Games","Wishlist","Cart","Library","Account"])
        with Recommended:
            Methods.recomanded(g.games_list)
        with Browes:    
            Methods.browes(g.games_list)
        with Categories:
            Methods.category(g.games_list)
        with Sort:
            Methods.sort(g.games_list)
        with Free:
            Methods.free_games(g.games_list)
        with Account:
            Methods.account()
        with Carts:
            cart=Cart()
            cart.show_cart()
        with Wishlists:
            wishlist=Wishlist()
            wishlist.show_wishlist()
        with Library:
            Methods.library()
