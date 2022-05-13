import numpy as np
import matplotlib.pyplot as plt
import PySimpleGUI as sg
from scipy import signal
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def response(name, sig, L, R, Km, KT, b, J, t):
    figure, axis = plt.subplots(3, figsize=(14, 11))
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
    axis[0].grid()

    axis[1].set_title("Current")
    axis[1].set_ylabel("I[A]")
    axis[1].set_xlabel("t[s]")
    axis[1].grid()

    axis[2].set_title("Angular velocity")
    axis[2].set_ylabel("w[rad/s]")
    axis[2].set_xlabel("t[s]")
    axis[2].grid()

    plt.subplots_adjust(hspace=0.5)

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
moment_inertia = 1
km = 1
kT = 1
damping = 1
samples = 100000
duration = 2
is_generated = False



sg.theme("DarkAmber")

first_column = [
    [sg.Text("Frequency [Hz]:", size=(20, 1)), sg.InputText(frequency, key="-frequency-")],
    [sg.Text("Amplitude [V]:", size=(20, 1)), sg.InputText(amplitude, key="-amplitude-")],
    [sg.Text("Time [s]:", size=(20, 1)), sg.InputText(max_time, key="-time-")],
    [sg.Text("Resistance [\u03A9]:", size=(20, 1)), sg.InputText(resistance, key="-resistance-")],
    [sg.Text("Inductance [H]:", size=(20, 1)), sg.InputText(inductance, key="-inductance-")],
    [sg.Text("Moment of inertia [kg*m^2]:", size=(20, 1)), sg.InputText(moment_inertia, key="-moment_inertia-")],
    [sg.Text("Constant value kM:", size=(20, 1)), sg.InputText(km, key="-km-")],
    [sg.Text("Constant value kT:", size=(20, 1)), sg.InputText(kT, key="-kT-")],
    [sg.Text("Damping factor:", size=(20, 1)), sg.InputText(damping, key="-damping-")],
    [sg.Text("Number of samples:", size=(20, 1)), sg.InputText(samples, key="-samples-")],
    [sg.Text("Duration:", size=(20, 1)), sg.InputText(duration, key="-duration-")],
    [sg.Text(" ")],
    [sg.Button("Generate square wave", size=(20, 1))],
    [sg.Button("Generate triangle wave", size=(20, 1))],
    [sg.Button("Generate sine wave", size=(20, 1))],
    [sg.Button("Generate square wave with finite duration", size=(20, 2))],
    [sg.Text(" ")],
    [sg.Button("Save data to txt", size=(20, 1)), sg.Button("Save image to jpg", size=(20, 1))],
    [sg.Button("Load data from txt", size=(20, 1)), sg.InputText(key="--", size=(23, 1))],
    [sg.Text(" ")],
    [sg.Button("Quit")],

]

second_column = [
    [sg.Canvas(size=(1400, 1100), key="-CANVAS-")],
]

layout = [
    [
        sg.Column(first_column),
        sg.VSeparator(),
        sg.Column(second_column),
    ]
]

window = sg.Window("hi", layout, location=(500, 50), size=(500, 650), finalize=True)

while True:
    event, values = window.read()
    if event and is_generated == False:
        fig_agg = draw_figure(window["-CANVAS-"].TKCanvas, None)
        is_generated = True
        time = np.linspace(0, max_time, samples, endpoint=True)
    if event in (sg.WIN_CLOSED, "Quit"):
        break
    elif event == "Generate square wave" or event == "Generate triangle wave" or event == "Generate sine wave" or event == "Generate square wave with finite duration":
        try:
            frequency = float(values["-frequency-"])
            amplitude = float(values["-amplitude-"])
            max_time_after = float(values["-time-"])
            resistance = float(values["-resistance-"])
            inductance = float(values["-inductance-"])
            moment_inertia = float(values["-moment_inertia-"])
            km = float(values["-km-"])
            kT = float(values["-kT-"])
            damping = float(values["-damping-"])
            samples_after = int(values["-samples-"])
            duration = float(values["-duration-"])
            isError = False
            if max_time_after != max_time or samples_after != samples:
                max_time = max_time_after
                samples = samples_after
                time = np.linspace(0, max_time, samples, endpoint=True)

        except ValueError:
            sg.popup("An error has occurred\nValue in the text box is incorrect!\n", title="ERROR", grab_anywhere=True)
            isError = True

    if not isError:
        if event == "Generate triangle wave":
            fig_agg.get_tk_widget().forget()
            plt.close('all')
            triangle = amplitude * signal.sawtooth(2 * np.pi * frequency * time - 1.5 * np.pi, 0.5)
            wave_name = "Triangle"
            fig_agg = draw_figure(window["-CANVAS-"].TKCanvas,
                                  response(wave_name, triangle, inductance, resistance, km, kT, damping, moment_inertia,
                                           time))
            window.refresh()
        elif event == "Generate square wave":
            fig_agg.get_tk_widget().forget()
            plt.close('all')
            square = amplitude * signal.square(2 * np.pi * frequency * time)
            wave_name = "Square"
            fig_agg = draw_figure(window["-CANVAS-"].TKCanvas,
                                  response(wave_name, square, inductance, resistance, km, kT, damping, moment_inertia,
                                           time))
            window.refresh()
        elif event == "Generate sine wave":
            fig_agg.get_tk_widget().forget()
            plt.close('all')
            sin = amplitude * np.sin(2 * np.pi * frequency * time)
            wave_name = "Sine"
            fig_agg = draw_figure(window["-CANVAS-"].TKCanvas,
                                  response(wave_name, sin, inductance, resistance, km, kT, damping, moment_inertia,
                                           time))
            window.refresh()
        elif event == "Generate square wave with finite duration":
            fig_agg.get_tk_widget().forget()
            plt.close('all')
            square_timed = amplitude + time * 0
            wave_name = "Square"
            for i, j in enumerate(time):
                if j >= duration:
                    square_timed[i] = 0

            fig_agg = draw_figure(window["-CANVAS-"].TKCanvas,
                                  response(wave_name, square_timed, inductance, resistance, km, kT, damping,
                                           moment_inertia, time))
            window.refresh()

    window.Maximize()

window.close()
