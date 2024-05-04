import tkinter as tk
from tkinter import ttk
import speech_recognition as sr
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


class SpeechRecognizerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("语音识别及Levenshtein距离评估")

        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.frame = ttk.Frame(self.master)
        self.frame.pack(pady=20, padx=20)

        self.actual_text = ttk.Entry(self.frame, width=50)
        self.actual_text.pack(padx=10, pady=10)
        self.actual_text.insert(0, "在此输入对比文本...")

        self.language_var = tk.StringVar()
        self.language_options = ttk.Combobox(self.frame, textvariable=self.language_var,
                                             values=['zh-CN', 'en-US', 'es-ES', 'de-DE'])
        self.language_options.pack(padx=10, pady=10)
        self.language_options.set('zh-CN')

        self.recognize_button = ttk.Button(self.frame, text="开始语音识别", command=self.start_recognition_thread)
        self.recognize_button.pack(pady=10)

        self.result_var = tk.StringVar()
        self.distance_var = tk.StringVar()

        self.result_label = ttk.Label(self.frame, textvariable=self.result_var)
        self.result_label.pack()
        self.distance_label = ttk.Label(self.frame, textvariable=self.distance_var)
        self.distance_label.pack()

        self.recognizer = sr.Recognizer()

    def recognize_and_evaluate(self):
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source)
                self.result_var.set("正在听...")
                audio = self.recognizer.listen(source)
                recognized_text = self.recognizer.recognize_google(audio, language=self.language_var.get())
                self.result_var.set(f"识别内容: {recognized_text}")
                distance = levenshtein_distance(self.actual_text.get(), recognized_text)
                self.distance_var.set(f"Levenshtein 距离: {distance}")
        except sr.RequestError:
            self.result_var.set("无法连接到API")
        except sr.UnknownValueError:
            self.result_var.set("无法识别语音")

    def start_recognition_thread(self):
        threading.Thread(target=self.recognize_and_evaluate).start()


root = tk.Tk()
app = SpeechRecognizerApp(root)
root.mainloop()
