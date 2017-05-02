#! /usr/bin/env python

import argparse
from vad import VAD
from main import EditForm

original = [[1, '00:00:00', '00:04:00'],
            [2, '00:04:17', '00:11:00'],
            [3, '00:11:09', '00:15:10'],
            [4, '00:15:16', '00:19:45'],
            [5, '00:19:57', '00:25:10'],
            [6, '00:25:22', '00:32:06'],
            [7, '00:32:20', '00:36:55'],
            [8, '00:37:00', '00:40:31'],
            [9, '00:40:42', '00:47:24']]

resulttt = [[1, '00:00:00', '00:04:03'],
            [2, '00:04:11', '00:11:04'],
            [3, '00:11:10', '00:15:14'],
            [4, '00:15:17', '00:19:49'],
            [5, '00:19:58', '00:25:08'],
            [6, '00:25:25', '00:32:04'],
            [7, '00:32:21', '00:36:56'],
            [8, '00:37:01', '00:40:31'],
            [9, '00:40:43', '00:47:29']]


def cost_function(output, f):
    diff_sum = 0
    for i in range(len(output)):
        start = output[i][2]
        end = output[i][3]
        start_orig = original[i][1]
        end_orig = original[i][2]
        h, m, s = EditForm.ParseTime(start)
        sec_start_out = h * 3600 + m * 60 + s
        h, m, s = EditForm.ParseTime(end)
        sec_end_out = h * 3600 + m * 60 + s
        h, m, s = EditForm.ParseTime(start_orig)
        sec_start_orig = h * 3600 + m * 60 + s
        h, m, s = EditForm.ParseTime(end_orig)
        sec_end_orig = h * 3600 + m * 60 + s
        diff_sum += abs(sec_start_orig - sec_start_out) + abs(sec_end_orig - sec_end_out)
        f.write('Start diff: ' + str(abs(sec_start_orig - sec_start_out)) +
                ', end diff: ' + str(abs(sec_end_orig - sec_end_out)) + '\n')
    f.write('Diff sum: ' + str(diff_sum) + '\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Music detector without GUI")
    parser.add_argument('--input-file', action='store', dest='filename', type=str, required=True)
    parser.add_argument('--output-file', action='store', dest='output', type=str, required=True)
    parser.add_argument('--band-end', action='store', dest='band_end', type=int, required=True)
    parser.add_argument('--silence-len', action='store', dest='sil_len', type=int, required=True)
    parser.add_argument('--threshold', action='store', dest='thr', type=float, required=True)
    parser.add_argument('--window', action='store', dest='window', type=float, required=True)
    parser.add_argument('--median-filter', action='store_true', dest='median', required=False)
    parser.add_argument('--no-median-filter', action='store_false', dest='median', required=False)
    r = parser.parse_args()

    vad = VAD()

    bandStart = 50
    vad.music_start_band = bandStart

    minSongLen = 120
    vad.min_song_len = minSongLen

    vad.music_end_band = r.band_end

    vad.sil_len = r.sil_len

    vad.thr = r.thr

    vad.frame_window = r.window
    vad.frame_overlap = r.window / 2

    result = vad.ProcessFile(r.filename, r.median)
    if result is not None:
        if len(result) == len(original) or len(result) + 1 == len(original):
            f = open(r.output, 'w', 0)
            f.write('Length: ' + str(len(result)) + ', result: ' + str(result) + '\n')
            cost_function(result, f)
            f.close()
