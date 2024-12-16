import streamlit as st
import pandas as pd
import numpy as np
import math as mt
import random
from bs4 import BeautifulSoup
import re



def page():
 st.write("osman")
def sonuc():
 st.write("Osman2")

pg = st.navigation([
    st.Page(sonuc, title="First page", icon="🔥"),
    st.Page(page, title="Second page", icon=":material/favorite:"),
])
pg.run()
