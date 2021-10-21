import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import bar_chart_race as bcr


st.set_page_config(page_title='Projet Streamlit Japhet',
                   layout="wide")
st.image('netflix-logo-2.jpg')

url={
"linkedin" : {
           "img" : "https://img.shields.io/badge/Japhet-0077B5?style=for-the-badge&logo=linkedin&logoColor=white&link=https://www.linkedin.com/in/ditsouga-perera-japhet",
           "url" : "https://www.linkedin.com/in/ditsouga-perera-japhet"           }
}
st.sidebar.write(f"[![Connect]({url['linkedin']['img']})]({url['linkedin']['url']})")
st.sidebar.header('My personnal Netflix data')
st.sidebar.markdown('some information about this')
menu = st.sidebar.radio(
    "",
    ("Intro", "Data", "data Variables", "shape", "describe"),
)
st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

st.sidebar.markdown('---')
st.sidebar.write('Data visualisation | Japhet 2021. https://github.com/pererajaphet ')

#####
st.title("Analysis of my Netflix Data")
st.markdown("### Since its emergence Netflix has become a leader in the world of online entertainment with numerous catalogues such as films, series, documentaries and children animation. It has been a global revolution, because long before it appeared, we had to buy DVDs or go to the cinema to be entertained. However, we do not have access to a great cinematographic diversity. Being a great user of Netflix, I intend today, I make you discover my Netflix data. You will discover with me my favourite movies and series, the time I spend on each Netflix entertainment. This application is a Streamlit dashbord to analyze my Netflix Data. ")


#st.sidebar.markdown('hey')
data = pd.read_csv('~/Downloads/ViewingActivity.csv')
if menu == 'Data':
    st.write(data)
elif menu == 'data Variables':
    st.write(data.columns)
elif menu == 'shape':
    st.write(data.shape)
elif menu =='describe':
    st.write(data.describe())

#----- Modifications
def count_rows(rows): 
    return len(rows)

def get_hour(dt):
    return dt.hour

data.fillna(method='bfill',inplace=True)
df = data
st.sidebar.header(" New Dataset, cleaned and transformed, infos")
select0 = st.sidebar.selectbox("See some information about the new dataset", ['info','df shape', 'df describe'], key ="1")
if select0=="info":
    st.write(df.info())
elif select0=="df shape":
    st.write(df.shape)
else:
    st.write(df.describe())

df['Start Time']=pd.to_datetime(df['Start Time'])
def get_minute(dt):
    return dt.minute
df['Bookmark']=pd.to_datetime(df['Bookmark'])
df['minute'] = df['Bookmark'].map(get_minute)

st.sidebar.header("My Netflix Dataset")
select = st.sidebar.selectbox("See Dataset", ['no', 'yes'], key ="2")
if select == "yes":
    st.sidebar.markdown("My Netflix Dataset is given below:-")
    st.write(df)

st.sidebar.header("Rating Title")
select1 = st.sidebar.selectbox("Visualisation type", ['Histogram', 'Pie chart'], key="3")
df_=df[:50]
rating_count = df_['Title'].value_counts()
rating_count = pd.DataFrame({'rating Title': rating_count.index, 'Rating_count':rating_count.values})
if not st.sidebar.checkbox("Hide", True, key="2"):
    st.sidebar.markdown("Rating Title for all Netflix Movies/seies")
    if select1=="Histogram":
        fig = px.bar(rating_count, x="rating Title", y="Rating_count", height=500)
        st.plotly_chart(fig)
    else:
        fig = px.pie(rating_count, values = "Rating_count", names="rating Title")
        st.plotly_chart(fig)

st.sidebar.header("Rating minute")
select2=st.sidebar.selectbox("Visualization type", ['Histogram', 'Pie Chart'], key="4")
rating_count1=df_["minute"].value_counts()
rating_count1 = pd.DataFrame({'rating minute': rating_count1.index, 'rating_count1':rating_count1.values})
if not st.sidebar.checkbox("Hide", True, key="3"):
    st.sidebar.markdown("Rating minute for all Netflix Movies/seies")
    if select2=="Histogram":
        fig1 = px.bar(rating_count1, x="rating minute", y="rating_count1", height=500)
        st.plotly_chart(fig1)
    else:
        fig1 = px.pie(rating_count1, values = "rating_count1", names="rating minute")
        st.plotly_chart(fig1)

##----Above are the entertainments which have a duration 20 minutes or more 
st.title('Above are the entertainments which have a duration 20 minutes or more')
st.markdown("### In this section, we only consider data on entertainment with a duration of more than 20 minutes.")
Time_view = df[df['minute']>20]
if st.checkbox('show bar'):
    fig3 = px.bar(
      Time_view[:30],
      x="minute",
      y='Title',
      color='Device Type',
      orientation='h'
      )
    st.plotly_chart(fig3)

if st.checkbox('show bar2 '):
    fig5 = px.bar(Time_view[:40], x="Title", y="minute", height=500)
    st.plotly_chart(fig5)


if st.checkbox('show barplot'):
    fig4, ax = plt.subplots()
    sns.barplot(x = 'minute', 
    y = 'Title',
    hue ='Device Type',
    data =Time_view[:20],
    ax=ax
    )
    st.write(fig4)

###------------Above are the entertainments which have a duration less than 20 minutes
st.title('Above are the entertainments which have a duration less than 20 minutes')
st.markdown("### In this section, we only consider data on entertainment with a duration less than 20 minutes.")
Time_inf_view = df[df['minute']<=20]
if st.checkbox('show bar inf'):
    fig3 = px.bar(
      Time_inf_view[:30],
      x="minute",
      y='Title',
      color='Device Type',
      orientation='h'
      )
    st.plotly_chart(fig3)

if st.checkbox('show bar2 inf'):
    fig5 = px.bar(Time_inf_view[:40], x="Title", y="minute", height=500)
    st.plotly_chart(fig5)


if st.checkbox('show barplot inf'):
    fig4, ax = plt.subplots()
    sns.barplot(x = 'minute', 
    y = 'Title',
    hue ='Device Type',
    data =Time_inf_view[:20],
    ax=ax
    )
    st.write(fig4)



####-----Restriction
st.title('Restriction')
st.markdown("### We notice that the data from the entertainment with a duration of more than 20 minutes are more telling and significant than those with a duration of less than 20 minutes. So, for the rest of this presentation, we will just take into account the data of my Netflix programmes with a duration of more than 20 minutes. This will allow us to have more concrete results on my Netflix activity.")
Minute_hight = df[df['minute']>20][['Profile Name','Start Time', 'Title','Supplemental Video Type','Device Type', 'Country', 'minute']].sort_values('minute', ascending = True)

if st.checkbox('Minute_hight.head'):
    st.write(Minute_hight.head())

Minute_hight['Titles'] = Minute_hight['Title'].map(count_rows)
if st.checkbox("chart_data"):
    chart_data=pd.DataFrame(Minute_hight, columns=['Titles', 'minute'])
    st.area_chart(chart_data)

rating_count_ = Minute_hight['Device Type'].value_counts()
rating_count_= pd.DataFrame({'rating minute': rating_count_.index, 'rating_count_':rating_count_.values})
if st.checkbox('show pie Minute_hight_'):
    fig6 = px.pie(rating_count_, values= 'rating_count_', names='rating minute')
    st.plotly_chart(fig6)

st.markdown('### who watches more Netflix, between my friends and me?')
rating_count_1 = Minute_hight['Profile Name'].value_counts()
rating_count_1= pd.DataFrame({'rating minute': rating_count_1.index, 'rating_count_1':rating_count_1.values})
if st.checkbox('show pie Profile Name'):
    fig7 = px.pie(rating_count_1, values= 'rating_count_1', names='rating minute')
    st.plotly_chart(fig7)

st.markdown('### the categories of films/series I watch the most.')
rating_count_2 = Minute_hight['Supplemental Video Type'].value_counts()
rating_count_2= pd.DataFrame({'rating minute': rating_count_2.index, 'rating_count_2':rating_count_2.values})
if st.checkbox('show pie Supplemental Video Type'):
    fig8 = px.pie(rating_count_2, values= 'rating_count_2', names='rating minute')
    st.plotly_chart(fig8)

if st.checkbox('The power of the VPN'):
    mymap = pd.DataFrame({
    'awesome country' : Minute_hight['Country'],
    'lat' : Minute_hight['minute'],
    'lon' : Minute_hight['minute']
    })
    st.map(mymap)

#####--------Play
st.title("Play")
st.markdown("### Here, we have a short play which show Times that spent on my Netflix entertainment by data. Indeed, I watch a lot of Netflix programmes, so it is important to have an overview of it all. I have been restraining my data so o do not have a long video? You are ready, let's go !")
if st.checkbox("show video"):
    Minute_hight_=Minute_hight[:200]
    df_column = Minute_hight_[['Start Time', 'Title', 'minute']]
    df_column = pd.pivot_table(df_column, index=['Start Time'], columns=['Title'], values=['minute'])
    df.index.name = None
    df_column.columns = [col[1] for col in df_column.columns]
    df_column = df_column.fillna(0).astype(int)
    df_column.columns = [col.replace('-', ' ') for col in df_column.columns]
    Title_reserved = set()
    for index, row in df_column.iterrows():
        Title_reserved |= set(row[row > 0].sort_values(ascending=False).head(10).index)
    df_column = df_column[list(Title_reserved)]
    video=bcr.bar_chart_race(
    df_column,
    filename=None,
    n_bars=10,
    period_fmt='%B %d, %Y',
    title='The times spent on my Netflix entertainment by date'
    )
    st.write(video)