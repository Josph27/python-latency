from PyQt5 import QtCore, QtGui, QtWidgets, uic
import sys, timeit, datetime, os
from matplotlib import pyplot
from time import sleep
from pythonping import ping
#Multiple threads for multiple ips, time sync

# variables
delay = 0.05   # seconds
byte_size = 100 #byes
ip = '8.8.8.8'  # - google -> list?
loaded = []

values = [] # list of ,measure_lists
measures_list = [] # time / IP / size / ping /
loaded_data = [] # temp list
start = timeit.timeit()

class net_stats4 (QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = uic.loadUi('network_stats.ui', self)


        self.thread = {}
        self.startbutton.clicked.connect(self.start_ping)
        self.stopbutton.clicked.connect(self.stop_ping)
        self.savebutton.clicked.connect(self.save)
        self.graph_button.clicked.connect(self.graph)
        self.browsebutton.clicked.connect(self.load)
        self.graph_button2.clicked.connect(self.graph2)

    def start_ping(self):
        self.thread[1] = ThreadClass(parent=None, index = 1)
        self.thread[1].start()
        self.thread[1].any_signal.connect(self.ping)
        self.startbutton.setEnabled(False)

    def stop_ping(self):
        self.thread[1].stop()
        self.startbutton.setEnabled(True)

    def graph(self):
        x_axis = []
        for i in values:
            x_axis.append(float(i[0]))
        print(len(x_axis))
        print('time axis: ' + str(x_axis))

        y_axis = []
        for i in values:
            if i[1] == values[0][1]:
                y_axis.append(float(i[3]))
        print('ping axis:' + str(y_axis))


        if self.jitter_box.isChecked():
            jitter = self.jitter(values)
            print('jitter axis:' + str(jitter))
            pyplot.plot(x_axis, jitter, color='r', label='jitter')
        else:
            pass

        if self.ping_box.isChecked():
            pyplot.plot(x_axis, y_axis, color='b', label='ping')
        else:
            pass

        pyplot.title(f'pinging ip: {values[0][1]}', fontsize=20)
        pyplot.xlabel('time [s]')
        pyplot.ylabel('latency [ms]')
        pyplot.legend()
        pyplot.show()
        pyplot.figure('graph')
# ________________________________________________________________________________
    def graph2 (self):
        x_axis = []
        for i in loaded:
            x_axis.append(float(i[0]))
        print(len(x_axis))
        print('time axis: ' + str(x_axis))

        y_axis = []
        for i in loaded:
            if i[1] == loaded[0][1]:
                y_axis.append(float(i[3]))
        print('ping axis:' + str(y_axis))

        jitter = self.jitter(loaded)
        print('jitter axis:' + str(jitter))

        pyplot.plot(x_axis, jitter, color='r', label='jitter')
        pyplot.plot(x_axis, y_axis, color='b', label='ping')
        pyplot.title(f'pinging ip: {loaded[0][1]}', fontsize=20)
        pyplot.xlabel('time [s]')
        pyplot.ylabel('latency [ms]')
        pyplot.legend()
        pyplot.show()
        pyplot.figure('graph')

    def jitter(self, listvalues):
        jitterlist = []
        tempsum = 0
        pos = 0
        for value in listvalues:
            if pos < 10:
                jitterlist.append(0)
            else:
                for i in range(9):
                    calc = float(listvalues[pos-(10 - i)][3]) - float(listvalues[pos-(10 - i + 1)][3])
                    tempsum += abs(calc)
                jitterlist.append(tempsum / 9)
                tempsum = 0

            pos += 1
        return jitterlist

    def ping(self):
        self.ping_value.setText(values[len(values)-1][3])

    def save(self):
        file = open(os.getcwd() + f'\\Data\\{datetime.datetime.now().strftime("%Y_%m_%d %H_%M_%S.TXT")}','x')
        for i in values:
            for set in i:
                file.write(str(set))
                file.write(',')
            file.write('\n')

    def load(self):
        file_to_load = QtWidgets.QFileDialog.getOpenFileName(self, "Load TXT file", os.getcwd() + '\\Data\\')
        file = open(file_to_load[0],'r')
        print(file.readline())
        for line in file:
            a = line[:-2].split(',')
            print(a)
            loaded.append(a)
        loaded_text = str(file_to_load).split('/')
        self.loadedfile.setText(f'{loaded_text[-2]}/{loaded_text[-1]}')
        print(loaded)

class ThreadClass(QtCore.QThread):
    any_signal = QtCore.pyqtSignal(int)

    def __init__(self, parent=None, index=0):
        super(ThreadClass, self).__init__(parent)
        self.index = index
        self.is_running = True

    def run(self):
        print('Starting ping thread...')
        while (True):
            a = ping(ip, verbose=False, count=1, size=byte_size)
            b = str(a._responses).split(' ')
            global measures_list
            measures_list.append(round(timeit.timeit() + (delay * len(values)) - start, 4))  # time
            measures_list.append(b[2][:-1])  # ip
            measures_list.append(b[3])  # size
            measures_list.append(b[6][:-3])  # ping
            values.append(measures_list)
            self.any_signal.emit(1)
            measures_list = []
            sleep(delay)

    def stop(self):
        self.is_running = False
        print('Stopping thread...', self.index)
        self.terminate()
app = QtWidgets.QApplication(sys.argv)
mainWindow = net_stats4()
mainWindow.show()
sys.exit(app.exec_())









