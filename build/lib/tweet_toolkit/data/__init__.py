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
        plt.title(f"Conteo de etiquetas agrupadas: {FrecuencyHandle.extract_labels(labels)} {FrecuencyHandle.extract_users(data)}")
        ax.legend()
        plt.show()
        return 