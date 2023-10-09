from vnstock import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import locale
from datetime import datetime, time

# Set the locale to the user's default
locale.setlocale(locale.LC_ALL, '')

def format_number(number):
    return locale.format_string("%.1f", number, grouping=True)

def invest_vol_df(df):
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

input = input("Chọn mã chứng khoán: ")
stock_inday_df = stock_intraday_data(symbol=input, page_size=5000)
combine_dict = invest_vol_df(stock_inday_df)
investor_inday_df = pd.DataFrame([combine_dict])

company_df = listing_companies()
prefix_to_remove = "FU"
df = company_df[~(company_df['ticker'].str.startswith('FU') | company_df['ticker'].str.startswith('E1V'))]

companyName = df.ticker
hist_df = stock_historical_data("VNINDEX", "2023-10-01", "2023-10-06", "15", 'index')

uniqueIndustry = pd.unique(df.industry)

group_df = df[['ticker', 'industry']]
grouped = group_df.groupby(group_df['industry'])
industry_dict = {industry: group['ticker'].to_list() for industry, group in grouped}
# print(industry_dict["Dịch vụ tài chính"])

df_time_inday = pd.to_datetime(stock_inday_df['time'])
df_time = df_time_inday.dt.time
# Define the time bins
time_morning = pd.date_range(start='09:00:00', end='11:30:00', freq='15T')
time_afternoon = pd.date_range(start='13:00:00', end='15:00:00', freq='15T')
time_bins = time_morning.append(time_afternoon)
bins = [dt.time() for dt in time_bins]
# print(df_time[32], df_time[33])

start_index = []
# cho chạy ngược từ trên xuống
for i in range(len(bins)-1, 1, -1):
  # print(f"in range {bins[i]} to {bins[i-1]}")
  for j in range(len(df_time)-1):
    if df_time[j] >= bins[i] and df_time[j + 1] < bins[i]:
      # in ra giá trị đứng trước range
      # ví dụ: trong range 10:30:00 - 10:25:00
      # sẽ lấy ra giá trị 10:29:52 ứng với vị trí [j+1]
      start_index.append(j+1)
      # print(df_time[j+1], df_time[j])                  
  # print("_______\n")

# print(start_index)
end_index = []
for i in range(len(start_index) - 1):
    # print(i, len(start_index))
    end_index_time = start_index[i + 1]
    end_index.append(end_index_time)

end_index.append(len(df_time))

pair_index = list(zip(start_index, end_index))
# print(end_index)
print(pair_index)
range_time_dict = {}
for start, end in pair_index:
    selected_rows = stock_inday_df.iloc[start+1:end]
    range_time_name = stock_inday_df.loc[start, 'time']
    range_time_dict[range_time_name] = invest_vol_df(selected_rows)
# Create a DataFrame from the dictionary
result_df = pd.DataFrame(range_time_dict).T

# Reset the index to make range_time_name a column
result_df.reset_index(inplace=True)
result_df.rename(columns={'index': 'range_time_name'}, inplace=True)

# Now, result_df is your desired DataFrame
# print(result_df)

# import matplotlib.pyplot as plt

# Create separate DataFrames for BUY and SELL volumes
buy_df = result_df.filter(like='_Buy_Vol')
sell_df = result_df.filter(like='_Sell_Vol')

# Create a figure with two subplots (1 row, 2 columns)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

# Plot BUY volumes on the first subplot
buy_df.plot(kind='line', marker='o', title='Vol mua theo tgian', ax=ax1)
ax1.set_xlabel('Tgian 15ph')
ax1.set_ylabel('Vol')
ax1.tick_params(axis='x', rotation=45)

# Plot SELL volumes on the second subplot
sell_df.plot(kind='line', marker='o', title='Vol bán theo tgian', ax=ax2)
ax2.set_xlabel('Tgian 15ph')
ax2.set_ylabel('Vol')
ax2.tick_params(axis='x', rotation=45)

fig.suptitle(f'Mã chứng khoán {input}')

# Adjust layout and display the subplots
plt.tight_layout()
plt.show()

