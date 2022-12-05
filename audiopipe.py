import os
import pickle5
import numpy as np 
from pickle5 import HIGHEST_PROTOCOL
import pyflac
"""
This is meant a as a general audio processing pipeline and will be updated as I go. 
The environmental variables are set because this script is meant to be run on a high power computing cluster. 


TODO:
Allow for other audio file types to be read
Need to write encode the audio files as FLAC for NOW, will add options for other audio encodings

"""

HOME = os.getenv('HOME')
WORK = os.getenv('WORK')

#Removed rats with NA on them.  
PATH = os.path.join(HOME, "/usv_analysis/nath_rat_pipe/unique_rats.txt")


class AudioPipe:
    """
    This acts as a general audio processing pipe line it currently only requires a path to work.
    _getwritepath()       creates the path to write audio files to 
    _getreaddir()         creates the path to read audio from 
    getIDs()              creates list of acceptable files to read from
    _createAudioList()     creates list of audio directory paths. 
    """
    def __init__(self, fp:str):
        self.workdir = fp
        self.writedir = self._getwritekdir()
        self.audiodir = self._getreaddir()
        self.audiopathlist = self._createAudioPathList()

    def __str__(self):
        return "AudioPath"
    
    def __repr__(self):
        return "AudioPath Object"

    def _getwritedir(self):
        """get the dierctory to write to"""
        WORK_DIR_PATH = os.path.join(WORK,"5_min_samples")
        if not os.path.exists(WORK_DIR_PATH):
            os.mkdir(WORK_DIR_PATH)
            return WORK_DIR_PATH
        else:
            return WORK_DIR_PATH
        
    def _getreaddir(self):
        """get the directory to be read from"""
        READ_DIR_PATH = os.pathjoin(self.workdir, "audios")
        if not os.path.exists(READ_DIR_PATH):
            os.mkdir(READ_DIR_PATH)
            return READ_DIR_PATH
        else:
            return READ_DIR_PATH       
    
    def getIDs(self,textPATH:str) -> list: 
        """
        Reads the IDs of the rats from a txt file by line
        textPATH        This is the path to the text file
        """
        _, fname = os.path.split(textPATH)
        with open(fname, 'r') as f:
            id_list = f.readline().strip()
        del id_list[0] # header info.
        for id in id_list:
            id = id.strip()
        self.idlist = id_list
        return id_list
    
    def _createAudioPathList(self, id:str) -> list:
        """Create a list of acceptable audio paths to be read from"""
        os.chdir(self.audiodir)
        
        audio_path_list = list()
        #find the audios for each of the rats in the ids and return list element 
        
        for dirpath, _, filenames in os.walk(self.audiodir, topdown=True):
            os.chdir(dirpath)
            for name in filenames:
                if id in name: 
                    audio_path_list.append(name)
        
        return audio_path_list

    def _savePickle(self, var, name:str):
        """save dict as pickle"""
        
        name = #++??
        
        with open(var, "wb") as fp:
            pickle5.dump(var,f"{name}", HIGHEST_PROTOCOL)
        pass
    
    def _saveAudio(self, audio_buffer:np.array, sr:int):
        # use audio_buffer and sr to encode into flac. 
        return

    def _sampleAudio1(self, audio:np.array, sr:int) -> np.ndarray:
        """auxiliary function to sample only the first minute of audio"""
        fithminute = sr * 5
        sampleFiveminutes = audio[0:fithminute]
        return sampleFiveminutes
    
    def _sampleAudioS(self, audio:np.array, sr:int) -> list:
        """
        Version of the auxiliary function that slides over the 
        length of the audio in 5 minute sections returing a list of audio samples
        """
        length = len(audio)
        fiveminute = 5*sr
        
        window_length = length//fiveminute
        
        num_slides = (window_length *2) - 1
        
        samples = list()
        
        for n in range(num_slides):
            start = n * fiveminute
            stop = start +fiveminute
            
            samples.append(audio[start:stop])
        
        return samples
            
    # needs to work for other audio files i.e. wav, mp3, flac etc. 
    def _processAudio(self, audiopath, option = None):
        """
        opens the FLAC file,
        save array of PMF and sample rate
        variable is saved as flac via copyAudio and wiritten
        """
        decoder = pyflac.FileDecoder(input_file=audiopath)
        array, sr = decoder.process()
        if option == None:
            processed = self._sampleAudio(array, sr)
        else: 
            processed = self._sampleAudioS(array, sr)
        
        return processed
    
    
    def sampleAudio(self):
        # open audio 
        """
        This samples the audio files in the readdir and makes a copy of it using 
        the auxiliary _processAudio and _sampleAudio1 or _sampleAudioS functions.
        It then returns a dictionary of the sampled files
        """
        processed = list()
        name = list()
        for audio_file in self.audiopathlist:
            fn = os.split(audio_file)[-1].strip().split()[0]
            if fn in self.idlist:
                fn.append(name)
                processed.append(self._processAudio(fn))
        self.data = dict(zip(name,processed))
        
        return self.data


    #create spectrogram of each of their audios. 
    def saveSample(object:np.array, name) -> None:
        FIGURES_PATH = os.path.join(WORK,"spectrograms")
        os.chdir(FIGURES_PATH)
        
        with open(object, 'wb') as f: 
            pkl.dump(f, f"{name}.spec", HIGHEST_PROTOCOL)
        
        return None

# def createSpecs(ids:list) -> str:
    
#     sample_rate = 384000
#     time_res = 20 
#     n_fft = int(sample_rate / time_res)
#     hop_length = n_fft // 2  
  
    
#     for id in ids: 
#         audio_file = os.path.join(WORK,id)
        
#         data, _ = librosa.load(audio_file, sr = sample_rate)
#         fourier = librosa.stft(data, n_fft = n_fft, hop_length=hop_length)
#         power_spec = librosa.power_to_db(np.abs(fourier), ref=np.max)

#         savePickle(power_spec)
    
    
#     return print("success")
    


