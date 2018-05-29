import matplotlib.pyplot as plt
import numpy as np

# import data with loadtxt, but only the relevant floats. 
# data.csv is the file as you have given it above
data = np.loadtxt('Results/hillclimber/h_results0.csv', delimiter=',', skiprows = 1, usecols = range(1,5))
data = data.transpose()

# import the tick labels
xt = np.loadtxt('Results/hillclimber/h.results0.csv', dtype='str', delimiter=',', skiprows = 1, usecols = (0,))

width = 0.45
ind = np.arange(11) + 0.75

fig, ax = plt.subplots(1,1)
p0 = ax.bar(ind, data[0],  width, color = 'cyan')
p1 = ax.bar(ind, data[1], width, bottom = data[0], color = 'violet')
p2 = ax.bar(ind, data[2], width, bottom = data[0] + data[1], color = 'g')
p3 = ax.bar(ind, data[3], width, bottom = data[0] + data[1] + data[2], color = 'r')

ax.set_ylabel('kWh')
ax.set_xlabel('month')
ax.set_xticks (ind + width/2.)
ax.set_xticklabels( xt, rotation = 70 )

fig.legend( (p0[0], p1[0], p2[0], p3[0]), ('kitchen', 'laundry', 'aircon&heater', 'other') )
fig.tight_layout()
fig.show()