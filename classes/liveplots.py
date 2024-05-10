import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.pyplot import figure

matplotlib.use('TkAgg')

plot_colors = ['b', 'r', 'orange', 'green', 'pink', 'black']
class liveplots:

    def __init__(self, buffer_size, canvas):
        self.time_recorded = []
        self.pressure_recorded = []
        self.time_plotted = []
        self.pressures_plotted =[ []]#, [], [], [], [], []]
        self.buffer_size = buffer_size
        self.record_is_true = False

        # self.name = "time vs pressure"

        self.fig, self.ax = plt.subplots()
        self.fig.set_size_inches(10.5, 5.5)
        self.format_fig()

        self.tkcanvas = FigureCanvasTkAgg(self.fig, canvas)
        self.ax.plot([], [], marker="o")
        self.tkcanvas.draw()
        self.tkcanvas.get_tk_widget().pack(side='right', fill='none', expand=0)

    def add_point(self, t, y):
        # if self.record_is_true:
        self.tkcanvas.flush_events()
        self.ax.clear()

        self.time_plotted.append(t)

        for i in range(len(self.pressures_plotted)):

            self.pressures_plotted[i].append(eval(y[i]))
            self.pressures_plotted[i] = self.pressures_plotted[i][-self.buffer_size:]

        self.time_plotted = self.time_plotted[-self.buffer_size:]
        # self.pressures_plotted = self.pressures_plotted[-self.buffer_size:]


        for i in range(len(self.pressures_plotted)) :

            p_temp = self.pressures_plotted[i]
            self.ax.plot(self.time_plotted, p_temp,  plot_colors[i], marker="o")

        self.format_fig()
        self.tkcanvas.draw()
        self.tkcanvas.get_tk_widget().pack(side='right', fill='none', expand=0)

        return self.tkcanvas

        # print(self.time_plotted, self.pressures_plotted)

    def format_fig(self):
        # self.ax.set(ylim=(0, 1024))

        self.ax.grid()
        self.ax.set_title("Time vs Pressure")
        self.ax.set_ylabel("Pressure [Pa]")
        self.ax.set_xlabel("Time [ms]")
        self.ax.set_yticks([92.5,95,97.5,100,102.5,105])
        self.ax.set_yticklabels([92.5,95,97.5,100,102.5,105])


    # def plot_data(self):
    #     # self.ax.clear()
    #
    #
    #
