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
        self.sample_window = 0.02
        self.sample_overlap = 0.01
        self.speech_window = 0.5
        self.speech_start_band = 300
        self.speech_end_band = 3000

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
        detected_sil = np.array([])
        sample_window = int(self.bitrate * self.sample_window)
        sample_overlap = int(self.bitrate * self.sample_overlap)
        data = self.data
        sample_start = 0
        start_band = self.speech_start_band
        end_band = self.speech_end_band
        data_len = len(data)
        while sample_start < (data_len - sample_window):
            sample_end = sample_start + sample_window
            if sample_end >= data_len:
                sample_end = data_len - 1
            data_window = data[sample_start:sample_end]
            norm_ene = self.GetNormalizedEnergy(data_window)
            sum_voice_energy = VAD.ComputeBandEnergy(
                norm_ene, start_band, end_band)
            sum_full_energy = sum(norm_ene.values())
            speech_ratio = sum_voice_energy / sum_full_energy
            if speech_ratio < self.thr:
                detected_sil = np.append(
                    detected_sil, [sample_start, sample_end])
            sample_start += sample_overlap
        print detected_sil
        detected_sil = detected_sil.reshape(len(detected_sil) / 2, 2)
        print detected_sil
        # detected_windows[:,1] = self._smooth_speech_detection(detected_windows)
        # return detected_windows

    def GetNormalizedEnergy(self, audio_data):
        data_freq = VAD.ComputeFrequencies(audio_data, self.bitrate)
        data_energy = VAD.ComputeEnergy(audio_data)
        print data_freq.shape, data_energy.shape
        energy_freq = dict()
        for (i, freq) in enumerate(data_freq):
            if abs(freq) not in energy_freq:
                energy_freq[abs(freq)] = data_energy[i] * 2
        return energy_freq

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

