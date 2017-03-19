import numpy as np
import scipy.io.wavfile as wf
import matplotlib.pyplot as plt

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
            self.channels = len(self.data.shape)
            print self.bitrate, self.data.shape, self.channels
            self.inputFile = input_file
            self.thr = threshold
            self.sil_len = silence_len
        except ValueError:
            return None
