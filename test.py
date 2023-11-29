from youteplustrans.whisper import WhisperTranscribe

def main():
    trans = WhisperTranscribe("ABQEu14OJYQ.webm", "The lockpicking lawyer looks at a lock sent in by a viewer", "medium")
    #print(trans.srt)

if __name__ == '__main__':
    main()