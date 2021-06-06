import streamlit as st

import networkx as nx
import matplotlib.pyplot as plt 
import pandas as pd
import seaborn as sns
import logging
import numpy as np
import geopandas as gpd
from geopy.geocoders import Nominatim
from shapely.wkt import loads
from scipy.spatial.distance import cdist

import plotly.graph_objects as go

# Let's brag about digital twins ;)
import sgp_dt as dt


@st.cache(allow_output_mutation=True)#allow_output_mutation=True)
def loadShp(path):
    # Reading the overall network
    G= nx.readwrite.nx_shp.read_shp(path)
    # Support to network identification
    df_nodes = pd.read_csv("data/SG_nodes.txt", index_col=0)
    # Some cleaning necessary for csv loadup
    dfNodes = pd.read_csv("data/dfNodes.csv.zip")
    dfNodes.Pos = dfNodes.Pos.apply(lambda x: eval(x))
    dfEdges = pd.read_csv("data/dfEdges.csv.zip") 
    dfEdges.geometry = dfEdges.geometry.apply(lambda x: loads(x.replace('\'', '')))
    # Additional layers  
    gTrees = gpd.read_file('data/sTrees.zip') 
    gLamps = gpd.read_file('data/sLamps.zip') 
    gPark = gpd.read_file('data/sParks.zip') 
    gCCTV = gpd.read_file('data/sCCTV.zip') 
    return G, df_nodes, dfNodes, dfEdges, gTrees, gLamps, gPark, gCCTV

# This call should be cached
G, df_nodes, dfNodes, dfEdges, gTrees, gLamps, gPark, gCCTV = loadShp("data/s4/SingaporeLampsCCTVTrees.shp")


# Writing the sidebar

UseDummyPoints= st.sidebar.checkbox('Dummy values',value = True)
if not UseDummyPoints:
    start_point = st.sidebar.text_input('Choose starting point...',"Marina Bay, Singapore") 
    end_point = st.sidebar.text_input('Choose destination...',"Boat Quay, Singapore") 

#security = st.sidebar.checkbox('Security',value = True)
security =1
if security:
    cctv_perf = st.sidebar.slider ( "CCTV" , min_value=0 , max_value=1000 , value=0 , step=1 , format=None , key=None )
    lamps_perf = st.sidebar.slider ( "Lamps" , min_value=0 , max_value=1000 , value=0 , step=1 , format=None , key=None ) 
    trees_perf = st.sidebar.slider ( "Trees" , min_value=0 , max_value=1000 , value=0 , step=1 , format=None , key=None ) 
    #@todo add type of walk, presence of trees
    
if UseDummyPoints:
    start,end = dt.getStartEnd("nop", "end", df_nodes, dummy= UseDummyPoints)
else:
    start,end = dt.getStartEnd(start_point, end_point, df_nodes, dummy= UseDummyPoints)

weighted_G  = dt.modernGraphWeightUpdates(G,cctv_perf,lamps_perf,trees_perf)

fig = dt.mapIt(start,end,weighted_G,dfNodes,dfEdges)

st.write(fig)