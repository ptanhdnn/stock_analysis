import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from vnstock import *

class TechniqueAnalysis():
    def __init__(self, data) -> None:
        self.data = data
        self.data = pd.DataFrame(data)

    def plot(self):
        pass

class Ichimoku(TechniqueAnalysis):
    def __init__(self, data) -> None:
        super().__init__(data)

    def calculateComponent(self):
        # Tenkan-sen (Conversion Line)
        period9_high = self.data['high'].rolling(window=9).max()
        period9_low = self.data['low'].rolling(window=9).min()
        self.data['Tenkan-sen'] = (period9_high + period9_low) / 2

        # Kijun-sen (Base Line)
        period26_high = self.data['high'].rolling(window=26).max()
        period26_low = self.data['low'].rolling(window=26).min()
        self.data['Kijun-sen'] = (period26_high + period26_low) / 2

        # Senkou Span A (Leading Span A)
        self.data['Senkou Span A'] = ((self.data['Tenkan-sen'] + self.data['Kijun-sen']) / 2).shift(26)

        # Senkou Span B (Leading Span B)
        period52_high = self.data['high'].rolling(window=52).max()
        period52_low = self.data['low'].rolling(window=52).min()
        self.data['Senkou Span B'] = ((period52_high + period52_low) / 2).shift(26)

        # Chikou Span (Lagging Span)
        self.data['Chikou Span'] = self.data['close'].shift(-26)

    def plot(self):
        # Plotting the Ichimoku Cloud
        plt.figure(figsize=(12, 6))
        plt.plot(self.data.index, self.data['close'], label='Close Price', color='black')
        plt.plot(self.data.index, self.data['Tenkan-sen'], label='Tenkan-sen', color='blue')
        plt.plot(self.data.index, self.data['Kijun-sen'], label='Kijun-sen', color='red')
        plt.fill_between(self.data.index, self.data['Senkou Span A'], self.data['Senkou Span B'], where=self.data['Senkou Span A'] >= self.data['Senkou Span B'], color='lightgreen', alpha=0.5)
        plt.fill_between(self.data.index, self.data['Senkou Span A'], self.data['Senkou Span B'], where=self.data['Senkou Span A'] < self.data['Senkou Span B'], color='lightcoral', alpha=0.5)
        plt.plot(self.data.index, self.data['Chikou Span'], label='Chikou Span', color='purple', linestyle='--')

        plt.title('Ichimoku Cloud')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.grid(True)
        plt.show()


