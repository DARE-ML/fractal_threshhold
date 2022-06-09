# -*- coding: utf-8 -*-
"""Untitled2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1oVpqyeXqMEYrlakzs1bDgjW4SMBlWgaP
"""

import sklearn.linear_model as sk
import time
import random
import math
import numpy as np
import matplotlib.pyplot as plt
import openpyxl
import pandas as pd
import math
from sklearn.model_selection import train_test_split
pd.set_option('mode.chained_assignment','raise')

#------------------------------------------------------------------------------
# Customization section:
initial_temperature = 100
cooling = 0.8  # cooling coefficient
number_variables = 4
upper_bounds = [800,2200,2300,2400]   
lower_bounds = [2, 5, 10,15]  
computing_time = 300 # second(s)

def least_square_value(A,B,a,b):
    sum=0
    for i in range(len(A)):
      sum = math.sqrt((B[i]-a*A[i]-b)*(B[i]-a*A[i]-b)) + sum
    return sum  
def objective_function(X):
    a=X[0]
    b=X[1]
    c=X[2]
    d=X[3]
    df = pd.read_csv('weeek2.csv')
    df1=df.iloc[1:math.floor(a),:]
    df_binary = df1[['log Y', 'log x']]
    df_binary.head()

    X_1 = np.array(df_binary['log Y']).reshape(-1, 1)
    y_1 = np.array(df_binary['log x']).reshape(-1, 1)
 
    df2=df.iloc[math.floor(a):math.floor(b),:]
    df_binary2 = df2[['log Y', 'log x']]
    df_binary2.head()

    x2 = np.array(df_binary2['log Y']).reshape(-1, 1)
    y1 = np.array(df_binary2['log x']).reshape(-1, 1)
  
    df3=df.iloc[math.floor(b):math.floor(c),:]
    df_binary3 = df3[['log Y', 'log x']]
    df_binary3.head()

    x3 = np.array(df_binary3['log Y']).reshape(-1, 1)
    y2 = np.array(df_binary3['log x']).reshape(-1, 1)

    # df4=df.iloc[math.floor(c):2410,:]
    # df_binary4 = df4[['log Y', 'log x']]
    # df_binary4.head()


    df4=df.iloc[math.floor(c):math.floor(d),:]
    df_binary4 = df4[['log Y', 'log x']]
    df_binary4.head()


    x4 = np.array(df_binary4['log Y']).reshape(-1, 1)
    y3 = np.array(df_binary4['log x']).reshape(-1, 1)

    df5=df.iloc[math.floor(d):2410,:]
    df_binary5 = df5[['log Y', 'log x']]
    df_binary5.head()

    x5 = np.array(df_binary4['log Y']).reshape(-1, 1)
    y4 = np.array(df_binary4['log x']).reshape(-1, 1)

    lr1 = sk.LinearRegression();
    lr1.fit(X_1,y_1)
    lr2 = sk.LinearRegression();
    lr2.fit(x2,y1)
    lr3 = sk.LinearRegression();
    lr3.fit(x3,y2)
    lr4 = sk.LinearRegression();

    lr4.fit(x4,y3)
    lr5 = sk.LinearRegression();

    lr5.fit(x4,y3)
   # value = (least_square_value(X_1,y_1,lr1.coef_[0],lr1.intercept_)+least_square_value(x2,y1,lr2.coef_[0],lr2.intercept_)+least_square_value(x3,y2,lr3.coef_[0],lr3.intercept_)+least_square_value(x4,y3,lr4.coef_[0],lr4.intercept_))
    value = (least_square_value(X_1,y_1,lr1.coef_[0],lr1.intercept_)+least_square_value(x2,y1,lr2.coef_[0],lr2.intercept_)+least_square_value(x3,y2,lr3.coef_[0],lr3.intercept_)+least_square_value(x4,y3,lr4.coef_[0],lr4.intercept_)+least_square_value(x5,y4,lr5.coef_[0],lr5.intercept_))

    return value
  
#------------------------------------------------------------------------------
# Simulated Annealing Algorithm:
initial_solution=np.zeros((number_variables))
for v in range(number_variables):
   initial_solution[v] = random.uniform(lower_bounds[v],upper_bounds[v])

for v in range(number_variables):   
          
            while(initial_solution[v]<=1+initial_solution[v-1] and v>=1):
                  initial_solution[v] = random.uniform(lower_bounds[v],upper_bounds[v])

      
current_solution = initial_solution
best_solution = initial_solution
min_solution = initial_solution
n = 1  # no of solutions accepted
best_fitness = objective_function(best_solution)
min_fitness = best_fitness
current_temperature = initial_temperature # current temperature
start = time.time()
no_attempts = 1000 # number of attempts in each level of temperature
record_best_fitness =[]
  
for i in range(25):
  for j in range(no_attempts):
          accept=False
          for k in range(number_variables):
              current_solution[k] = best_solution[k] + 0.01*(random.uniform(lower_bounds[k],upper_bounds[k]))-0.01*(random.uniform(lower_bounds[k],upper_bounds[k]))
              current_solution[k] = max(min(current_solution[k],upper_bounds[k]),lower_bounds[k])
          for k in range(number_variables):   
            
              while(current_solution[k]<=1+current_solution[k-1] and k>=1):
                current_solution[k] = best_solution[k] + 0.01*(random.uniform(lower_bounds[k],upper_bounds[k]))-0.01*(random.uniform(lower_bounds[k],upper_bounds[k]))
                current_solution[k] = max(min(current_solution[k],upper_bounds[k]),lower_bounds[k])

          current_fitness = objective_function(current_solution)
          E = abs(current_fitness-best_fitness)  
          if current_fitness<min_fitness:
            min_solution = current_solution
            min_fitness = current_fitness
          if i==0 and j==0:
              EA=E
            

          if current_fitness>best_fitness:
              p = math.exp(-E/(EA*current_temperature))    

              if random.random()<p:
                  accept = True
              else:
                  accept = False

          else:
              accept = True
            
          if accept == True:
              best_solution = current_solution
              best_fitness = objective_function(best_solution)
              n = n + 1
              EA = (EA*(n-1)+E)/n
          print('interation:{},min_solution:{},best_fitness: {}'.format(j,min_solution,best_fitness))        
  record_best_fitness.append(best_fitness)
  current_temperature=current_temperature*cooling
  end = time.time()
  #if end-start >= computing_time:
   #  break
DF = pd.read_csv('weeek2.csv')
DF1=DF[1:math.floor(min_solution[0])]
DF_binary = DF1[['log Y', 'log x']]
DF_binary.head()

X = np.array(DF_binary['log Y']).reshape(-1, 1)
y = np.array(DF_binary['log x']).reshape(-1, 1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25)
regr = sk.LinearRegression()
regr.fit(X_train, y_train)
print(regr.coef_)


y_pred = regr.predict(X_test)
plt.scatter(X_test, y_test, color ='b')
plt.plot(X_test, y_pred, color ='pink')

DF2=DF[math.floor(min_solution[0]):math.floor(min_solution[1])]
DF_binary2 = DF2[['log Y', 'log x']]
DF_binary2.head()

x2 = np.array(DF_binary2['log Y']).reshape(-1, 1)
y1 = np.array(DF_binary2['log x']).reshape(-1, 1)

x2_train, x2_test, y1_train, y1_test = train_test_split(x2, y1, test_size = 0.25)
regr = sk.LinearRegression()

regr.fit(x2_train, y1_train)

y1_pred = regr.predict(x2_test)
plt.scatter(x2_test, y1_test, color ='b')
plt.plot(x2_test, y1_pred, color ='yellow')

DF3=DF[math.floor(min_solution[1]):math.floor(min_solution[2])]
DF_binary2 = DF3[['log Y', 'log x']]
DF_binary2.head()

x3 = np.array(DF_binary2['log Y']).reshape(-1, 1)
y2 = np.array(DF_binary2['log x']).reshape(-1, 1)

x3_train, x3_test, y2_train, y2_test = train_test_split(x3, y2, test_size = 0.25)
regr = sk.LinearRegression()
regr.fit(x3_train, y2_train)


y2_pred = regr.predict(x3_test)
plt.scatter(x3_test, y2_test, color ='b')
plt.plot(x3_test, y2_pred, color ='k')

# DF4=DF[math.floor(min_solution[2]):2450]
# DF_binary2 = DF4[['log Y', 'log x']]
# DF_binary2.head()

DF4=DF[math.floor(min_solution[2]):math.floor(min_solution[3])]
DF_binary2 = DF4[['log Y', 'log x']]
DF_binary2.head()

x4 = np.array(DF_binary2['log Y']).reshape(-1, 1)
y3 = np.array(DF_binary2['log x']).reshape(-1, 1)

x4_train, x4_test, y3_train, y3_test = train_test_split(x4, y3, test_size = 0.25)
regr = sk.LinearRegression()
regr.fit(x4_train, y3_train)


y3_pred = regr.predict(x4_test)
plt.scatter(x4_test, y3_test, color ='b')
plt.plot(x4_test, y3_pred, color ='red')

DF5=DF[math.floor(min_solution[3]): 2410]
DF_binary5 = DF5[['log Y', 'log x']]
DF_binary5.head()

x5 = np.array(DF_binary5['log Y']).reshape(-1, 1)
y4 = np.array(DF_binary5['log x']).reshape(-1, 1)

x5_train, x5_test, y4_train, y4_test = train_test_split(x5, y4, test_size = 0.25)
regr = sk.LinearRegression()
regr.fit(x5_train, y4_train)


y4_pred = regr.predict(x5_test)
plt.scatter(x5_test, y4_test, color ='b')
plt.plot(x5_test, y4_pred, color ='green')
# xx = np.linspace(-5,5,100)
# yy = -0.032*xx+3.4
# plt.plot(xx, yy, '-r', label='y=2x+1')
# plt.title('Graph of y=2x+1')
# plt.xlabel('x', color='#1C2833')
# plt.ylabel('y', color='#1C2833')
# plt.legend(loc='upper left')
# plt.grid()
# plt.show()
  
  
  
plt.show()