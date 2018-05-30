import csv
from collections import Counter
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np

with open('Results/hillclimber/h_results7.csv', 'r') as f:
    values = []
    freq = []
    score = []

    reader = csv.reader(f)
    for row in reader:
        values.append(row[0])

    counts = Counter(values)
    for key in counts.keys():
        score.append(int(key))
    score = list(reversed(sorted(score)))

    highest_score = score[0]
    lowest_score = score[len(score) - 1]
    x = -lowest_score + highest_score + 1
    number = highest_score + 1
    score = []
    for i in range(x):
        number = number - 1
        score.append(number)

    for key in score:
        freq.append(counts[str(key)])

    y_pos = np.arange(len(score)) 
    plt.bar(y_pos, freq, align='center', alpha=0.75, color='r')
    plt.xticks(y_pos, score)
    plt.xlabel('Score')
    plt.ylabel('Frequentie')
    plt.title('Hillclimber')
    plt.show()