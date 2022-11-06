import matplotlib.pyplot as plt
import pandas as pd

class TimeLapsePlot:

    @staticmethod
    def label_tracing(file):
        data = pd.read_csv(file)
        data = data[["text"] + data.columns[-1:"date"]]
        return data
    
    @staticmethod
    def match_tracing(file):
        return

class StatisticsPrinter:

    @staticmethod
    def label_summary():
        return

    @staticmethod
    def match_summary():
        return