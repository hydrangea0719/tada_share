# coding: utf-8

import csv
import numpy as np
import matplotlib.pyplot as plt
import collections
from pprint import pprint


def main():
    
    file_input = 'bunpu1/csv/_20210713022703.csv'

    # 
    coin_N = []
    total_yen = []

    with open(file_input, mode='r') as f:
        
        # 1行目を飛ばす
        f.readline()

        reader = csv.reader(f)
        for line in reader:
            coin_N.append(int(line[4]))
            total_yen.append(int(line[5]))

    fig = plt.figure()

    ax = fig.add_subplot(1,1,1)
    ax.hist(coin_N, bins=10, align='mid')
    ax.set_xlabel('coin_N')
    ax.set_ylabel('freq')
    # plt.show()
    plt.close(fig)
    fig.savefig('hist_coin_N.png')

    c = collections.Counter(total_yen)
    c_sorted = sorted(c.items(), key=lambda x:x[0])
    pprint(c_sorted)
    
    num_bin = c_sorted[-1][0] - c_sorted[0][0]

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.hist(total_yen, bins=num_bin, align='mid')
    ax.set_xlabel('total_yen')
    ax.set_ylabel('freq')
    plt.close(fig)
    fig.savefig('hist_total_yen.png')

    c = collections.Counter(total_yen)
    c_sorted = sorted(c.items(), key=lambda x:x[0])
    pprint(c_sorted)





if __name__ == '__main__':
    main()

