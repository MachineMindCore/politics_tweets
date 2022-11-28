from analytics_prototype import FrecuencyPlot as fplt
import pandas as pd

path = r"data/{}/{}"
labels = ["cortes", "descortes"]
file2 = "petrogustavo_full_[Sergio-Fajardo-sergio_fajardo-ingeniero-Ingeniero-Rodolfo-ingrodolfohdez-Fico-FicoGutierrez-Federico]_[01-03-2022&19-06-2022].csv"
data2 = pd.read_csv(path.format("processed", file2))
groups2 = {
    "Petro": ["Gustavo", "petro", "Petro", "gustavopetro", "GustavoPetro", "gustavito", "gustavo"],
    "Rodolfo": ["Rodo", "Rodolfo", "rodolfo"],
}

fplt.group_evaluation(data2, groups2, labels=["cortes", "descortés"])