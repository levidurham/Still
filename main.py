#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    main.py

    Launch still automation GUI.
"""

import sys
import serial
from PyQt5.QtWidgets import QApplication
from main_window import MainWindow

if __name__ == '__main__':
    APP = QApplication(sys.argv)
    WIN = MainWindow()
    WIN.showMaximized()

    sys.exit(APP.exec_())
