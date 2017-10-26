import sys
import time

import tkinter as tk
import tkinter.ttk as ttk

from tkinter import scrolledtext
from tkinter import filedialog

import matplotlib.pyplot as plt

from .status import Status, StatusFrame
from .status import Plot
from .gridframe import GridFrame
from .primary import Primary
from .list import List
from .style import configure_style

from .plot import plot_imbedded

plt.style.use('dark_background')

class MainApplication(GridFrame):

    def __init__(self, parent, *args, **kwargs):
        GridFrame.__init__(self, parent, *args, **kwargs)

        self.parent = parent
        self.primary = Primary(self, *args, **kwargs)
        self.add(self.primary, 0, 0, xspan=2)
        self.create_widgets()
        GridFrame.configure(self)
        
        #self.messages = []

    #def log(self, message):
    #    self.messages.append(message)

    def create_widgets(self):
        self.slipList = List(self, 10)
        self.add(self.slipList, 0, 1)

        self.codeletList = List(self, 10)
        self.add(self.codeletList, 1, 1)

        self.objectList = List(self, 10)
        self.add(self.objectList, 2, 1)

        #self.logBox = List(self, 10)
        #self.add(self.logBox, 1, 0)

        self.graph2 = Plot(self, 'Answer Distribution')
        self.add(self.graph2, 2, 0)

    def update(self, copycat):
        self.primary.update(copycat)

        slipnodes = copycat.slipnet.slipnodes
        codelets  = copycat.coderack.codelets
        objects   = copycat.workspace.objects

        self.slipList.update(slipnodes, key=lambda s:s.activation, 
                formatter=lambda s : '{}: {}'.format(s.name, round(s.activation, 2)))
        self.codeletList.update(codelets, key=lambda c:c.urgency, formatter= lambda s : '{}: {}'.format(s.name, round(s.urgency, 2)))
        self.objectList.update(objects, formatter=lambda s : '{}'.format(str(s.descriptions)))
        #self.logBox.update(list(reversed(self.messages))[:10])

    def reset_with_strings(self, initial, modified, target):
        self.primary.reset_with_strings(initial, modified, target)

class GUI(object):
    def __init__(self, title, updateInterval=.1):
        self.root = tk.Tk()
        self.root.title(title)
        tk.Grid.rowconfigure(self.root, 0, weight=1)
        tk.Grid.columnconfigure(self.root, 0, weight=1)
        self.app = MainApplication(self.root)
        self.app.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

        configure_style(ttk.Style())

        self.lastUpdated = time.time()
        self.updateInterval = updateInterval

    def add_answers(self, answers):
        def modifier(status):
            with plt.style.context(('dark_background')):
                plot_imbedded(answers, status)
        self.app.graph2.status.modifier = modifier 

    def refresh(self):
        self.root.update_idletasks()
        self.root.update()

    def update(self, copycat):
        current = time.time()
        self.app.update(copycat)
        self.lastUpdated = current