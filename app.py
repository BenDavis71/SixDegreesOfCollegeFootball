#!/usr/bin/env python
# coding: utf-8


import numpy as np
import pandas as pd
import networkx as nx
import streamlit as st
import graphviz as graphviz



st.title('Six Degrees of College Football')
st.markdown('_Data courtesy of BorderingOnWisdom | Inspiration from @__DapperDan_')

@st.cache
def getData():
    url = 'https://raw.githubusercontent.com/BenDavis71/SixDegreesOfCollegeFootball/master/CFB%20Coaches.csv'
    df = pd.read_csv(url)
    return df

def addTeamsAndCoachesToGraph(row):
    if row.squad not in added_nodes:
        G.add_node(row.squad)
        added_nodes.append(row.squad)
    if row.coach not in added_nodes:
        G.add_node(row.coach)
        added_nodes.append(row.coach)
    G.add_edge(row.squad, row.coach)   


df = getData()

G = nx.Graph()
added_nodes = []

_ = df.apply(lambda r: addTeamsAndCoachesToGraph(r), axis=1)


coaches = list(list(df.sort_values(by='coach')['coach'].unique()))

a = st.selectbox(
    "Select first coach",coaches, index = 104
)

b = st.selectbox(
    "Select second coach",coaches, index = 110
)





path = nx.shortest_path(G,source=a,target=b)
st.markdown('**{0} and {1} are separated by {2} degrees: \n**'.format(a, b, int(len(path)/2)))


i = 0
graph = graphviz.Digraph()
for _ in path:
    if i + 1 == len(path):
        break
    #st.write('{0} was on the {1} team with {2}'.format(path[i], path[i+1], path[i+2]))
    graph.edge(path[i], path[i+2], label=path[i+1])
    i+=2

st.graphviz_chart(graph)