import numpy as np
import matplotlib.pyplot as plt
import PySimpleGUI as sg
from scipy import signal
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def response(name, sig, L, R, Km, KT, b, J, t):
    figure, axis = plt.subplots(3, figsize=(12,9))
    I = [0]
    w = [0]
    for i in range(len(sig)):
        if i + 1 == len(sig):
            break
        else:
            ts = t[i + 1] - t[i]
            I.append(I[i] + ts * (sig[i] / L - (R * I[i]) / L - (Km * w[i]) / L))
            w.append(w[i] + ts * ((KT * I[i]) / J - (b * w[i]) / J))

    axis[0].plot(t, sig)
    axis[1].plot(t, I)
    axis[2].plot(t, w)

    axis[0].set_title(f"{name} wave")
    axis[0].set_ylabel("U[V]")
    axis[0].set_xlabel("t[s]")
    axis[1].set_title("Current")
    axis[2].set_title("Angular velocity")
    plt.subplots_adjust(hspace=1)

    # plt.title('Triangle wave')
    # plt.xlabel('Time')
    # plt.ylabel('Amplitude')
    # plt.ylim(-V - 1, V + 1)
    # plt.grid(True, which='both')
    # plt.axhline(y=0, color='k')
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
    [sg.Canvas(size=(800, 800), key="-CANVAS-")],
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

    if not isError:
        if event == "Generate triangle wave":
            fig_agg.get_tk_widget().forget()
            plt.close('all')
            triangle = amplitude * signal.sawtooth(2 * np.pi * frequency * time - 1.5*np.pi, 0.5)
            wave_name = "Triangle"
            fig_agg = draw_figure(window["-CANVAS-"].TKCanvas, response(wave_name, triangle, inductance, resistance, km, kT, damping, Moment_inertia, time))
            window.refresh()
        elif event == "Generate square wave":
            fig_agg.get_tk_widget().forget()
            plt.close('all')
            square = amplitude * signal.square(2 * np.pi * frequency * time)
            wave_name = "Square"
            fig_agg = draw_figure(window["-CANVAS-"].TKCanvas, response(wave_name, square, inductance, resistance, km, kT, damping, Moment_inertia, time))
            window.refresh()
        elif event == "Generate sine wave":
            fig_agg.get_tk_widget().forget()
            plt.close('all')
            sin = amplitude * np.sin(2 * np.pi * frequency * time)
            wave_name = "Sine"
            fig_agg = draw_figure(window["-CANVAS-"].TKCanvas, response(wave_name, sin, inductance, resistance, km, kT, damping, Moment_inertia, time))
            window.refresh()

window.close()
