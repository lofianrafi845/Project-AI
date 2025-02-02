# import streamlit as st
# import yfinance as yf
# import plotly.graph_objects as go
# import pickle
# import numpy as np
# from datetime import datetime, timedelta
# import pandas as pd

# # Set page config
# st.set_page_config(page_title="KKB Project", layout="wide")

# # Custom CSS to maintain similar styling
# st.markdown("""
#     <style>
#     .stButton > button {
#         background-color: #007BFF;
#         color: white;
#         border-radius: 5px;
#         padding: 10px 20px;
#         border: none;
#         margin: 10px 0;
#     }
#     .stButton > button:hover {
#         background-color: #0056b3;
#     }
#     .main {
#         padding: 20px;
#         background-color: white;
#         border-radius: 10px;
#         box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
#     }
#     h1, h2, h3 {
#         color: #007bff;
#     }
#     </style>
# """, unsafe_allow_html=True)

# class MLR:
#     def __init__(self, data):
#         X = [list(i[:-1]) for i in data]
#         for xi in X:
#             xi.insert(0, 1)
#         X = np.array(X)
#         Y = np.array([[i[-1]] for i in data])
#         y_bar = sum(Y)/len(Y)
#         XT = X.T
#         XTX = np.dot(XT, X)
#         XTX_inv = np.linalg.inv(XTX)
#         XTY = np.dot(XT, Y)
#         self.B = np.dot(XTX_inv, XTY)
#         self.SST = sum([(Y[i][0] - y_bar)**2 for i in range(len(X))])
#         y_pred = []
#         for i in range(len(X)):
#             t_pred = self.B[0][0]
#             for b in range(1, len(self.B)):
#                 px = X[i][b-1]*self.B[b][0]
#                 t_pred += px
#             y_pred.append(t_pred)
#         self.SSE = sum([(Y[i][0] - y_pred[i])**2 for i in range(len(X))])
#         self.R2 = 1 - (self.SSE/self.SST)

#     def predict(self, X):
#         prediction = []
#         for i in range(len(X)):
#             t_pred = self.B[0][0]
#             for b in range(1, len(self.B)):
#                 px = X[i][b-1]*self.B[b][0]
#                 t_pred += px
#             prediction.append(t_pred)
#         return prediction
    
# def main():
#     # Sidebar navigation
#     st.sidebar.title("Navigation")
#     page = st.sidebar.selectbox(
#         "Choose a page",
#         ["Homepage", "About Project", "Stock Analysis"]
#     )

#     if page == "Homepage":
#         show_homepage()
#     elif page == "About Project":
#         show_about()
#     elif page == "Stock Analysis":
#         show_stock_analysis()

# def show_homepage():
#     st.title("Welcome To KKB Project")
#     st.header("Portfolio Optimization")

# def show_about():
#     st.title("About This Project")
#     # Add project description here

# def show_stock_analysis():
#     st.title("Stock Analysis")
    
#     # List of stocks with descriptions
#     stocks = {
#         "BBRI.JK": "Bank Rakyat Indonesia",
#         "BMRI.JK": "Bank Mandiri",
#         "BBCA.JK": "Bank Central Asia",
#         "ASII.JK": "Astra International",
#         "UNVR.JK": "Unilever Indonesia",
#         "TLKM.JK": "Telekomunikasi Indonesia"
#     }
    
#     # Stock selection
#     selected_ticker = st.selectbox(
#         "Select a stock:",
#         list(stocks.keys()),
#         format_func=lambda x: f"{x} - {stocks[x]}"
#     )
    
#     # Create tabs for different views
#     tab1, tab2, tab3 = st.tabs(["Company Details", "Financial Analysis", "Predictions"])
    
#     with tab1:
#         show_company_details(selected_ticker)
    
#     with tab2:
#         show_enhanced_financial_details(selected_ticker)
    
#     with tab3:
#         show_predictions(selected_ticker)

# def show_company_details(ticker):
#     stock = yf.Ticker(ticker)
#     info = stock.info
    
#     st.header("Company Details")
#     col1, col2 = st.columns(2)
    
#     with col1:
#         st.metric("Company Name", info.get('longName', 'N/A'))
#         st.metric("Sector", info.get('sector', 'N/A'))
#         st.metric("Industry", info.get('industry', 'N/A'))
    
#     with col2:
#         st.metric("Market Cap", info.get('marketCap', 'N/A'))
#         st.metric("Previous Close", info.get('previousClose', 'N/A'))

# def show_predictions(ticker):
#     st.header("Stock Predictions")
    
#     try:
#         # Load models
#         my_model = pickle.load(open('./model/my_MLR.pickle', 'rb'))
#         model_teknikal = pickle.load(open('./model/weekly_model.pickle', 'rb'))
        
#         # Get stock data
#         saham = yf.Ticker(ticker)
        
#         # Calculate fundamental prediction
#         # Get historical data for quarterly prediction
#         daftar_harga = saham.history(start='2024-07-01', end='2024-11-01', interval='1mo')
#         daftar_harga.reset_index(inplace=True)
#         q_harga = []
#         for i in range(0, len(daftar_harga), 3):
#             q_harga.append(daftar_harga['Close'][i])
#         q_harga.reverse()

#         # Get financial data
#         neraca = saham.quarterly_balance_sheet
#         income = saham.quarterly_income_stmt

#         # Calculate financial metrics
#         net_income = income.loc['Net Income'].iloc[0:2]
#         saham_beredar = neraca.loc['Ordinary Shares Number'].iloc[0:2]
#         ekuitas = neraca.loc['Total Equity Gross Minority Interest'].iloc[:2]
#         aset = neraca.loc['Total Assets'].iloc[:2]
        
#         # Calculate ratios
#         eps = net_income/saham_beredar
#         bpvs = ekuitas/saham_beredar
#         pb = q_harga/bpvs
#         roa = net_income/aset

#         # Calculate differences
#         diff_net_income = (net_income.iloc[0] - net_income.iloc[1])/net_income.iloc[1]
#         diff_eps = (eps.iloc[0] - eps.iloc[1])/eps.iloc[1]
#         diff_pb = (pb.iloc[0] - pb.iloc[1])/pb.iloc[1]
#         diff_roa = (roa.iloc[0] - roa.iloc[1])/roa.iloc[1]

#         # Make fundamental prediction
#         q_prediction = my_model.predict([[diff_net_income, diff_eps, diff_pb, diff_roa]])
#         q_target_price = q_harga[0] + (q_harga[0] * q_prediction[0])

#         # Calculate technical prediction
#         end_date = datetime.now()
#         start_date = end_date - timedelta(days=100)
#         harga_saham = saham.history(start=start_date, end=end_date)
        
#         # Calculate technical indicators
#         harga_saham['SMA_10'] = harga_saham['Close'].rolling(window=10).mean()
#         harga_saham['SMA_50'] = harga_saham['Close'].rolling(window=50).mean()
        
#         # Calculate RSI
#         delta = harga_saham['Close'].diff(1)
#         gain = delta.clip(lower=0)
#         loss = -delta.clip(upper=0)
#         avg_gain = gain.rolling(window=14).mean()
#         avg_loss = loss.rolling(window=14).mean()
#         rs = avg_gain / avg_loss
#         harga_saham['RSI'] = 100 - (100 / (1 + rs))
        
#         # Calculate Bollinger Bands
#         harga_saham['SMA_20'] = harga_saham['Close'].rolling(window=20).mean()
#         harga_saham['BB_Upper'] = harga_saham['SMA_20'] + 2 * harga_saham['Close'].rolling(window=20).std()
#         harga_saham['BB_Lower'] = harga_saham['SMA_20'] - 2 * harga_saham['Close'].rolling(window=20).std()
        
#         # Calculate ATR
#         high_low = harga_saham['High'] - harga_saham['Low']
#         high_close_prev = np.abs(harga_saham['High'] - harga_saham['Close'].shift(1))
#         low_close_prev = np.abs(harga_saham['Low'] - harga_saham['Close'].shift(1))
#         true_range = pd.concat([high_low, high_close_prev, low_close_prev], axis=1).max(axis=1)
#         harga_saham['ATR'] = true_range.rolling(window=14).mean()
        
#         # Calculate Log Return
#         harga_saham['Log_Return'] = np.log(harga_saham['Close'] / harga_saham['Close'].shift(1))

#         # Make technical prediction
#         hasil_prediksi = model_teknikal.predict([harga_saham.iloc[-1][['SMA_10', 'SMA_50', 'Volume', 'RSI', 'BB_Upper', 'BB_Lower', 'ATR', 'Log_Return']].to_list()])
        
#         # Calculate predicted prices
#         selisih = (float(hasil_prediksi[0]) - harga_saham['Close'].iloc[-1])/5
#         l_pred = []
#         for s in range(1, 6):
#             l_pred.append(harga_saham['Close'].iloc[-1] + (s*selisih))
        
#         # Create prediction dates
#         prediksi_tanggal = [end_date + timedelta(days=i) for i in range(1, 6)]
        
#         # Create prediction dataframe
#         data_prediksi = pd.DataFrame({
#             'Date': prediksi_tanggal,
#             'Close': l_pred
#         })
        
#         # Display predictions
#         st.subheader("Fundamental Analysis Prediction")
#         prediction_value = round(float(q_prediction[0]), 2)
#         color = "green" if prediction_value > 0 else "red"
#         st.markdown(f"<h3 style='color: {color};'>Predicted quarterly change: {prediction_value}%</h3>", unsafe_allow_html=True)
#         st.subheader(f"Rp {q_target_price:,.2f}")
        
#         st.subheader("Technical Analysis Prediction")
        
#         # Prepare data for chart
#         data_harga = harga_saham[['Close']].iloc[:]
#         data_harga.index = data_harga.index.tz_localize(None)
#         data_prediksi['Date'] = pd.to_datetime(data_prediksi['Date'])
#         data_prediksi.set_index('Date', inplace=True)
#         data_final = pd.concat([data_harga, data_prediksi])
        
#         # Create the prediction chart
#         fig = go.Figure()
        
#         # Add historical data
#         fig.add_trace(go.Scatter(
#             x=data_harga.index,
#             y=data_harga['Close'],
#             mode='lines',
#             name='Historical Data',
#             line=dict(color='blue')
#         ))
        
#         # Add prediction data
#         fig.add_trace(go.Scatter(
#             x=data_prediksi.index,
#             y=data_prediksi['Close'],
#             mode='lines',
#             name='Prediction',
#             line=dict(color='orange', dash='dash')
#         ))
        
#         # Update layout
#         fig.update_layout(
#             title=f'Stock Price Prediction for {ticker}',
#             xaxis_title='Date',
#             yaxis_title='Price',
#             showlegend=True,
#             template='plotly_white'
#         )
        
#         # Add separator line
#         fig.add_vline(x=data_harga.index[-1], line_dash="dash", line_color="red")
        
#         # Display the chart
#         st.plotly_chart(fig)
        
#     except Exception as e:
#         st.error(f"Error in prediction: {str(e)}")
#         st.info("Please make sure all required data is available and models are properly loaded.")

# def calculate_detailed_metrics(data_neraca, data_laba, data_arus):
#     metrics = {}
    
#     # Basic Financial Metrics
#     metrics.update(calculate_financial_metrics(data_neraca, data_laba, data_arus))
    
#     # Additional Performance Metrics
#     try:
#         # Calculate EPS
#         net_income = data_laba.loc['Net Income'].iloc[0:2]
#         saham_beredar = data_neraca.loc['Ordinary Shares Number'].iloc[0:2]
#         ekuitas = data_neraca.loc['Total Equity Gross Minority Interest'].iloc[:2]
#         aset = data_neraca.loc['Total Assets'].iloc[:2]
#         revenue = data_laba.loc['Operating Revenue'].iloc[0:2]
        
#         # Current Values
#         eps_now = net_income.iloc[0]/saham_beredar.iloc[0]
#         bvps_now = ekuitas.iloc[0]/saham_beredar.iloc[0]
#         roa_now = net_income.iloc[0]/aset.iloc[0]
#         roe_now = net_income.iloc[0]/ekuitas.iloc[0]
#         net_margin_now = net_income.iloc[0]/revenue.iloc[0]
#         asset_turnover_now = revenue.iloc[0]/aset.iloc[0]
#         der_now = data_neraca.loc['Total Liabilities Net Minority Interest'].iloc[0]/ekuitas.iloc[0]

#         # Previous Values
#         eps_old = net_income.iloc[1]/saham_beredar.iloc[1]
#         bvps_old = ekuitas.iloc[1]/saham_beredar.iloc[1]
#         roa_old = net_income.iloc[1]/aset.iloc[1]
#         roe_old = net_income.iloc[1]/ekuitas.iloc[1]
#         net_margin_old = net_income.iloc[1]/revenue.iloc[1]
#         asset_turnover_old = revenue.iloc[1]/aset.iloc[1]
#         der_old = data_neraca.loc['Total Liabilities Net Minority Interest'].iloc[1]/ekuitas.iloc[1]

#         # Calculate differences
#         metrics['EPS'] = {
#             'value': eps_now,
#             'diff': ((eps_now - eps_old)/eps_old) * 100
#         }
#         metrics['BVPS'] = {
#             'value': bvps_now,
#             'diff': ((bvps_now - bvps_old)/bvps_old) * 100
#         }
#         metrics['ROA'] = {
#             'value': roa_now,
#             'diff': ((roa_now - roa_old)/roa_old) * 100
#         }
#         metrics['ROE'] = {
#             'value': roe_now,
#             'diff': ((roe_now - roe_old)/roe_old) * 100
#         }
#         metrics['Net Margin'] = {
#             'value': net_margin_now,
#             'diff': ((net_margin_now - net_margin_old)/net_margin_old) * 100
#         }
#         metrics['Asset Turnover'] = {
#             'value': asset_turnover_now,
#             'diff': ((asset_turnover_now - asset_turnover_old)/asset_turnover_old) * 100
#         }
#         metrics['DER'] = {
#             'value': der_now,
#             'diff': ((der_now - der_old)/der_old) * 100
#         }
        
#     except Exception as e:
#         st.error(f"Error calculating additional metrics: {str(e)}")
    
#     return metrics

# def calculate_financial_metrics(data_neraca, data_laba, data_arus):
#     metrics = {}
    
#     try:
#         # Net Income
#         net_income_current = data_laba.loc['Net Income'].iloc[0]
#         net_income_prev = data_laba.loc['Net Income'].iloc[1]
#         metrics['Net Income'] = {
#             'value': net_income_current,
#             'diff': ((net_income_current - net_income_prev) / net_income_prev * 100)
#         }
        
#         # Total Assets
#         assets_current = data_neraca.loc['Total Assets'].iloc[0]
#         assets_prev = data_neraca.loc['Total Assets'].iloc[1]
#         metrics['Total Assets'] = {
#             'value': assets_current,
#             'diff': ((assets_current - assets_prev) / assets_prev * 100)
#         }
        
#         # Total Liabilities
#         liabilities_current = data_neraca.loc['Total Liabilities Net Minority Interest'].iloc[0]
#         liabilities_prev = data_neraca.loc['Total Liabilities Net Minority Interest'].iloc[1]
#         metrics['Total Liabilities'] = {
#             'value': liabilities_current,
#             'diff': ((liabilities_current - liabilities_prev) / liabilities_prev * 100)
#         }
        
#         # Total Equity
#         equity_current = data_neraca.loc['Total Equity Gross Minority Interest'].iloc[0]
#         equity_prev = data_neraca.loc['Total Equity Gross Minority Interest'].iloc[1]
#         metrics['Total Equity'] = {
#             'value': equity_current,
#             'diff': ((equity_current - equity_prev) / equity_prev * 100)
#         }
        
#         # Revenue
#         revenue_current = data_laba.loc['Operating Revenue'].iloc[0]
#         revenue_prev = data_laba.loc['Operating Revenue'].iloc[1]
#         metrics['Revenue'] = {
#             'value': revenue_current,
#             'diff': ((revenue_current - revenue_prev) / revenue_prev * 100)
#         }
        
#         # Cash and Cash Equivalents
#         cash_current = data_neraca.loc['Cash And Cash Equivalents'].iloc[0]
#         cash_prev = data_neraca.loc['Cash And Cash Equivalents'].iloc[1]
#         metrics['Cash'] = {
#             'value': cash_current,
#             'diff': ((cash_current - cash_prev) / cash_prev * 100)
#         }
        
#         # Capital Expenditure
#         capex_current = data_arus.loc['Capital Expenditure'].iloc[0]
#         capex_prev = data_arus.loc['Capital Expenditure'].iloc[1]
#         metrics['Capital Expenditure'] = {
#             'value': capex_current,
#             'diff': ((capex_current - capex_prev) / capex_prev * 100)
#         }
        
#         # Outstanding Shares
#         shares = data_neraca.loc['Ordinary Shares Number'].iloc[0]
#         metrics['Outstanding Shares'] = {
#             'value': shares,
#             'diff': None  # No difference calculation for shares
#         }
        
#     except Exception as e:
#         st.error(f"Error calculating financial metrics: {str(e)}")
        
#     return metrics

# def show_enhanced_financial_details(ticker):
#     st.header("Financial Details")
    
#     # Get stock data
#     saham = yf.Ticker(ticker)
    
#     # Get financial statements
#     data_neraca = saham.quarterly_balance_sheet
#     data_laba = saham.quarterly_income_stmt
#     data_arus = saham.quarterly_cash_flow
    
#     # Calculate detailed metrics
#     metrics = calculate_detailed_metrics(data_neraca, data_laba, data_arus)
    
#     # Create tabs for different metric categories
#     tab1, tab2, tab3 = st.tabs(["Basic Financials", "Performance Metrics", "Price Chart"])
    
#     with tab1:
#         col1, col2, col3 = st.columns(3)
        
#         # Balance Sheet Metrics
#         with col1:
#             st.markdown("##### Balance Sheet Metrics")
#             for metric in ['Total Assets', 'Total Liabilities', 'Total Equity']:
#                 if metric in metrics:
#                     st.metric(
#                         metric,
#                         f"{metrics[metric]['value']:,.2f}",
#                         f"{metrics[metric]['diff']:.2f}%"
#                     )
        
#         # Income Statement Metrics
#         with col2:
#             st.markdown("##### Income Statement Metrics")
#             for metric in ['Revenue', 'Net Income', 'EPS']:
#                 if metric in metrics:
#                     st.metric(
#                         metric,
#                         f"{metrics[metric]['value']:,.2f}",
#                         f"{metrics[metric]['diff']:.2f}%"
#                     )
        
#         # Cash Flow Metrics
#         with col3:
#             st.markdown("##### Cash Flow Metrics")
#             for metric in ['Cash', 'Capital Expenditure']:
#                 if metric in metrics:
#                     st.metric(
#                         metric,
#                         f"{metrics[metric]['value']:,.2f}",
#                         f"{metrics[metric]['diff']:.2f}%"
#                     )
    
#     with tab2:
#         col1, col2 = st.columns(2)
        
#         # Profitability Metrics
#         with col1:
#             st.markdown("##### Profitability Metrics")
#             for metric in ['ROA', 'ROE', 'Net Margin']:
#                 if metric in metrics:
#                     st.metric(
#                         metric,
#                         f"{metrics[metric]['value']*100:.2f}%",
#                         f"{metrics[metric]['diff']:.2f}%"
#                     )
        
#         # Efficiency and Leverage Metrics
#         with col2:
#             st.markdown("##### Efficiency & Leverage Metrics")
#             for metric in ['Asset Turnover', 'DER', 'BVPS']:
#                 if metric in metrics:
#                     st.metric(
#                         metric,
#                         f"{metrics[metric]['value']:.2f}",
#                         f"{metrics[metric]['diff']:.2f}%"
#                     )
    
#     with tab3:
#         # Show price charts
#         show_enhanced_stock_chart(ticker)

# def show_enhanced_stock_chart(ticker):
#     # Get stock data for different time periods
#     stock = yf.Ticker(ticker)
#     periods = {
#         'Day': '1d',
#         '5 Days': '5d',
#         '1 Month': '1mo',
#         '3 Months': '3mo',
#         '6 Months': '6mo',
#         '1 Year': '1y',
#         '2 Year': '2y',
#         '5 Year': '5y',
#         'YTD': 'ytd',
#         'Max': 'max'
#     }
    
#     selected_period = st.selectbox('Select Time Period', list(periods.keys()))
    
#     data = stock.history(period=periods[selected_period])
    
#     # Create candlestick chart
#     fig = go.Figure()
    
#     fig.add_trace(go.Candlestick(
#         x=data.index,
#         open=data['Open'],
#         high=data['High'],
#         low=data['Low'],
#         close=data['Close'],
#         name='OHLC'
#     ))
    
#     # Add volume bars
#     fig.add_trace(go.Bar(
#         x=data.index,
#         y=data['Volume'],
#         name='Volume',
#         yaxis='y2',
#         marker_color='rgba(0,0,0,0.2)'
#     ))
    
#     # Update layout for dual axis
#     fig.update_layout(
#         title=f'{ticker} Stock Price and Volume ({selected_period})',
#         yaxis_title='Price',
#         yaxis2=dict(
#             title='Volume',
#             overlaying='y',
#             side='right'
#         ),
#         xaxis_title='Date',
#         height=600
#     )
    
#     st.plotly_chart(fig, use_container_width=True)


# if __name__ == '__main__':
#     main()

import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pickle
import numpy as np
from datetime import datetime, timedelta
import pandas as pd

st.set_page_config(page_title="KKB Project", layout="wide")

st.markdown("""
    <style>
    .stButton > button {
        background-color: #007BFF;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        border: none;
        margin: 10px 0;
    }
    .stButton > button:hover {
        background-color: #0056b3;
    }
    .main {
        padding: 20px;
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    h1, h2, h3 {
        color: #007bff;
    }
    </style>
""", unsafe_allow_html=True)

class MLR:
    def __init__(self, data):
        X = [list(i[:-1]) for i in data]
        for xi in X:
            xi.insert(0, 1)
        X = np.array(X)
        Y = np.array([[i[-1]] for i in data])
        y_bar = sum(Y)/len(Y)
        XT = X.T
        XTX = np.dot(XT, X)
        XTX_inv = np.linalg.inv(XTX)
        XTY = np.dot(XT, Y)
        self.B = np.dot(XTX_inv, XTY)
        self.SST = sum([(Y[i][0] - y_bar)**2 for i in range(len(X))])
        y_pred = []
        for i in range(len(X)):
            t_pred = self.B[0][0]
            for b in range(1, len(self.B)):
                px = X[i][b-1]*self.B[b][0]
                t_pred += px
            y_pred.append(t_pred)
        self.SSE = sum([(Y[i][0] - y_pred[i])**2 for i in range(len(X))])
        self.R2 = 1 - (self.SSE/self.SST)

    def predict(self, X):
        prediction = []
        for i in range(len(X)):
            t_pred = self.B[0][0]
            for b in range(1, len(self.B)):
                px = X[i][b-1]*self.B[b][0]
                t_pred += px
            prediction.append(t_pred)
        return prediction
    
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page",
        ["Homepage", "About Project", "Stock Analysis"]
    )

    if page == "Homepage":
        show_homepage()
    elif page == "About Project":
        show_about()
    elif page == "Stock Analysis":
        show_stock_analysis()

def show_homepage():
    st.title("Welcome To KKB Project")
    st.header("Portfolio Optimization")

def show_about():
    st.title("Proyek Prediksi Harga Saham")

    st.header("Deskripsi Proyek")
    st.write("""
    Proyek ini bertujuan untuk mengembangkan model prediksi harga saham menggunakan teknik regresi. 
    Dengan mengolah data historis harga saham dan faktor-faktor keuangan lainnya, model ini 
    memberikan prediksi pergerakan harga saham di masa depan yang dapat membantu investor dalam 
    pengambilan keputusan investasi yang lebih baik.
    """)

    st.header("Metodologi")
    st.write("""
    Model prediksi harga saham ini menggunakan metode analisis regresi linier berganda. 
    Proyek ini bertujuan untuk mengidentifikasi pola pergerakan harga saham yang dapat 
    membantu dalam pengambilan keputusan investasi.
    """)

    st.header("Data yang Digunakan")
    st.write("""
    Data yang digunakan dalam proyek ini mencakup data historis harga saham, volume perdagangan, 
    serta indikator teknikal dan fundamental yang relevan. Data ini diambil dari berbagai sumber 
    terpercaya untuk memastikan akurasi dan kualitas model prediksi.
    """)

    st.header("Tujuan dan Manfaat")
    st.write("""
    Tujuan utama dari proyek ini adalah untuk memberikan wawasan lebih dalam tentang pergerakan 
    harga saham di masa depan, yang dapat digunakan oleh investor untuk membuat keputusan yang 
    lebih cerdas dan terinformasi dalam dunia investasi saham.
    """)

    st.header("Aplikasi dan Penggunaan")
    st.write("""
    Proyek ini dapat digunakan oleh berbagai pihak yang terlibat dalam pasar saham, seperti 
    investor individu, dan trafer untuk mengevaluasi potensi pergerakan harga saham dan 
    memutuskan langkah-langkah yang tepat dalam strategi investasi mereka.
    """)

    st.header("Evaluasi Model")
    st.write("""
    Untuk melihat lebih detail tentang bagaimana performa model, anda bisa klik di """)
    st.markdown("[sini](https://colab.research.google.com/drive/1gVXrpn8dPvamLaep5QTzytQLLYtLAkIt?usp=sharing)")

    st.markdown("---")
    st.markdown("<div style='text-align: center; color: #007bff;'>&copy; KKB Project</div>", 
                unsafe_allow_html=True)

    st.markdown("""
        <style>
        h1 {
            color: #007bff;
            text-align: center;
        }
        h2 {
            color: #007bff;
        }
        p {
            line-height: 1.6;
        }
        </style>
    """, unsafe_allow_html=True)

def show_stock_analysis():
    st.title("Stock Analysis")
    
    stocks = {
        "BBRI.JK": "Bank Rakyat Indonesia",
        "BMRI.JK": "Bank Mandiri",
        "BBCA.JK": "Bank Central Asia",
        "ASII.JK": "Astra International",
        "UNVR.JK": "Unilever Indonesia",
        "TLKM.JK": "Telekomunikasi Indonesia"
    }
    
    selected_ticker = st.selectbox(
        "Select a stock:",
        list(stocks.keys()),
        format_func=lambda x: f"{x} - {stocks[x]}"
    )
    
    tab1, tab2, tab3 = st.tabs(["Company Details", "Financial Analysis", "Predictions"])
    
    with tab1:
        show_company_details(selected_ticker)
    
    with tab2:
        show_enhanced_financial_details(selected_ticker)
    
    with tab3:
        show_predictions(selected_ticker)

def show_company_details(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    
    st.header("Company Details")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Company Name", info.get('longName', 'N/A'))
        st.metric("Sector", info.get('sector', 'N/A'))
        st.metric("Industry", info.get('industry', 'N/A'))
    
    with col2:
        st.metric("Market Cap", info.get('marketCap', 'N/A'))
        st.metric("Previous Close", info.get('previousClose', 'N/A'))

def show_predictions(ticker):
    st.header("Stock Predictions")
    
    try:
        my_model = pickle.load(open('./model/my_MLR.pickle', 'rb'))
        model_teknikal = pickle.load(open('./model/weekly_model.pickle', 'rb'))
        
        saham = yf.Ticker(ticker)
        
        daftar_harga = saham.history(start='2024-07-01', end='2024-11-01', interval='1mo')
        daftar_harga.reset_index(inplace=True)
        q_harga = []
        for i in range(0, len(daftar_harga), 3):
            q_harga.append(daftar_harga['Close'][i])
        q_harga.reverse()

        neraca = saham.quarterly_balance_sheet
        income = saham.quarterly_income_stmt

        net_income = income.loc['Net Income'].iloc[0:2]
        saham_beredar = neraca.loc['Ordinary Shares Number'].iloc[0:2]
        ekuitas = neraca.loc['Total Equity Gross Minority Interest'].iloc[:2]
        aset = neraca.loc['Total Assets'].iloc[:2]
        
        eps = net_income/saham_beredar
        bpvs = ekuitas/saham_beredar
        pb = q_harga/bpvs
        roa = net_income/aset

        diff_net_income = (net_income.iloc[0] - net_income.iloc[1])/net_income.iloc[1]
        diff_eps = (eps.iloc[0] - eps.iloc[1])/eps.iloc[1]
        diff_pb = (pb.iloc[0] - pb.iloc[1])/pb.iloc[1]
        diff_roa = (roa.iloc[0] - roa.iloc[1])/roa.iloc[1]

        q_prediction = my_model.predict([[diff_net_income, diff_eps, diff_pb, diff_roa]])
        q_target_price = q_harga[0] + (q_harga[0] * q_prediction[0])

        end_date = datetime.now()
        start_date = end_date - timedelta(days=100)
        harga_saham = saham.history(start=start_date, end=end_date)
        
        harga_saham['SMA_10'] = harga_saham['Close'].rolling(window=10).mean()
        harga_saham['SMA_50'] = harga_saham['Close'].rolling(window=50).mean()
        
        delta = harga_saham['Close'].diff(1)
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        avg_gain = gain.rolling(window=14).mean()
        avg_loss = loss.rolling(window=14).mean()
        rs = avg_gain / avg_loss
        harga_saham['RSI'] = 100 - (100 / (1 + rs))
        
        harga_saham['SMA_20'] = harga_saham['Close'].rolling(window=20).mean()
        harga_saham['BB_Upper'] = harga_saham['SMA_20'] + 2 * harga_saham['Close'].rolling(window=20).std()
        harga_saham['BB_Lower'] = harga_saham['SMA_20'] - 2 * harga_saham['Close'].rolling(window=20).std()
        
        high_low = harga_saham['High'] - harga_saham['Low']
        high_close_prev = np.abs(harga_saham['High'] - harga_saham['Close'].shift(1))
        low_close_prev = np.abs(harga_saham['Low'] - harga_saham['Close'].shift(1))
        true_range = pd.concat([high_low, high_close_prev, low_close_prev], axis=1).max(axis=1)
        harga_saham['ATR'] = true_range.rolling(window=14).mean()
        
        harga_saham['Log_Return'] = np.log(harga_saham['Close'] / harga_saham['Close'].shift(1))

        hasil_prediksi = model_teknikal.predict([harga_saham.iloc[-1][['SMA_10', 'SMA_50', 'Volume', 'RSI', 'BB_Upper', 'BB_Lower', 'ATR', 'Log_Return']].to_list()])
        
        selisih = (float(hasil_prediksi[0]) - harga_saham['Close'].iloc[-1])/5
        l_pred = []
        for s in range(1, 6):
            l_pred.append(harga_saham['Close'].iloc[-1] + (s*selisih))
        
        prediksi_tanggal = [end_date + timedelta(days=i) for i in range(1, 6)]
        
        data_prediksi = pd.DataFrame({
            'Date': prediksi_tanggal,
            'Close': l_pred
        })
        
        # Display predictions
        st.subheader("Fundamental Analysis Prediction")
        prediction_value = round(float(q_prediction[0]), 2)
        color = "green" if prediction_value > 0 else "red"
        st.markdown(f"<h3 style='color: {color};'>Predicted quarterly change: {prediction_value}%</h3>", unsafe_allow_html=True)
        st.subheader(f"Rp {q_target_price:,.2f}")
        
        st.subheader("Technical Analysis Prediction")
        
        # Prepare data for chart
        data_harga = harga_saham[['Close']].iloc[:]
        data_harga.index = data_harga.index.tz_localize(None)
        data_prediksi['Date'] = pd.to_datetime(data_prediksi['Date'])
        data_prediksi.set_index('Date', inplace=True)
        data_final = pd.concat([data_harga, data_prediksi])
        
        # Create the prediction chart
        fig = go.Figure()
        
        # Add historical data
        fig.add_trace(go.Scatter(
            x=data_harga.index,
            y=data_harga['Close'],
            mode='lines',
            name='Historical Data',
            line=dict(color='blue')
        ))
        
        # Add prediction data
        fig.add_trace(go.Scatter(
            x=data_prediksi.index,
            y=data_prediksi['Close'],
            mode='lines',
            name='Prediction',
            line=dict(color='orange', dash='dash')
        ))
        
        # Update layout
        fig.update_layout(
            title=f'Stock Price Prediction for {ticker}',
            xaxis_title='Date',
            yaxis_title='Price',
            showlegend=True,
            template='plotly_white'
        )
        
        # Add separator line
        fig.add_vline(x=data_harga.index[-1], line_dash="dash", line_color="red")
        
        # Display the chart
        st.plotly_chart(fig)
        
    except Exception as e:
        st.error(f"Error in prediction: {str(e)}")
        st.info("Please make sure all required data is available and models are properly loaded.")

def calculate_detailed_metrics(data_neraca, data_laba, data_arus):
    metrics = {}
    
    # Basic Financial Metrics
    metrics.update(calculate_financial_metrics(data_neraca, data_laba, data_arus))
    
    # Additional Performance Metrics
    try:
        # Calculate EPS
        net_income = data_laba.loc['Net Income'].iloc[0:2]
        saham_beredar = data_neraca.loc['Ordinary Shares Number'].iloc[0:2]
        ekuitas = data_neraca.loc['Total Equity Gross Minority Interest'].iloc[:2]
        aset = data_neraca.loc['Total Assets'].iloc[:2]
        revenue = data_laba.loc['Operating Revenue'].iloc[0:2]
        
        # Current Values
        eps_now = net_income.iloc[0]/saham_beredar.iloc[0]
        bvps_now = ekuitas.iloc[0]/saham_beredar.iloc[0]
        roa_now = net_income.iloc[0]/aset.iloc[0]
        roe_now = net_income.iloc[0]/ekuitas.iloc[0]
        net_margin_now = net_income.iloc[0]/revenue.iloc[0]
        asset_turnover_now = revenue.iloc[0]/aset.iloc[0]
        der_now = data_neraca.loc['Total Liabilities Net Minority Interest'].iloc[0]/ekuitas.iloc[0]

        # Previous Values
        eps_old = net_income.iloc[1]/saham_beredar.iloc[1]
        bvps_old = ekuitas.iloc[1]/saham_beredar.iloc[1]
        roa_old = net_income.iloc[1]/aset.iloc[1]
        roe_old = net_income.iloc[1]/ekuitas.iloc[1]
        net_margin_old = net_income.iloc[1]/revenue.iloc[1]
        asset_turnover_old = revenue.iloc[1]/aset.iloc[1]
        der_old = data_neraca.loc['Total Liabilities Net Minority Interest'].iloc[1]/ekuitas.iloc[1]

        # Calculate differences
        metrics['EPS'] = {
            'value': eps_now,
            'diff': ((eps_now - eps_old)/eps_old) * 100
        }
        metrics['BVPS'] = {
            'value': bvps_now,
            'diff': ((bvps_now - bvps_old)/bvps_old) * 100
        }
        metrics['ROA'] = {
            'value': roa_now,
            'diff': ((roa_now - roa_old)/roa_old) * 100
        }
        metrics['ROE'] = {
            'value': roe_now,
            'diff': ((roe_now - roe_old)/roe_old) * 100
        }
        metrics['Net Margin'] = {
            'value': net_margin_now,
            'diff': ((net_margin_now - net_margin_old)/net_margin_old) * 100
        }
        metrics['Asset Turnover'] = {
            'value': asset_turnover_now,
            'diff': ((asset_turnover_now - asset_turnover_old)/asset_turnover_old) * 100
        }
        metrics['DER'] = {
            'value': der_now,
            'diff': ((der_now - der_old)/der_old) * 100
        }
        
    except Exception as e:
        st.error(f"Error calculating additional metrics: {str(e)}")
    
    return metrics

def calculate_financial_metrics(data_neraca, data_laba, data_arus):
    metrics = {}
    
    try:
        # Net Income
        net_income_current = data_laba.loc['Net Income'].iloc[0]
        net_income_prev = data_laba.loc['Net Income'].iloc[1]
        metrics['Net Income'] = {
            'value': net_income_current,
            'diff': ((net_income_current - net_income_prev) / net_income_prev * 100)
        }
        
        # Total Assets
        assets_current = data_neraca.loc['Total Assets'].iloc[0]
        assets_prev = data_neraca.loc['Total Assets'].iloc[1]
        metrics['Total Assets'] = {
            'value': assets_current,
            'diff': ((assets_current - assets_prev) / assets_prev * 100)
        }
        
        # Total Liabilities
        liabilities_current = data_neraca.loc['Total Liabilities Net Minority Interest'].iloc[0]
        liabilities_prev = data_neraca.loc['Total Liabilities Net Minority Interest'].iloc[1]
        metrics['Total Liabilities'] = {
            'value': liabilities_current,
            'diff': ((liabilities_current - liabilities_prev) / liabilities_prev * 100)
        }
        
        # Total Equity
        equity_current = data_neraca.loc['Total Equity Gross Minority Interest'].iloc[0]
        equity_prev = data_neraca.loc['Total Equity Gross Minority Interest'].iloc[1]
        metrics['Total Equity'] = {
            'value': equity_current,
            'diff': ((equity_current - equity_prev) / equity_prev * 100)
        }
        
        # Revenue
        revenue_current = data_laba.loc['Operating Revenue'].iloc[0]
        revenue_prev = data_laba.loc['Operating Revenue'].iloc[1]
        metrics['Revenue'] = {
            'value': revenue_current,
            'diff': ((revenue_current - revenue_prev) / revenue_prev * 100)
        }
        
        # Cash and Cash Equivalents
        cash_current = data_neraca.loc['Cash And Cash Equivalents'].iloc[0]
        cash_prev = data_neraca.loc['Cash And Cash Equivalents'].iloc[1]
        metrics['Cash'] = {
            'value': cash_current,
            'diff': ((cash_current - cash_prev) / cash_prev * 100)
        }
        
        # Capital Expenditure
        capex_current = data_arus.loc['Capital Expenditure'].iloc[0]
        capex_prev = data_arus.loc['Capital Expenditure'].iloc[1]
        metrics['Capital Expenditure'] = {
            'value': capex_current,
            'diff': ((capex_current - capex_prev) / capex_prev * 100)
        }
        
        # Outstanding Shares
        shares = data_neraca.loc['Ordinary Shares Number'].iloc[0]
        metrics['Outstanding Shares'] = {
            'value': shares,
            'diff': None  # No difference calculation for shares
        }
        
    except Exception as e:
        st.error(f"Error calculating financial metrics: {str(e)}")
        
    return metrics

def show_enhanced_financial_details(ticker):
    st.header("Financial Details")
    
    # Get stock data
    saham = yf.Ticker(ticker)
    
    # Get financial statements
    data_neraca = saham.quarterly_balance_sheet
    data_laba = saham.quarterly_income_stmt
    data_arus = saham.quarterly_cash_flow
    
    # Calculate detailed metrics
    metrics = calculate_detailed_metrics(data_neraca, data_laba, data_arus)
    
    # Create tabs for different metric categories
    tab1, tab2, tab3 = st.tabs(["Basic Financials", "Performance Metrics", "Price Chart"])
    
    with tab1:
        col1, col2, col3 = st.columns(3)
        
        # Balance Sheet Metrics
        with col1:
            st.markdown("##### Balance Sheet Metrics")
            for metric in ['Total Assets', 'Total Liabilities', 'Total Equity']:
                if metric in metrics:
                    st.metric(
                        metric,
                        f"{metrics[metric]['value']:,.2f}",
                        f"{metrics[metric]['diff']:.2f}%"
                    )
        
        # Income Statement Metrics
        with col2:
            st.markdown("##### Income Statement Metrics")
            for metric in ['Revenue', 'Net Income', 'EPS']:
                if metric in metrics:
                    st.metric(
                        metric,
                        f"{metrics[metric]['value']:,.2f}",
                        f"{metrics[metric]['diff']:.2f}%"
                    )
        
        # Cash Flow Metrics
        with col3:
            st.markdown("##### Cash Flow Metrics")
            for metric in ['Cash', 'Capital Expenditure']:
                if metric in metrics:
                    st.metric(
                        metric,
                        f"{metrics[metric]['value']:,.2f}",
                        f"{metrics[metric]['diff']:.2f}%"
                    )
    
    with tab2:
        col1, col2 = st.columns(2)
        
        # Profitability Metrics
        with col1:
            st.markdown("##### Profitability Metrics")
            for metric in ['ROA', 'ROE', 'Net Margin']:
                if metric in metrics:
                    st.metric(
                        metric,
                        f"{metrics[metric]['value']*100:.2f}%",
                        f"{metrics[metric]['diff']:.2f}%"
                    )
        
        # Efficiency and Leverage Metrics
        with col2:
            st.markdown("##### Efficiency & Leverage Metrics")
            for metric in ['Asset Turnover', 'DER', 'BVPS']:
                if metric in metrics:
                    st.metric(
                        metric,
                        f"{metrics[metric]['value']:.2f}",
                        f"{metrics[metric]['diff']:.2f}%"
                    )
    
    with tab3:
        # Show price charts
        show_enhanced_stock_chart(ticker)

def show_enhanced_stock_chart(ticker):
    # Get stock data for different time periods
    stock = yf.Ticker(ticker)
    periods = {
        'Day': '1d',
        '5 Days': '5d',
        '1 Month': '1mo',
        '3 Months': '3mo',
        '6 Months': '6mo',
        '1 Year': '1y',
        '2 Year': '2y',
        '5 Year': '5y',
        'YTD': 'ytd',
        'Max': 'max'
    }
    
    selected_period = st.selectbox('Select Time Period', list(periods.keys()))
    
    data = stock.history(period=periods[selected_period])
    
    # Create candlestick chart
    fig = go.Figure()
    
    fig.add_trace(go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name='OHLC'
    ))
    
    # Add volume bars
    fig.add_trace(go.Bar(
        x=data.index,
        y=data['Volume'],
        name='Volume',
        yaxis='y2',
        marker_color='rgba(0,0,0,0.2)'
    ))
    
    # Update layout for dual axis
    fig.update_layout(
        title=f'{ticker} Stock Price and Volume ({selected_period})',
        yaxis_title='Price',
        yaxis2=dict(
            title='Volume',
            overlaying='y',
            side='right'
        ),
        xaxis_title='Date',
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)


if __name__ == '__main__':
    main()
