import csv
from collections import Counter
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

with open('Results/hillclimber/h_results0.csv', 'r') as f:
    values = []
    freq = []
    score = []
    reader = csv.reader(f)
    for row in reader:
        values.append(row[0])

    counts = Counter(values)
    score = sorted(counts)
    lowest_score = score[len(score)-1]
    score = []
    number = 1
    for i in range(int(lowest_score[1]) + 3):
        number = number - 1
        score.append(number)
    for key in score:
        freq.append(counts[str(key)])
    print(score)
    print(freq)


y_pos = np.arange(len(score)) 
plt.bar(y_pos, freq, align='center', alpha=0.75, color='r')
plt.xticks(y_pos, score)
plt.xlabel('Score')
plt.ylabel('Frequentie')
plt.title('Hillclimber')
plt.show()