import logging

import os
import numpy as np

import pickle5
from pickle5 import HIGHEST_PROTOCOL

import pyflac
import soundfile as sf

"""
This is meant a as a general audio processing pipeline and will be updated as I go. 
The environmental variables are set because this script is meant to be run on a high power computing cluster. 


TODO:
Allow for other audio file types to be read
Need to write encode the audio files as FLAC for NOW, will add options for other audio encodings

"""

# Removed rats with NA on them.


class AudioPipe:
    """
    This acts as a general audio processing pipe line it currently only requires a path to work.

    All writes to the self.writedir and read audio from the self.audiodir
    Class is centered around the workdir

    _getwritepath()       creates the path to write audio files to
    _getreaddir()         creates the path to read audio from
    getIDs()              creates list of acceptable files to read from
    _createAudioPathList  creates list of audio directory paths.
    _savePickle           saves Pickle of object to write directory
    _writeAudio           writes flac of sampled audio to write directory
    _sampleAudio1         samples only the first 5 minutes of the audio
    _sampleAudioS         samples the entire audio in sliding window format
    _processAudio         prepares the audio for sampling
    sampleAudio           begins to create samples of audio and writes them to write directory
    """

    def __init__(self, fp: str):
        self.workdir = fp
        self.writedir = self._getwritedir()
        self.readdir = self._getreaddir()

    def __str__(self):
        return "AudioPath"

    def __repr__(self):
        return "AudioPath Object"

    def _getwritedir(self):
        """get the dierctory to write to"""
        os.chdir(self.workdir)
        WORK_DIR_PATH = os.path.join(self.workdir, "5_min_samples")
        if not os.path.exists(WORK_DIR_PATH):
            os.mkdir(WORK_DIR_PATH)
            return WORK_DIR_PATH
        else:
            return WORK_DIR_PATH

    def _getreaddir(self):
        """get the directory to be read from"""
        os.chdir(self.workdir)
        READ_DIR_PATH = os.path.join(self.workdir, "audios")
        if not os.path.exists(READ_DIR_PATH):
            os.mkdir(READ_DIR_PATH)
            return READ_DIR_PATH
        else:
            return READ_DIR_PATH

    def getIDs(self, textPATH: str) -> tuple[list[str], list[str]]:
        """
        Reads the IDs of the rats from a txt file by line
        textPATH        This is the path to the text file can be anywhere
        """
        TMPPATH, fname = os.path.split(textPATH)

        os.chdir(TMPPATH)

        id_list = list()

        with open(fname, "r") as f:
            line = f.readline().strip()
            id_list.append(line)

        del id_list[0]  # header info.

        self.idlist = id_list

        audio_path_list = self._createAudioPathList(self.idlist)

        return id_list, audio_path_list

    def _createAudioPathList(self, id: list) -> list[str]:
        """Create a list of acceptable audio paths to be read from"""
        os.chdir(self.readdir)

        audio_path_list = list()
        # find the audios for each of the rats in the ids and return list element

        for dirpath, dirname, filenames in os.walk(self.readdir, topdown=True):
            os.chdir(dirpath)
            for name in filenames:
                if name in set(self.idlist):
                    audio_path_list.append(name)

        self.audiopathlist = audio_path_list

        return audio_path_list

    def _savePickle(self, var):
        """save dict as pickle"""

        name = "dictionary.pickle"
        name = os.path.join(self.writedir, name)

        with open(var, "wb") as fp:
            pickle5.dump(fp, f"{name}", HIGHEST_PROTOCOL)

    def _writeAudio(self, name: str, audio_buffer: np.ndarray, sr: int) -> None:
        os.chdir(self.writedir)

        try:
            sf.write(name, audio_buffer, sr)
            return None
        except Exception as e:
            logging.exception(e)

    def _sampleAudio1(self, audio: np.ndarray, sr: int) -> np.ndarray:
        """auxiliary function to sample only the first minute of audio"""
        fifthminute = sr * 5

        sampleFiveminutes = audio[0:fifthminute]

        return sampleFiveminutes

    def _sampleAudioS(self, audio: np.ndarray, sr: int) -> list:
        """
        Version of the auxiliary function that slides over the
        length of the audio in 5 minute sections returing a list of audio samples
        """
        length = len(audio)
        fiveminute = 5 * sr
        window_length = length // fiveminute
        num_slides = (window_length * 2) - 1
        samples = list()

        for n in range(num_slides):
            start = n * fiveminute
            stop = start + fiveminute

            samples.append(audio[start:stop])

        return samples

    # needs to work for other audio files i.e. wav, mp3, flac etc.
    def _processAudio(self, filename, option=None):
        """
        opens the FLAC file,
        save array of PMF and sample rate
        variable is saved as flac via copyAudio and wiritten
        """
        os.chdir(self.readdir)

        decoder = pyflac.FileDecoder(input_file=filename)
        array, sr = decoder.process()

        # Default is take take only the first sample
        if option == None:
            processed = self._sampleAudio1(array, sr)
        else:
            processed = self._sampleAudioS(array, sr)

        return array, sr, processed

    def sampleAudio(self) -> None:
        # open audio
        """
        This samples the audio files in the readdir and makes a copy of it using
        the auxiliary _processAudio and _sampleAudio1 or _sampleAudioS functions.
        Nothing is returned.

        The ID list parsed from the text file are used to check against the available
        files in the path list from the read directory. If it is found in the directory,
        Its name is saved and the name is passed to _processAudio and _writeAudio for
        additional processing.
        """
        processed = list()
        verified = list()

        #  clean each file path and save only the name of the audio.
        for audio_file in self.audiopathlist:
            fn = os.path.split(audio_file)[-1].strip().split()[0]

            # check if audio is in list of acceptable audios.
            if fn in self.idlist:

                verified.append(fn)

                array, sr, tmp = self._processAudio(fn)
                self._writeAudio(str(fn), array, sr)

                processed.append(tmp)

        self.data = dict(zip(verified, processed))

        self._savePickle(self.data)

        return None


if __name__ == "__main__":
    pass
