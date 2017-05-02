#! /usr/bin/env python

import numpy as np

filename = 'DireStraits-BrothersInArms.wav'


if __name__ == "__main__":
    for bandEnd in np.arange(1000, 20000, 1000):
        for sil_len in np.arange(2, 20, 1):
            for thr in np.arange(0.1, 0.9, 0.02):
                for window in np.arange(0.02, 0.2, 0.02):
                    for median_filter in [True, False]:
                        out = str(bandEnd) + '_' + str(sil_len) + '_' + str(thr) + '_' + \
                              str(window) + '_' + str(median_filter) + '.txt'
                        median = '--median-filter' if median_filter is True else '--no-median-filter'
                        print './nogui.py', '--input-file', filename, '--output-file', out, '--band-end', bandEnd, \
                              '--silence-len', sil_len, '--threshold', thr, '--window', window, median
