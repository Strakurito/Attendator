import pickle
import openpyxl


class Excelator:
    def __init__(pracici, stavby):
        print("blorb")



PIKP = "Resources\Pracovnici.pkl"
PIKS = "Resources\Stavby.pkl"
with open(PIKP, "rb") as a:
    pracici = pickle.load(a)
with open(PIKS, "rb") as a:
    stavby = pickle.load(a)

excelator = Excelator()

