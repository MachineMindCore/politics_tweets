import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime  as dt
class TimeLapsePlot:

    @staticmethod
    def label_tracing(file, labels):
        data = pd.read_csv(file)
        min_date = dt.datetime.strptime(min(data["date"]), "%Y-%m-%d")
        max_date = dt.datetime.strptime(max(data["date"]), "%Y-%m-%d")
        dates = np.arange(min_date, max_date, dt.timedelta(days=1)).astype(dt.datetime)
        points = np.zeros((len(labels), len(dates)))

        for l in range(len(labels)):
            i = 0
            for date in dates:
                points[l,i] = data[pd.to_datetime(data["date"]) == date][labels[l]].sum()
                i += 1
            plt.step(dates, points[l,:])
            plt.legend(labels)
            plt.xticks(rotation = 90)
        plt.show()
        return 
    
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