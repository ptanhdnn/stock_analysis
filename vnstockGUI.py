import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QFileDialog,
                             QHBoxLayout, QVBoxLayout, QLineEdit,
                             QComboBox, QPushButton, QTextBrowser, 
                             QMessageBox)
import pandas as pd
import matplotlib.pyplot as plt
from vnstock import stock_intraday_data

class VNStockApp(QWidget):
    def __init__(self):
        super().__init__()

        self.result_df = None
        self.stock_entered = None

        self.setWindowTitle("vnstock GUI")
        self.setGeometry(400, 100, 720, 720)

        self.line_edit = QLineEdit()
        self.combo_box = QComboBox()
        self.combo_box.addItems(["5 Min", "1 Day", "Default"])
        self.get_volume_btn = QPushButton("Lấy dữ liệu")
        self.plot_btn = QPushButton("Vẽ biểu đồ")
        self.export_btn = QPushButton("Xuất ra file Csv")

        self.line_edit.setPlaceholderText("Nhập mã chứng khoán tại đây...")

        self.text_browser = QTextBrowser()
        self.text_browser.setPlainText("In dữ liệu về các loại volume")
        self.detailCalculator_textBrowser = QTextBrowser()

        layout = QHBoxLayout()
        layout.addWidget(self.line_edit)
        layout.addWidget(self.combo_box)
        layout.addWidget(self.get_volume_btn)
        layout.addWidget(self.plot_btn)
        layout.addWidget(self.export_btn)

        vertical_layout = QVBoxLayout()
        vertical_layout.addLayout(layout)
        vertical_layout.addWidget(self.text_browser)
        vertical_layout.addWidget(self.detailCalculator_textBrowser)
        self.detailCalculator_textBrowser.setFixedHeight(250)

        self.get_volume_btn.clicked.connect(self.check_line_edit)
        self.get_volume_btn.clicked.connect(self.get_volume)  # Connect to get_volume method
        self.plot_btn.clicked.connect(self.check_plot_condition)
        self.export_btn.clicked.connect(self.export_file)

        self.setLayout(vertical_layout)

    def check_line_edit(self):
        if not self.line_edit.text():
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText("Nhập mã chứng khoán vào -_-")
            msg.setWindowTitle("Validation Error")
            msg.exec()

    def get_volume(self):
        time_selected = self.combo_box.currentText()
        self.stock_entered = self.line_edit.text().upper()
        stock_inday_df = stock_intraday_data(symbol=self.stock_entered, page_size=5000)

        df = pd.DataFrame(stock_inday_df)

        # Chuyển cột 'time' sang kiểu datetime
        df['time'] = pd.to_datetime(df['time'], format='%H:%M:%S').dt.time

        # Chia thành hai khoảng thời gian: buổi sáng và buổi chiều
        morning_df = df[(df['time'] >= pd.to_datetime('09:15:00', format='%H:%M:%S').time()) & (df['time'] <= pd.to_datetime('11:30:00', format='%H:%M:%S').time())]
        afternoon_df = df[(df['time'] >= pd.to_datetime('13:00:00', format='%H:%M:%S').time()) & (df['time'] <= pd.to_datetime('14:30:00', format='%H:%M:%S').time())]
        self.detail_calculator(stock_inday_df, morning_df, afternoon_df)

        if time_selected == "1 Day":
            combine_dict = self.investor_vol_df(stock_inday_df)
            self.result_df = pd.DataFrame([combine_dict])
            html_table = self.result_df.to_html(index=False, classes='table table-bordered table-striped')
            self.text_browser.setHtml(html_table)

        elif time_selected == "5 Min":
            df_time_inday = pd.to_datetime(stock_inday_df['time'], format='%H:%M:%S')
            df_time = df_time_inday.dt.time

            time_morning = pd.date_range(start='09:00:00', end='11:30:00', freq='5T')
            time_afternoon = pd.date_range(start='13:00:00', end='15:00:00', freq='5T')
            time_bins = time_morning.append(time_afternoon)
            bins = [dt.time() for dt in time_bins]

            pair_index = []
            for i in range(1, len(bins)):
                bin_start, bin_end = bins[i - 1], bins[i]
                selected_rows = stock_inday_df[(df_time >= bin_start) & (df_time < bin_end)]
                if not selected_rows.empty:
                    pair_index.append((selected_rows.index[0], selected_rows.index[-1] + 1))

            range_time_dict = {}
            for start, end in pair_index:
                selected_rows = stock_inday_df.iloc[start:end]
                range_time_name = stock_inday_df.loc[start, 'time']
                range_time_dict[range_time_name] = self.investor_vol_df(selected_rows)

            sorted_range_time_dict = dict(sorted(range_time_dict.items(), key=lambda item: item[0], reverse=True))

            self.result_df = pd.DataFrame(sorted_range_time_dict).T
            self.result_df.reset_index(inplace=True)
            self.result_df.rename(columns={'index': 'range_time_name'}, inplace=True)

            html_table = self.result_df.to_html(index=False, classes='table table-bordered table-striped')
            self.text_browser.setHtml(html_table)

        else:
            html_table = stock_inday_df.to_html(index=False)
            self.text_browser.setHtml(html_table)

    def check_plot_condition(self):
        if self.result_df is None:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText("Không có dữ liệu biểu đồ. Vui lòng lấy dữ liệu trước.")
            msg.setWindowTitle("Error")
            msg.exec()
        else:
            self.plot_stock_data()

    def investor_vol_df(self, df):
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

    def plot_stock_data(self):
        buy_df = self.result_df.filter(like='_Buy_Vol')
        sell_df = self.result_df.filter(like='_Sell_Vol')

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6), sharey=True)

        buy_df.plot(kind='line', marker='o', title='Vol mua theo thời gian', ax=ax1)
        ax1.set_xlabel('Thời gian')
        ax1.set_ylabel('Vol')
        ax1.tick_params(axis='x', rotation=90)
        ax1.set_xticks(range(len(self.result_df)))
        ax1.set_xticklabels(self.result_df['range_time_name'], rotation=90)

        sell_df.plot(kind='line', marker='o', title='Vol bán theo thời gian', ax=ax2)
        ax2.set_xlabel('Thời gian')
        ax2.set_ylabel('Vol')
        ax2.tick_params(axis='x', rotation=90)
        ax2.set_xticks(range(len(self.result_df)))
        ax2.set_xticklabels(self.result_df['range_time_name'], rotation=90)

        fig.suptitle(f'Mã chứng khoán {self.stock_entered}')
        plt.tight_layout()
        plt.show()

    def export_file(self):
        if self.result_df is None:
            # Kiểm tra dữ liệu result_df
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText("Không có dữ liệu để xuất. Vui lòng lấy dữ liệu trước.")
            msg.setWindowTitle("Error")
            msg.exec()
        else:
            file_dialog = QFileDialog()
            options = file_dialog.options()
            file_path, _ = file_dialog.getSaveFileName(self, "Save File", "", "Excel Files (*.xlsx);;All Files (*)", options=options)

            if file_path:
                self.result_df.to_excel(file_path, index=False)

    def detail_calculator(self, stock_inday_df, morning_df, afternoon_df):
        result_text = ""
        for time_df, time_period in zip([morning_df, afternoon_df], ["buổi sáng", "buổi chiều"]):
            for investor_type in ["SHARK", "WOLF"]:
                df_copy = time_df[time_df['investorType'] == investor_type].copy()
                buy_df = df_copy[df_copy['orderType'] == 'Buy Up']
                sell_df = df_copy[df_copy['orderType'] == 'Sell Down']

                total_value_buy = (buy_df['volume'] * buy_df['averagePrice']).sum()
                total_value_sell = (sell_df['volume'] * sell_df['averagePrice']).sum()
                total_volume_buy = buy_df['volume'].sum()
                total_volume_sell = sell_df['volume'].sum()

                max_price_buy = total_value_buy / total_volume_buy if total_volume_buy > 0 else 0
                max_price_sell = total_value_sell / total_volume_sell if total_volume_sell > 0 else 0

                result_text += f"Trong {time_period}:\n"
                result_text += f"{investor_type}\n"
                result_text += f"Mua: {total_value_buy:.2e},\tBán: {total_value_sell:.2e}\n"
                result_text += f"Giá mua tb: {max_price_buy:.2f},\tGiá bán tb: {max_price_sell:.2f}\n"
                result_text += "________________________________________________________________________\n"

                self.detailCalculator_textBrowser.setPlainText(result_text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VNStockApp()
    window.show()
    sys.exit(app.exec())
