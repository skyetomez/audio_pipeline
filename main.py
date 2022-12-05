import audiopipe as pipe
import os 


HOME = os.getenv('HOME')
WORK = os.getenv('WORK')

TEXTPATH = os.path.join(WORK, "/usv_analysis/nath_rat_pipe/unique_rats.txt")


def main():
    audio_pipe  = pipe.AudioPipe(WORK)
    idlist, audiopathlist = audio_pipe.getIDs(TEXTPATH)
    audio_pipe.sampleAudio()
    
    return print("Success")

if __name__ == '__main__':
    main()