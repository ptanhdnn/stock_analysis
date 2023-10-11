from vnstock import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import locale
from datetime import datetime, time
import json
# import Technique_analysis


class GetVolStock:
    def __init__(self, symbol):
        locale.setlocale(locale.LC_ALL, '')
        self.symbol = symbol

    @staticmethod
    def format_number(number):
        return locale.format_string("%.1f", number, grouping=True)

    @staticmethod
    def investor_vol_df(df):
        investor = ['SHEEP', 'WOLF', 'SHARK']
        combine_dict = {}

        for i in investor:
            invest = df[df['investorType'] == i]
            invest_buyOrder = invest[invest['orderType'] == 'Buy Up']
            vol_invest_buyOrder = invest_buyOrder['volume'].sum()
            invest_sellOrder = invest[invest['orderType'] == 'Sell Down']
            vol_invest_sellOrder = invest_sellOrder['volume'].sum()

            combine_dict.update({
                f'{i}_Buy_Vol': vol_invest_buyOrder,
                f'{i}_Sell_Vol': vol_invest_sellOrder,
            })
        return combine_dict

    def analyzeStockVol(self):
    
        stock_inday_df = stock_intraday_data(symbol=self.symbol, page_size=5000)

        combine_dict = self.investor_vol_df(stock_inday_df)
        # investor_inday_df = pd.DataFrame([combine_dict])
        print(combine_dict)

        df_time_inday = pd.to_datetime(stock_inday_df['time'], format='%H:%M:%S')
        df_time = df_time_inday.dt.time

        time_morning = pd.date_range(start='09:00:00', end='11:30:00', freq='5T')
        time_afternoon = pd.date_range(start='13:00:00', end='15:00:00', freq='5T')
        time_bins = time_morning.append(time_afternoon)
        bins = [dt.time() for dt in time_bins]

        start_index = []
        for i in range(len(bins) - 1, 1, -1):
            for j in range(len(df_time) - 1):
                if df_time[j] >= bins[i] and df_time[j + 1] < bins[i]:
                    start_index.append(j + 1)

        end_index = []
        for i in range(len(start_index) - 1):
            end_index_time = start_index[i + 1]
            end_index.append(end_index_time)

        end_index.append(len(df_time))

        pair_index = list(zip(start_index, end_index))

        range_time_dict = {}
        for start, end in pair_index:
            selected_rows = stock_inday_df.iloc[start + 1:end]
            range_time_name = stock_inday_df.loc[start, 'time']
            range_time_dict[range_time_name] = self.investor_vol_df(selected_rows)

        result_df = pd.DataFrame(range_time_dict).T

        result_df.reset_index(inplace=True)
        result_df.rename(columns={'index': 'range_time_name'}, inplace=True)
        print(result_df)
        self.plot_stock_data(result_df, self.symbol)

    def getTotalVolInvestor(self):
        stock_inday_df = stock_intraday_data(symbol=self.symbol, page_size=5000)
        return stock_inday_df
    
    def plot_stock_data(self, result_df, symbol):
        buy_df = result_df.filter(like='_Buy_Vol')
        sell_df = result_df.filter(like='_Sell_Vol')

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6), sharey=True)

        buy_df.plot(kind='line', marker='o', title='Vol mua theo thời gian', ax=ax1)
        ax1.set_xlabel('Thời gian')
        ax1.set_ylabel('Vol')
        ax1.tick_params(axis='x', rotation=90)  # Rotate x-axis tick labels to 90 degrees
        ax1.set_xticks(range(len(result_df)))
        ax1.set_xticklabels(result_df['range_time_name'], rotation=90)

        sell_df.plot(kind='line', marker='o', title='Vol bán theo thời gian', ax=ax2)
        ax2.set_xlabel('Thời gian')
        ax2.set_ylabel('Vol')
        ax2.tick_params(axis='x', rotation=90)  # Rotate x-axis tick labels to 90 degrees
        ax2.set_xticks(range(len(result_df)))
        ax2.set_xticklabels(result_df['range_time_name'], rotation=90)

        fig.suptitle(f'Mã chứng khoán {symbol}')
        plt.tight_layout()
        plt.show()

analyzer = GetVolStock("PVD")
stock_data = analyzer.analyzeStockVol()
# volDay_dict = analyzer.investor_vol_df(volDay)
# print("______________________")
# print(volDay_dict)  



# It's work
###########################################################
# hist_df = stock_historical_data("SSI", 
#                                 "2022-10-01", "2023-10-06", 
#                                 "1D", "stock")
# ichimoku = Technique_analysis.Ichimoku(hist_df)
# ichimoku.calculateComponent()
# ichimoku.plot()
############################################################

# with open("data_final.json") as dataFile:
#     companyData = json.load(dataFile)
# # Có tổng cộng 143 công ty

# stock_data_day = {}
# bankList = companyData['Ngân hàng']

# for i, bankName in enumerate(bankList):
#     bank = GetVolStock(bankName)
#     bankVolInvestor = bank.getTotalVolInvestor()
#     bankInvestorVol = bank.investor_vol_df(bankVolInvestor)
    
#     stock_data_day[bankName] = bankInvestorVol
#     print(stock_data_day[bankName])


