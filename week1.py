import pandas as pd
import matplotlib.pyplot as plt
x= list(pd.read_excel("week1task.xlsx")['log Y'])
y = list(pd.read_excel("week1task.xlsx")['log x'])
plt.figure()
plt.style.use('seaborn')
plt.scatter(x,y,marker=".",s=100,edgecolors="black",c="yellow")
plt.title("Excel sheet to Scatter Plot")
plt.show()
