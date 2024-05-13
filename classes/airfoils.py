import matplotlib.pyplot as plt
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.pyplot import figure

matplotlib.use('TkAgg')


class airfoils:

    def __init__(self, canvas):
        self.fig, self.ax = plt.subplots( facecolor = 'aliceblue')
        self.fig.set_size_inches(5.5, 3.5)
        self.ax.set_facecolor('lavender')
        self.file = ""
        self.name = "Airfoil - XXXX"
        # Airfoil Points
        self.x_array = []
        self.y_upper_array = []
        self.y_lower_array = []
        self.chord = 1.0

        # Port locations
        self.x_upper_ports = []
        self.x_lower_ports = []
        self.y_upper_ports = []
        self.y_lower_ports = []


        # self.format_figure()
        self.tkcanvas = FigureCanvasTkAgg(self.fig, canvas)
        figure(figsize=(4, 3), dpi=80)
        # self.fig.set_size_inches(1, 0.5)
        # self.fig.tight_layout()
        # plt.tight_layout(rect=[0.1, -0.1, 1, 0.])



    def read_points(self):
        f = open(self.file, "r")
        for x in f:
            print(x)

    def draw_figure(self):
        self.format_figure()
        # plt.grid()

        self.tkcanvas.draw()
        self.tkcanvas.get_tk_widget().pack(side='right', fill='none', expand=0)
        return self.tkcanvas

    def format_figure(self):

        try:
            xlim_min = min(self.x_array)
            xlim_max =  max(self.x_array)
            ylim_min = min(self.y_upper_array)
            ylim_max = max(self.y_upper_array)
        except:
            xlim_min = -0.1
            xlim_max = 1.1
            ylim_min = -0.15
            ylim_max = 0.35

        self.ax.set(xlim=(xlim_min,xlim_max),
                    ylim=(ylim_min, ylim_max))
        self.ax.axis('equal')
        self.ax.set_title(self.name)
        self.ax.set_ylabel("y [mm]")
        self.ax.set_xlabel("x [mm]")
        self.ax.grid()
        self.fig.tight_layout()

    def load_airfoil(self, file, chord):
        self.chord = float(chord)
        self.file = file
        self.ax.clear()

        # Read the file in question
        f = open(self.file, "r")
        self.x_array = []
        self.y_upper_array = []
        counter = 0

        for line in f:

            if counter > 0:
                x, y = line.split()
                self.x_array.append(self.chord*float(x))
                self.y_upper_array.append(self.chord*float(y))
            else:
                self.name = line

            counter = counter + 1
        self.ax.plot(self.x_array, self.y_upper_array)

        # plt.margins(x=0)