import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
import yfinance as yf
import statistics
from PIL import Image








st.title("Live Trading Dashboard")
img = Image.open('trading.jpg')
st.image(img)
    
ticker = st.sidebar.text_input('Ticker')
start_date = st.sidebar.date_input('Start Date')
end_date = st.sidebar.date_input('End Date')

data = yf.download(ticker,start=start_date, end=end_date)
data

fig = px.line(data, x =data.index, y = data['Adj Close'], title = ticker)
st.plotly_chart(fig)

pricing_data, fundamental_data, news = st.tabs(["Pricing Data", "Fundamental Data", "Top 20 News"])

with pricing_data:
     st.header('Price Movements')
     data2 = data
     data2['% Change'] = data['Adj Close'] / data['Adj Close'].shift(1) - 1
     data2.dropna(inplace = True)
     st.write(data2)
     annual_return = data2['% Change'].mean()*252*100
     st.write('Annual Return is', annual_return, '%' )
     stdev = np.std(data2['% Change'])*np.sqrt(252)
     st.write('Standard Deviation is',stdev*100,'%')
     st.write('Risk Adj. Return is', annual_return/(stdev*100))






with fundamental_data:
    st.write('Fundamental')


from stocknews import StockNews
with news:
        st.header(f'News of {ticker}')
        sn = StockNews(ticker, save_news=False)
        df_news = sn.read_rss()
        for i in range(10):
              st.subheader(f'News {i+1}')
              st.write(df_news['published'][i])
              st.write(df_news['title'][i])
              st.write(df_news['summary'][i])
              title_sentiment = df_news['sentiment_title'][i]
              st.write(f'Title Sentiment{title_sentiment}')
              news_sentiment = df_news['sentiment_summary'][i]  
              st.write(f'News Sentiment {news_sentiment}')      
        



     



