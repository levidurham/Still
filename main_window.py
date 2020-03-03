"""
main_window.py

The main window for the automated still.
"""
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
import serial
from ui_still import Ui_Still

class MainWindow(QMainWindow, Ui_Still):
    """Main window for the automated still."""

    _SER = serial.Serial(
        port='/dev/ttyACM0',
        baudrate=9600,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE
    )

    def serial_connect(self):
        """
            Ensure serial connection is up and ready
        """
        if self._SER.isOpen():
            self._SER.close()
        self._SER.open()
        self._SER.isOpen()

    def check_serial_connection(self):
        """ Maintain the serial connection"""
        try:
            if not self._SER.isOpen():
                self.statusbar.showMessage('Disconnected')
                self.serial_connect()
            else:
                self.statusbar.showMessage('Connected')
        finally:
            self.serial_check_timer = QTimer()
            self.serial_check_timer.setInterval(30000)
            self.serial_check_timer.timeout.connect(self.check_serial_connection)
            self.serial_check_timer.start()

        return self._SER.isOpen()

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        # Set Min/Max on Slider
        self.slider.setMinimum(150)
        self.slider.setMaximum(250)
        self.slider.lowSliderMoved.connect(self.on_low_slider_moved)
        self.slider.highSliderMoved.connect(self.on_high_slider_moved)
        #Set Temp label to 0
        self.temp_label.setText(str(0) + u'\N{DEGREE SIGN}')
        #Set Sliders to Min/Max as default
        self.slider.set_low(178)
        self.slider.set_high(190)

        # Data we will request later and an iterator over it
        self.data = ['Temp', 'High', 'Low', 'Burner', 'Pump']
        # Set up timers
        self.iterator = 0
        self.serial_check_timer = None
        self.read_timer = None
        self.serial_connect()
        self.check_serial_connection()
        self.read_serial()
        self.burner = 'Off'
        self.pump = 'On'

    def read_serial(self):
        """ Check serial bus for new data every 0.25 seconds """
        try:
            serial_in = ''
            while self._SER.inWaiting() > 0:
                serial_in += self._SER.read(1).decode()
        
            if serial_in != '':
                command = serial_in.split()
                print(command[0])
                if command[0] == 'Temp:':
                    self.on_temp_change(command[1])
                if command[0] == 'High':
                    self.slider.set_high(int(command[1]))
                if command[0] == 'Low':
                    self.slider.set_low(int(command[1]))
                if command[0] == 'Burner':
                    self.burner_state(command[1])
                if command[0] == 'Pump':
                    self.pump_state(command[1])

            self._SER.flushInput()
            self._SER.flushOutput()
            self.request_serial_data()
        finally:
            self.read_timer = QTimer()
            self.read_timer.setInterval(250)
            self.read_timer.timeout.connect(self.read_serial)
            self.read_timer.start()

    def burner_state(self, state):
        if not state == self.burner:
            if state == 'On':
                self.fire0.setPixmap(QPixmap(":/data/data/redfire.png"))
                self.fire1.setPixmap(QPixmap(":/data/data/redfire.png"))
                self.fire2.setPixmap(QPixmap(":/data/data/redfire.png"))
                self.burner = state
            elif state == 'Off':
                self.fire0.setPixmap(QPixmap(":/data/data/fire.png"))
                self.fire1.setPixmap(QPixmap(":/data/data/fire.png"))
                self.fire2.setPixmap(QPixmap(":/data/data/fire.png"))
                self.burner = state

    def pump_state(self, state):
        if not state == self.pump:
            if state == 'On':
                self.label.setPixmap(QPixmap(":/data/data/pump_on.png"))
                self.pump = state
            elif state == 'Off':
                self.label.setPixmap(QPixmap(":/data/data/pump.png"))
                self.pump = state

    def request_serial_data(self):
        """ Request the sending of data over serial """
        if self.iterator == len(self.data):
            self.iterator = 0
        self._SER.write(('Get ' + self.data[self.iterator] + '\n').encode())
        self.iterator += 1

    def on_low_slider_moved(self, value):
        """Set low_label on slider change"""
        self.low_label.setText(str(value) + u'\N{DEGREE SIGN}')

    def on_high_slider_moved(self, value):
        """Set high_label on slider change"""
        self.high_label.setText(str(value) + u'\N{DEGREE SIGN}')

    def on_temp_change(self, value):
        """Set temperature label on temperature change"""
        self.temp_label.setText(str(value) + u'\N{DEGREE SIGN}')

