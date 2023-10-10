from vnstock import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import locale
from datetime import datetime, time
import json
import Technique_analysis

# # Set the locale to the user's default
# locale.setlocale(locale.LC_ALL, '')

# def format_number(number):
#     return locale.format_string("%.1f", number, grouping=True)

# def invest_vol_df(df):
#   investor = ['SHEEP', 'WOLF', 'SHARK']
#   combine_dict = {}

#   for i in investor:
#       invest = df[df['investorType'] == i]
#       invest_buyOrder = invest[invest['orderType'] == 'Buy Up']
#       vol_invest_buyOrder = invest_buyOrder['volume'].sum()
#       invest_sellOrder = invest[invest['orderType'] == 'Sell Down']
#       vol_invest_sellOrder = invest_sellOrder['volume'].sum()

#       combine_dict.update({
#           f'{i}_Buy_Vol': vol_invest_buyOrder,
#           f'{i}_Sell_Vol': vol_invest_sellOrder,
#       })
#   return combine_dict

# with open("data_final.json", "r") as outfile: 
#     data_company = json.load(outfile)

# input = input("Chọn mã chứng khoán: ")
# stock_inday_df = stock_intraday_data(symbol=input, page_size=5000)

# combine_dict = invest_vol_df(stock_inday_df)
# investor_inday_df = pd.DataFrame([combine_dict])

# df_time_inday = pd.to_datetime(stock_inday_df['time'])
# df_time = df_time_inday.dt.time

# # Define the time bins
# time_morning = pd.date_range(start='09:00:00', end='11:30:00', freq='5T')
# time_afternoon = pd.date_range(start='13:00:00', end='15:00:00', freq='5T')
# time_bins = time_morning.append(time_afternoon)
# bins = [dt.time() for dt in time_bins]
# # print(df_time[32], df_time[33])

# start_index = []
# # cho chạy ngược từ trên xuống
# for i in range(len(bins)-1, 1, -1):
#   # print(f"in range {bins[i]} to {bins[i-1]}")
#   for j in range(len(df_time)-1):
#     if df_time[j] >= bins[i] and df_time[j + 1] < bins[i]:
#       # in ra giá trị đứng trước range
#       # ví dụ: trong range 10:30:00 - 10:25:00
#       # sẽ lấy ra giá trị 10:29:52 ứng với vị trí [j+1]
#       start_index.append(j+1)
#       # print(df_time[j+1], df_time[j])                  

# end_index = []
# for i in range(len(start_index) - 1):
#     end_index_time = start_index[i + 1]
#     end_index.append(end_index_time)

# end_index.append(len(df_time))

# pair_index = list(zip(start_index, end_index))

# range_time_dict = {}
# for start, end in pair_index:
#     selected_rows = stock_inday_df.iloc[start+1:end]
#     range_time_name = stock_inday_df.loc[start, 'time']
#     range_time_dict[range_time_name] = invest_vol_df(selected_rows)

# # Create a DataFrame from the dictionary
# result_df = pd.DataFrame(range_time_dict).T

# # Reset the index to make range_time_name a column
# result_df.reset_index(inplace=True)
# result_df.rename(columns={'index': 'range_time_name'}, inplace=True)
# print(result_df)

# buy_df = result_df.filter(like='_Buy_Vol')
# sell_df = result_df.filter(like='_Sell_Vol')

# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))  # Increase the width

# # Plot BUY volumes on the first subplot
# buy_df.plot(kind='line', marker='o', title='Vol mua theo tgian', ax=ax1)
# ax1.set_xlabel('Thời gian')
# ax1.set_ylabel('Vol')
# ax1.tick_params(axis='x', rotation=0)  # Set rotation to 0 degrees
# ax1.set_xticks(range(len(result_df)))
# ax1.set_xticklabels(result_df['range_time_name'], rotation=45)  # Use range_time_name as x-axis labels

# # Plot SELL volumes on the second subplot
# sell_df.plot(kind='line', marker='o', title='Vol bán theo tgian', ax=ax2)
# ax2.set_xlabel('Thời gian')
# ax2.set_ylabel('Vol')
# ax2.tick_params(axis='x', rotation=0)  # Set rotation to 0 degrees
# ax2.set_xticks(range(len(result_df)))
# ax2.set_xticklabels(result_df['range_time_name'], rotation=45)  # Use range_time_name as x-axis labels

# fig.suptitle(f'Mã chứng khoán {input}')
# plt.tight_layout()
# plt.show()

# It's work
###########################################################
# hist_df = stock_historical_data("SSI", 
#                                 "2022-10-01", "2023-10-06", 
#                                 "1D", "stock")
# ichimoku = Technique_analysis.Ichimoku(hist_df)
# ichimoku.calculateComponent()
# ichimoku.plot()
############################################################

hist_df = stock_historical_data("SSI", 
                                "2023-03-09", "2023-10-09", 
                                "1D", "stock")
ichimoku = Technique_analysis.Ichimoku(hist_df)
ichimoku.calculateComponent()
ichimoku.plot()