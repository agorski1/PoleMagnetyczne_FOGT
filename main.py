from Kabel import Kabel
from MFieldVisualizer import MFieldVisualizer


kabel_prosty = Kabel(50, "spirala")

rysowanie = MFieldVisualizer(kabel_prosty.get_cable_structure())


rysowanie.addConesFromFile("spirala/coords.csv", "spirala/vectors.csv")
rysowanie.draw()

