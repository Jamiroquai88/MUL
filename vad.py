import os
import datetime
from joblib import Parallel, delayed
import matplotlib.pyplot as plt
import numpy as np
import scipy.io.wavfile as wf


def ProcessFilePart(data, freq, start_band, end_band, window, overlap, i):
    """ Process part of wav file defined by parameters.
    
        :param data: input data
        :type data: numpy.array
        :param freq: input wav file frequency
        :type freq: int
        :param start_band: band start
        :type start_band: int
        :param end_band: band end
        :type end_band: int
        :param window: size of frame window
        :type window: float
        :param overlap: frame overlap
        :type overlap: float
        :param i: index of chunked data
        :type i: int
        :returns: processed frames
        :rtype: numpy.array
    """
    frames = []
    frame_start = 0
    data_len = len(data)
    while frame_start < (data_len - window):
        frame_end = frame_start + window
        if frame_end >= data_len:
            frame_end = data_len - 1
        data_window = data[frame_start:frame_end]
        norm_ene = VAD.GetNormalizedEnergy(data_window, freq)
        sum_voice_energy = VAD.ComputeBandEnergy(
            norm_ene, start_band, end_band)
        sum_full_energy = sum(norm_ene.values())
        speech_ratio = sum_voice_energy / sum_full_energy
        frames = np.append(
            frames, [frame_start + data_len * i, speech_ratio])
        frame_start += overlap
    return frames, i


class VAD(object):
    """ Voice activity detector.

    """
    def __init__(self):
        """ Class constructor.

        """
        self.inputFile = None
        self.bitrate = None
        self.data = None
        self.thr = None
        self.length = None
        self.sil_len = None
        self.channels = None
        self.music_start_band = None
        self.music_end_band = None
        self.min_song_len = None
        self.coresNum = None
        self.frame_window = 0.1
        self.frame_overlap = self.frame_window / 2
        self.music_window = 0.5

    def ProcessFile(self, input_file, median=False):
        """ Process one wav file.

            :param input_file: path to input file
            :type input_file: str
            :param median: use or do not use median filter
            :type median: bool
            :returns: list of records, None otherwise
            :rtype: list
        """
        try:
            self.bitrate, self.data = wf.read(input_file)
        except ValueError:
            return None
        self.channels = len(self.data.shape)
        self.inputFile = str(input_file)
        self.length = self.data.shape[0] / self.bitrate
        frame_window = int(self.bitrate * self.frame_window)
        frame_overlap = int(self.bitrate * self.frame_overlap)
        if self.channels == 2:
            data = np.mean(self.data, axis=1, dtype=self.data.dtype)
            self.channels = 1
        data = data - np.mean(self.data)
        start_band = self.music_start_band
        end_band = self.music_end_band
        num_cores = self.coresNum
        chunked_data = VAD.ChunkData(data, num_cores)
        frames = Parallel(n_jobs=num_cores)(
            delayed(ProcessFilePart)(
                ch, self.bitrate, start_band,
                end_band, frame_window, frame_overlap, i)
            for i, ch in chunked_data.items())
        frames = np.concatenate([x[0] for x in frames])
        frames = frames.reshape(len(frames) / 2, 2)
        if median:
            frames = self.ApplyMedianFilter(frames)
        # VAD.Plot(data, frames, self.bitrate * 20, self.bitrate, frame_window)
        return self.DetectSongs(frames)

    @staticmethod
    def Plot(data, frames, num, bitrate, window):
        """ Plot data.
        
        """
        # plt.figure(1)
        # plt.title('Wave')
        # plt.plot(data[:num])
        # plt.title('Energy')
        plt_frames = []
        for i in range(num):
            plt_frames.append(frames[i / window, 1])
        plt_frames = np.array(plt_frames)[:, np.newaxis]
        # plt.plot(data[:num])
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        x_plot = np.linspace(0, num, num)
        ax.plot(x_plot, plt_frames, 'r-', label="pdf")
        x_ticks = np.arange(0, num / bitrate, bitrate)
        ax.set_xticks(x_ticks)
        plt.show()

    def DetectSongs(self, frames):
        """ Detect songs in frames. Compare with threshold.
        
            :param frames: processed frames
            :type frames: numpy.array
            :returns: songs in list
            :rtype: list
        """
        sil_start = 0
        sil_amount = 0
        sil_frames = []
        n_sil = 0
        for f in frames:
            if f[1] < self.thr:
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
    def ChunkData(data, num_cores):
        """ Chunk data for parallel processing.
        
            :param data: input data
            :type data: numpy.array
            :param num_cores: number of cores
            :type num_cores: int
        """
        data_dict = {}
        chunks = np.split(data, num_cores)
        for i in range(num_cores):
            data_dict[i] = chunks[i]
        return data_dict

    @staticmethod
    def ProcessSilence(sil_seq, min_song_len, f):
        """ Process silence, find sequences with silence and detect songs.
        
            :param sil_seq: sequence of silence
            :type sil_seq: list
            :param min_song_len: minimal length of song
            :type min_song_len: int
            :param f: filename
            :type f: str
            :returns: list with songs
            :rtype: list
        """
        songs_list = []
        k = 1
        start = 0
        for i in range(len(sil_seq)):
            sil_start = sil_seq[i][1]
            sil_len = sil_seq[i][2]
            if sil_start - start > min_song_len:
                songs_list.append([k, f.replace('.wav', '_' + str(k) + '.wav'),
                                   str(datetime.timedelta(seconds=int(start))),
                                   str(datetime.timedelta(seconds=int(sil_start)))])
                k += 1
            start = sil_start + sil_len
        return songs_list

    def ApplyMedianFilter(self, frames):
        """ Apply median filter to frames.
        
            :param frames: processed frames
            :type frames: numpy.array
            :returns: filtered frames
            :rtype: numpy.array
        """
        median_window = int(self.music_window / self.frame_window)
        if median_window % 2 == 0:
            median_window = median_window - 1
        frames[:, 1] = VAD.MedianFilter(frames[:, 1], median_window)
        return frames

    @staticmethod
    def GetNormalizedEnergy(audio_data, bitrate):
        """ Compute normalized energy in data.
            
            :param audio_data: input data
            :type audio_data: numpy.array
            :param bitrate: bitrate
            :type bitrate: int
            :returns: normalized energy
            :rtype: list
        """
        data_freq = VAD.ComputeFrequencies(audio_data, bitrate)
        data_energy = VAD.ComputeEnergy(audio_data)
        energy_freq = dict()
        for (i, freq) in enumerate(data_freq):
            if abs(freq) not in energy_freq:
                energy_freq[abs(freq)] = data_energy[i] * 2
        return energy_freq

    @staticmethod
    def MedianFilter(x, k):
        """ Filter data with median filter.
        
            :param x: input data
            :type x: numpy.array
            :param k: filter size
            :type k: int
            :returns: filtered data
            :rtype: numpy.array
        """
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
        """ Compute frequencies by normalized frequency.
        
            :param audio_data: input data
            :type audio_data: numpy.array
            :param bitrate: input bitrate
            :type bitrate: int
            :returns: frequencies
            :rtype: numpy.array
        """
        return np.fft.fftfreq(len(audio_data), 1.0 / bitrate)[1:]

    @staticmethod
    def ComputeEnergy(audio_data):
        """ Compute energy in data.
        
            :param audio_data: input data
            :type audio_data: numpy.array
            :returns: energy in data
            :rtype: numpy.array
        """
        return np.abs(np.fft.fft(audio_data))[1:] ** 2

    @staticmethod
    def ComputeBandEnergy(freq, start, end):
        """ Compute energy in band.
        
            :param freq: frequency dict with energy
            :type freq: dict
            :param start: band start
            :type start: int
            :param end: band end
            :type end: int
            :returns: summed energy in band
            :rtype: float
        """
        sum_energy = 0
        for key in freq:
            if start < key < end:
                sum_energy += freq[key]
        return sum_energy
