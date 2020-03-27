import tkinter as tk
import threading
import pyaudio
import wave
from os import walk


class App():
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 2
    fs = 44100

    frames = []

    def ontopicchange(self, *args):
        topic_name = self.emo.get()
        file = open(topic_name + '/' + 'article.txt', 'r')
        content = file.read()
        self.sentences = content.split('\n')
        self.sentences.pop(0)
        self.current_sentence = -1


    def nextSentence(self):
        self.current_sentence += 1

        if self.current_sentence*2 >= len(self.sentences):
            print('End of article')
            exit()

        self.name_entry.delete(0, 1000)
        filename = self.sentences[self.current_sentence*2]
        self.name_entry.insert(0, filename[0:3])
        print(self.sentences[self.current_sentence*2+1])

    def __init__(self, master, topics):
        self.sentences = []
        self.current_sentence = -1
        self.isrecording = False
        self.button1 = tk.Button(main, text='rec', command=self.startrecording)
        self.button2 = tk.Button(main, text='stop', command=self.stoprecording)
        self.name_entry = tk.Entry(main, width=40)
        self.lable1 = tk.Label(main, text='Record Name')

        self.emo = tk.StringVar(main)
        self.emo.set('choose topic')
        self.popupMenu = tk.OptionMenu(main, self.emo, *topics)
        self.emo.trace('w', self.ontopicchange)

        self.sentence = 'article here'
        self.sentence_label = tk.Label(main, text=self.sentence)

        self.next_button = tk.Button(main, text='next', command=self.nextSentence)

        self.popupMenu.pack()
        self.lable1.pack()
        self.name_entry.pack()
        self.next_button.pack()
        self.button1.pack()
        self.button2.pack()

    def startrecording(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.sample_format, channels=self.channels, rate=self.fs,
                                  frames_per_buffer=self.chunk, input=True)
        self.isrecording = True

        print('Recording')
        self.t = threading.Thread(target=self.record)
        self.t.start()

    def stoprecording(self):
        self.isrecording = False
        print('recording complete')
        self.filename = self.emo.get() + "/" + self.name_entry.get()
        self.filename = self.filename + ".wav"
        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.sample_format))
        wf.setframerate(self.fs)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        self.frames.clear()

    def record(self):
        while self.isrecording:
            data = self.stream.read(self.chunk)
            self.frames.append(data)


# Get list of topics
topics = dict()
for (dirpath, dirnames, filenames) in walk('.'):
    for dirname in dirnames:
        topics.update({dirname: dirname})
    break

main = tk.Tk()
main.title('recorder')
main.geometry('1000x500')
app = App(main, topics)
main.mainloop()
