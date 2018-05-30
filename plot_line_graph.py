import csv
import matplotlib.pyplot as plt
import numpy as numpy
import pylab as pylab


with open('Results/simulated_anneal/hillclimber/sim_course_log3.csv', 'r') as f:
    score = []
    counter = 0
    reader = csv.reader(f)
    for row in reader:
        if counter == 1081:
            break
        if len(row) == 1:
            counter += 1
            score.append(int(row[0]))
    
    x = range(0, len(score))
    
    plt.plot(x, score, linewidth=0.99, alpha=1, color='b')
    # plt.gca().set_xscale('log')
    plt.gca().invert_yaxis()

    z = numpy.polyfit(x, score, 1)
    p = numpy.poly1d(z)
    pylab.plot(x,p(x),"r--")
    plt.show()


