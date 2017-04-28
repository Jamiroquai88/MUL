import time
import multiprocessing
import os
import datetime
from joblib import Parallel, delayed
import numpy as np
import scipy.io.wavfile as wf


# def ProcessFilePart():

class VAD(object):
    ''' Voice activity detector.

    '''
    def __init__(self):
        ''' Class constructor.

        '''
        self.InitMembers()

    def InitMembers(self):
        ''' Re-init members.

        '''
        self.inputFile = None
        self.bitrate = None
        self.data = None
        self.thr = None
        self.length = None
        self.sil_len = None
        self.frame_window = 0.02
        self.frame_overlap = 0.01
        self.music_window = 0.5

    def ProcessFile(self, input_file, threshold, silence_len):
        ''' Process one wav file.

            :param input_file: path to input file
            :type input_file: str
            :param threshold: treshold for detecting silence
            :type threshold: float
            :param silence_len: length of silence for segmentation
            :type silence_len: float
            :returns: list of records, None otherwise
        '''
        try:
            self.bitrate, self.data = wf.read(input_file)
        except ValueError:
            return None
        self.channels = len(self.data.shape)
        print self.bitrate, self.data.shape, self.channels
        self.inputFile = str(input_file)
        self.thr = threshold
        self.length = self.data.shape[0] / self.bitrate
        print self.length
        self.sil_len = silence_len
        frame_window = int(self.bitrate * self.frame_window)
        frame_overlap = int(self.bitrate * self.frame_overlap)
        if self.channels == 1:
            data = self.data - np.mean(self.data)
        else:
            data = np.ndarray(self.data.shape)
            for ch in range(self.channels):
                data[:, ch] = self.data[:, ch] - np.mean(self.data[:, ch])
        frame_start = 0
        start_band = self.music_start_band
        end_band = self.music_end_band
        data_len = len(data)
        frames = []
        # num_cores = multiprocessing.cpu_count()
        # results = Parallel(n_jobs=num_cores)(delayed(ProcessFilePart)
        while frame_start < (data_len - frame_window):
            frame_end = frame_start + frame_window
            if frame_end >= data_len:
                frame_end = data_len - 1
            data_window = data[frame_start:frame_end]
            norm_ene = self.GetNormalizedEnergy(data_window)
            # print norm_ene
            # return
            sum_voice_energy = VAD.ComputeBandEnergy(
                norm_ene, start_band, end_band)
            # print norm_ene
            sum_full_energy = sum(norm_ene.values())
            # print sum_voice_energy, sum_full_energy
            # return
            speech_ratio = sum_voice_energy / sum_full_energy
            # print [frame_start, speech_ratio]
            # print [frame_start, max(speech_ratio)]
            # time.sleep(0.1)
            # raw_input()
            frames = np.append(
                frames, [frame_start, np.max(speech_ratio)])
            frame_start += frame_overlap
        frames = frames.reshape(len(frames) / 2, 2)
        print frames
        # frames = self.ApplyMedianFilter(frames)
        return self.DetectSongs(frames)

    def DetectSongs(self, frames):
        sil_start = 0
        sil_amount = 0
        sil_frames = []
        n_sil = 0
        print 'Frames shape', frames.shape
        for f in frames:
            # print 'Sil start', sil_start, 'Sil amount', sil_amount, f
            # time.sleep(0.1)
            if f[1] < self.thr:
                # print 'Under threshold', f
                if sil_start == 0:
                    sil_start = f[0] / self.bitrate
                else:
                    sil_amount += self.frame_overlap
            else:
                if sil_amount > self.sil_len:
                    sil_frames.append([n_sil, sil_start, sil_amount])
                    n_sil += 1
                sil_start = 0
                sil_amount = 0
        # Check if there was silence at the end
        if sil_amount > self.sil_len:
            sil_frames.append([n_sil, sil_start, sil_amount])
            n_sil += 1
        return VAD.ProcessSilence(
            sil_frames, self.min_song_len, os.path.basename(self.inputFile))

    @staticmethod
    def ProcessSilence(sil_seq, min_song_len, f):
        # to do
        print sil_seq
        songs_list = []
        k = 1
        start = 0
        for i in range(len(sil_seq)):
            # raw_input()
            sil_start = sil_seq[i][1]
            sil_len = sil_seq[i][2]
            print start, sil_start, sil_len
            if sil_start - start > min_song_len:
                songs_list.append([k, f.replace('.wav', '_' + str(k) + '.wav'),
                                   str(datetime.timedelta(seconds=int(start))),
                                   str(datetime.timedelta(seconds=int(sil_start)))])
                k += 1
            start = sil_start + sil_len
            # print 'Songs:', songs_list
        return songs_list

    def ApplyMedianFilter(self, frames):
        median_window = int(self.music_window / self.frame_window)
        if median_window % 2 == 0:
            median_window = median_window - 1
        frames[:, 1] = VAD.MedianFilter(frames[:, 1], median_window)
        print 'After median filter\n', frames
        return frames

    def GetNormalizedEnergy(self, audio_data):
        data_freq = VAD.ComputeFrequencies(audio_data, self.bitrate)
        data_energy = VAD.ComputeEnergy(audio_data)
        energy_freq = dict()
        for (i, freq) in enumerate(data_freq):
            if abs(freq) not in energy_freq:
                energy_freq[abs(freq)] = data_energy[i] * 2
        return energy_freq

    @staticmethod
    def MedianFilter(x, k):
        k2 = (k - 1) // 2
        y = np.zeros((len(x), k), dtype=x.dtype)
        y[:, k2] = x
        for i in range(k2):
            j = k2 - i
            y[j:, i] = x[:-j]
            y[:j, i] = x[0]
            y[:-j, -(i + 1)] = x[j:]
            y[-j:, -(i + 1)] = x[-1]
        return np.median(y, axis=1)

    @staticmethod
    def ComputeFrequencies(audio_data, bitrate):
        return np.fft.fftfreq(len(audio_data), 1.0 / bitrate)[1:]

    @staticmethod
    def ComputeEnergy(audio_data):
        return np.abs(np.fft.fft(audio_data))[1:] ** 2

    @staticmethod
    def ComputeBandEnergy(freq, start, end):
        sum_energy = 0
        for key in freq:
            if start < key < end:
                sum_energy += freq[key]
        return sum_energy
