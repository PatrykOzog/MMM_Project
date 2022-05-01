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


def triangle_gen(t, V, f, tri):
    plt.plot(time, tri)
    plt.title('Triangle wave')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.ylim(-V - 1, V + 1)
    plt.grid(True, which='both')
    plt.axhline(y=0, color='k')
    return plt.gcf()


def triangle_response(tri, L, R, Km, KT, b, J, I, w, t):
    for i in range(len(tri)):
        if i + 1 == len(tri):
            break
        else:
            ts = t[i + 1] - t[i]
            I.append(I[i] + ts * (tri[i] / L - (R * I[i]) / L - (Km * w[i]) / L))
            w.append(w[i] + ts * ((KT * I[i]) / J - (b * w[i]) / J))


def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.flush_events()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg


max_time = 5
amplitude = 1
frequency = 1
resistance = 4
inductance = 1
Moment_inertia = 1
km = 1
kT = 1
damping = 1
current = [0]
omega = [0]

time = np.linspace(0, max_time, 100000, endpoint=True)

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
        try:
            frequency = float(values["-frequency-"])
            amplitude = float(values["-amplitude-"])
            max_time_after = float(values["-time-"])
            isError = False
            if max_time_after != max_time:
                time = np.linspace(0, max_time_after, 100000, endpoint=True)
                max_time = max_time_after
        except ValueError:
            sg.popup("An error has occurred\nValue in the text box is incorrect!\n", title="ERROR", grab_anywhere=True)
            isError = True
            # window.refresh()

    if not isError:
        if event == "Generate triangle wave":
            fig_agg.get_tk_widget().forget()
            plt.close('all')
            triangle = amplitude * signal.sawtooth(2 * np.pi * frequency * time, 0.5)
            fig_agg = draw_figure(window["-CANVAS-"].TKCanvas, triangle_gen(time, amplitude, frequency, triangle))
            triangle_response(triangle, inductance, resistance, km, kT, damping, Moment_inertia, current, omega, time)
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
