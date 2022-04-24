import numpy as np
import matplotlib.pyplot as plt
import PySimpleGUI as sg
from scipy import signal
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def sine_gen(t, V, f):
    sin = V * np.sin(2 * np.pi * f * t)
    plt.plot(time, sin)
    plt.title('Sine wave')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.ylim(-V - 1, V + 1)
    plt.grid(True, which='both')
    plt.axhline(y=0, color='k')
    return plt.gcf()


def square_gen(t, V, f):
    square = V * signal.square(2 * np.pi * f * t)
    plt.plot(time, square)
    plt.title('Square wave')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.ylim(-V - 1, V + 1)
    plt.grid(True, which='both')
    plt.axhline(y=0, color='k')
    return plt.gcf()


def triangle_gen(t, V, f):
    triangle = V * signal.sawtooth(2 * np.pi * f * t, 0.5)
    plt.plot(time, triangle)
    plt.title('Triangle wave')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.ylim(-V - 1, V + 1)
    plt.grid(True, which='both')
    plt.axhline(y=0, color='k')
    return plt.gcf()


def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.flush_events()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg


max_time = 5
amplitude = 1
frequency = 1


time = np.linspace(0, max_time, 500000, endpoint=True)
#voltage_values = np.array(sine_gen(time, amplitude, frequency))
#plt.plot(time, voltage_values)


sg.theme("DarkAmber")

first_column = [
    [sg.Text("Frequency [Hz]:", size=(12, 1)), sg.InputText(frequency, key="-frequency-")],
    [sg.Text("Amplitude [V]:", size=(12, 1)), sg.InputText(amplitude, key="-amplitude-")],
    [sg.Text("Time [s]:", size=(12, 1)), sg.InputText(max_time, key="-time-")],
    [sg.Text(" ")],
    [sg.Button("Generate square wave", size=(20, 1))],
    [sg.Button("Generate triangle wave", size=(20, 1))],
    [sg.Button("Generate sine wave", size=(20, 1))],
    [sg.Text(" ")],
    [sg.Button("Quit")],

]

second_column = [
    [sg.Canvas(size=(500, 500), key="-CANVAS-")],
]

layout = [
    [
        sg.Column(first_column),
        sg.VSeparator(),
        sg.Column(second_column),
    ]
]

window = sg.Window("hi", layout, finalize=True, element_justification="center")
fig_agg = draw_figure(window["-CANVAS-"].TKCanvas, None)

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, "Quit"):
        break
    elif event == "Generate square wave" or event == "Generate triangle wave" or event == "Generate sine wave":
        frequency = float(values["-frequency-"])
        amplitude = float(values["-amplitude-"])
        max_time_after = float(values["-time-"])
        if max_time_after != max_time:
            time = np.linspace(0, max_time_after, 1000, endpoint=True)
            max_time = max_time_after

    if event == "Generate triangle wave":
        fig_agg.get_tk_widget().forget()
        plt.close('all')
        fig_agg = draw_figure(window["-CANVAS-"].TKCanvas, triangle_gen(time, amplitude, frequency))
        window.refresh()
    elif event == "Generate square wave":
        fig_agg.get_tk_widget().forget()
        plt.close('all')
        fig_agg = draw_figure(window["-CANVAS-"].TKCanvas, square_gen(time, amplitude, frequency))
        window.refresh()
    elif event == "Generate sine wave":
        fig_agg.get_tk_widget().forget()
        plt.close('all')
        fig_agg = draw_figure(window["-CANVAS-"].TKCanvas, sine_gen(time, amplitude, frequency))
        window.refresh()

window.close()
#test