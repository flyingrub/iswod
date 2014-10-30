#!/usr/bin/python3
import speech_recognition as sr
import pyaudio
import wave
import sys
fail_counter=1
MDP = 'jambon'

def main():
    global fail_counter
    r = sr.Recognizer(language = "fr-FR")
    m = sr.Microphone()

    with m as source:
        audio = r.listen(source)
        print("Verification en cours...")
        playaudio('verif.wav')
        try:
            recognised=r.recognize(audio)
            print("Vous avez dit : %s" % (recognised))
        except LookupError:
            while fail_counter < 3:
                fail_counter += 1
                print('essai n°%d' % fail_counter)
                print("Nous n'avons pas sasie veuillez réessayer.")
                playaudio('repete.wav')
                main()
            print('Nous n\'avons pas compris')
            sys.exit()

    if MDP in recognised.lower() :
        print('Autorisation en cours... ')
        playaudio('autorise.wav')
        #Open the door here
    else:
        print('accés refusé')
        playaudio('refuse.wav')
    sys.exit()

def playaudio(file):
    chunk = 1024
    # open the file for reading.
    wf = wave.open(file, 'rb')

    # create an audio object
    p = pyaudio.PyAudio()

    # open stream based on the wave object which has been input.
    stream = p.open(format =
                    p.get_format_from_width(wf.getsampwidth()),
                    channels = wf.getnchannels(),
                    rate = wf.getframerate(),
                    output = True)

    # read data (based on the chunk size)
    data = wf.readframes(chunk)

    # play stream (looping from beginning of file to the end)
    while data != '':
        # writing to the stream is what *actually* plays the sound.
        stream.write(data)
        data = wf.readframes(chunk)

    # cleanup stuff.
    stream.close()
    p.terminate()


if __name__ == "__main__":
    print("Mot de passe!")
    playaudio('saisir.wav')
    main()
