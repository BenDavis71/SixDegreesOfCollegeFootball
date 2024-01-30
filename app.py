#!/usr/bin/env python
# coding: utf-8


import numpy as np
import pandas as pd
import networkx as nx
import streamlit as st
import graphviz as graphviz



st.title('Six Degrees of College Football')
st.markdown('_Data courtesy of BorderingOnWisdom | Inspiration from Sennua Lawson')


#read-in data that was collected from https://borderingonwisdom.wordpress.com/college-football-coach-database/ then processed in a jupyter notebook
#cache this function so that streamlit doesn't rerun it everytime a user input is changed
@st.cache
def getData():
    url = 'https://raw.githubusercontent.com/BenDavis71/SixDegreesOfCollegeFootball/master/CFB%20Coaches.csv'
    df = pd.read_csv(url)
    return df


#add nodes for the coach and team of the row passed in from the df if the nodes have yet to be added
#add edge connecting the coach node to the team node
def addTeamsAndCoachesToGraph(row):
    if row.squad not in added_nodes:
        G.add_node(row.squad)
        added_nodes.append(row.squad)
    if row.coach not in added_nodes:
        G.add_node(row.coach)
        added_nodes.append(row.coach)
    G.add_edge(row.squad, row.coach)   


df = getData()

#initialize NetworkX grpah and list of added coaches/teams
G = nx.Graph()
added_nodes = []


#run function on each row of df and assign return value to dummy variable (graph G is constructed within the function itself)
_ = df.apply(lambda r: addTeamsAndCoachesToGraph(r), axis=1)




#generate list of coaches (alphabetical order with duplicates removed) from dataframe
coaches = list(list(df.sort_values(by='coach')['coach'].unique()))


#streamlit user input for start and end points of desired path
a = st.selectbox(
    "Select first coach", coaches, index = coaches.index('Mike Leach')
)

b = st.selectbox(
    "Select second coach", coaches, index = coaches.index('Nick Saban')
)


#networkx function finds the shortest path between the user-specified coaches
path = nx.shortest_path(G,source=a,target=b)

#in order to count degrees of separation, we divide by the length of the shortest path two and use the floor
#this is because by default, path includes the schools connecting the coaches
st.markdown('**{0} and {1} are separated by {2} degrees: \n**'.format(a, b, int(len(path)/2)))


#initialize shortest path graph
graph = graphviz.Digraph()


#initialize variable to loop through in order to access multiple indices of the path during a single iteration
i = 0

#for loop to construct shortest path graph
for _ in path:
    if i + 1 == len(path):
        break  #exit function once we  have created all relevant nodes and edges
    graph.edge(path[i], path[i+2], label=path[i+1])
    i+=2

st.graphviz_chart(str(graph))


st.markdown('___')
st.markdown('Created by [Ben Davis](https://github.com/BenDavis71/)')
