import numpy as np
import scipy.io.wavfile as wf


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
        self.sil_len = None
        self.frame_window = 0.02
        self.frame_overlap = 0.01
        self.music_window = 0.5
        self.music_start_band = 50
        self.music_end_band = 3000

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
        self.inputFile = input_file
        self.thr = threshold
        self.sil_len = silence_len
        frame_window = int(self.bitrate * self.frame_window)
        frame_overlap = int(self.bitrate * self.frame_overlap)
        data = self.data
        frame_start = 0
        start_band = self.music_start_band
        end_band = self.music_end_band
        data_len = len(data)
        frames = []
        while frame_start < (data_len - frame_window):
            frame_end = frame_start + frame_window
            if frame_end >= data_len:
                frame_end = data_len - 1
            data_window = data[frame_start:frame_end]
            norm_ene = self.GetNormalizedEnergy(data_window)
            sum_voice_energy = VAD.ComputeBandEnergy(
                norm_ene, start_band, end_band)
            sum_full_energy = sum(norm_ene.values())
            speech_ratio = sum_voice_energy / sum_full_energy
            # print [frame_start, speech_ratio]
            # raw_input()
            frames = np.append(
                frames, [[frame_start, speech_ratio]])
            frame_start += frame_overlap
        frames = frames.reshape(len(frames) / 2, 2)
        print frames
        frames = self.ApplyMedianFilter(frames)
        return self.DetectSilence(frames)

    def DetectSilence(self, frames):
        sil_start = 0
        sil_amount = 0
        sil_frames = []
        print 'Frames shape', frames.shape
        for f in frames:
            # print 'Sil start', sil_start, 'Sil amount', sil_amount
            # raw_input()
            if f[1] < self.thr:
                print 'Under threshold', f
                if sil_start == 0:
                    sil_start = f[0] / self.bitrate
                else:
                    sil_amount += self.frame_overlap
            else:
                if sil_amount > self.sil_len:
                    sil_frames.append([sil_start, sil_amount])
                sil_start = 0
                sil_amount = 0
        # Check if there was silence at the end
        if sil_amount > self.sil_len:
            sil_frames.append([sil_start, sil_amount])
        return sil_frames

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
