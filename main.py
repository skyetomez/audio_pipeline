import audiopipe as pipe
import os 


HOME = str(os.getenv('HOME'))
WORK = str(os.getenv('WORK'))

textfile_path = "/usv_analysis/nath_rat_pipe/unique_rats.txt"

TEXTPATH = os.path.join(WORK, textfile_path)


def main():
    audio_pipe  = pipe.AudioPipe(WORK)
    idlist, audiopathlist = audio_pipe.getIDs(TEXTPATH)
    audio_pipe.sampleAudio()
    
    return print("Success")

if __name__ == '__main__':
    main()