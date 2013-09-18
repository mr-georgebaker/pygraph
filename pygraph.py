#!/usr/bin/python

""" A simple function plotter based on matplotlib, tkinter and numpy
See "Help" -> "Usage" for details on how to use different mathematical functions """

try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
from tkMessageBox import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from scipy.misc import factorial
from sympy.parsing.sympy_parser import parse_expr
from idlelib import ToolTip
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import parser
import re

REPLACE_DIC = {'sin' : 'np.sin',
               'arcsin' : 'np.arcsin',
               'sinh' : 'np.sinh',
               'arcsinh' : 'np.arcsinh',
               'cos' : 'np.cos',
               'arccos' : 'np.arccos',
               'cosh' : 'np.cosh',
               'arccosh' : 'np.arccosh',
               'tan' : 'np.tan',
               'arctan' : 'np.arctan',
               'tanh' : 'np.tanh',
               'arctanh' : 'np.arctanh',
               'ln' : 'np.log',
               'log' : 'np.log',
               'log10' : 'np.log10',
               'log2' : 'np.log2',
               'exp' : 'np.exp',
               '^' : '**',
               'fac' : 'factorial',
               'sqrt' : 'np.sqrt',
               'pi' : 'np.pi',
               'PI' : 'np.pi',
               'sinc' : 'np.sinc'
               }


class App:

    def __init__(self, master):

        self.master = master
        self.initUI()
        self.x = 0
        self.y = 0
        self.legend = 0
        self.formula_finish = 0
        self.slope = 0

    def initUI(self):
        """ Initialize the GUI-Elements """
        self.master.title("Formula Plotter")

        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)
        self.helpmenu = tk.Menu(self.menu)
        self.menu.add_cascade(label='Help', menu=self.helpmenu)
        self.helpmenu.add_command(label='Usage', command=self.instructions)

        self.scale_x_min = tk.Scale(self.master, from_=-500, to=0,
                               tickinterval=100, length=600,
                               orient='horizontal', command=self.set_x_min)
        self.scale_x_min.grid(row=4, column=1)
        self.x_min = tk.IntVar()

        self.scale_x_max = tk.Scale(self.master, from_=0, to=500,
                               tickinterval=100, length=600,
                               orient='horizontal', command=self.set_x_max)
        self.scale_x_max.grid(row=5, column=1)
        self.scale_x_max.set(10)
        self.x_max = tk.IntVar()

        self.replot_button = tk.Button(self.master, text='New plot',
                                  command=self.replot)
        self.replot_button.grid(row=0, column=2)
        ToolTip.ToolTip(self.replot_button,
                        'Clear current plot and draw new function')
        self.updateplot_button = tk.Button(self.master, text='Add to plot',
                                     command=self.update)
        self.updateplot_button.grid(row=0, column=3)
        ToolTip.ToolTip(self.updateplot_button,
                        'Draw new plot on existing')

        self.minima_button = tk.Button(self.master, text='Local Minima',
                                  command=self.minima)
        self.minima_button.grid(row=4, column=2)
        ToolTip.ToolTip(self.minima_button, 'Show local Minima')

        self.maxima_button = tk.Button(self.master, text='Local Maxima',
                                  command=self.maxima)
        self.maxima_button.grid(row=5, column=2)
        ToolTip.ToolTip(self.maxima_button, 'Show local Maxima')
        
        self.turning_button = tk.Button(self.master, text='Turning point',
                                   command=self.turning_point)
        self.turning_button.grid(row=6, column=2)
        ToolTip.ToolTip(self.turning_button, 'Show turning points')

        self.tangent_button = tk.Button(self.master, text='Tangent',
                                        command=self.tangent)
        self.tangent_button.grid(row=6, column=3)
        ToolTip.ToolTip(self.tangent_button, 'Show tangent at entered value')
        
        tk.Label(self.master, text='f (x) =').grid(row=0, column=0)
        tk.Label(self.master, text='x minimum').grid(row=4, column=0)
        tk.Label(self.master, text='x maximum').grid(row=5, column=0)
        tk.Label(self.master, text='Enter tangent value').grid(row=4, column=3)

        self.formula = tk.Entry(self.master, width=80)
        self.formula.grid(row=0, column=1)
        self.formula.insert(0, 'sin(x)')
        self.tangent_val = tk.Entry(self.master, width=10)
        self.tangent_val.grid(row=5, column=3)
        self.tangent_val.insert(0, 0)

        fig = plt.figure()
        canvas = FigureCanvasTkAgg(fig, master=self.master)
        toolbar = NavigationToolbar2TkAgg(canvas, self.master)
        canvas.get_tk_widget().grid(row=3, column=1)
        toolbar.grid(row=6, column=1)


    def compute_formula(self, accuracy, x_min, x_max):
        """ Compute the formula, based on re, compile and eval """
        self.x = np.arange(float(x_min),
                      float(x_max), accuracy)
        x = self.x
        formula_raw = self.formula.get().replace('e^x', 'exp(x)')
        formula_raw_exp = formula_raw.replace('e^', 'exp')
        formula_list = re.split('(\W)', formula_raw_exp)
        formula_replace = [REPLACE_DIC.get(item,item) for item in formula_list]
        self.formula_finish = ''.join(formula_replace)
        form = parser.expr(self.formula_finish).compile()
        
        try:
            self.y = eval(form)
            self.legend = self.formula.get()
        except NameError:
            self.y = np.sin(self.x)
            self.legend = 'sin(x)'
            
        return (self.x,self.y,self.legend)

    def replot(self):
        """ Clear old plot and draw new one """
        self.compute_formula(0.01,self.get_x_min(),self.get_x_max())
        plt.clf()
        plt.plot(self.x,self.y,label=self.legend)
        plt.grid('on')
        plt.legend()
        plt.gcf().canvas.draw()

    def update(self):
        """ Add new plot to the old one(s) """
        self.compute_formula(0.01,self.get_x_min(),self.get_x_max())
        plt.plot(self.x,self.y, label=self.legend)
        plt.legend()
        plt.gcf().canvas.draw()

    def minima(self):
        """ Calculate the local minimas from the last function """
        self.compute_formula(0.01,self.get_x_min(),self.get_x_max())
        local_min = (np.diff(np.sign(np.diff(self.y))) > 0).nonzero()[0] + 1
        for i in self.x[local_min]:
            for j in self.y[local_min]:
                plt.text(i, j, [float(np.round(i, decimals=3)),
                                float(np.round(j, decimals=3))])
        plt.plot(self.x[local_min], self.y[local_min], "o")
        plt.gcf().canvas.draw()

    def maxima(self):
        """ Calculate the local maximas from the last function """
        self.compute_formula(0.01,self.get_x_min(),self.get_x_max())
        local_max = (np.diff(np.sign(np.diff(self.y))) < 0).nonzero()[0] + 1
        for i in self.x[local_max]:
            for j in self.y[local_max]:
                plt.text(i, j, [float(np.round(i, decimals=3)),
                                float(np.round(j, decimals=3))])
        plt.plot(self.x[local_max], self.y[local_max], "o")
        plt.gcf().canvas.draw()

    def turning_point(self):
        """ Calculate the turning points from the last function """
        self.compute_formula(0.0001,self.get_x_min(),self.get_x_max())
        for i in xrange(1, len(self.y)):
            if self.y[i] < 0 and self.y[i-1] > 0:
                average_y = (self.y[i] + self.y[i-1]) / 2
                average_x = (self.x[i] + self.x[i-1]) / 2
                plt.plot(average_x,average_y,'o')
                plt.text(average_x, average_y, [float(np.round(average_x,
                                                               decimals=3)),
                                                float(np.round(average_y,
                                                               decimals=3))])
                plt.gcf().canvas.draw()
            if self.y[i] > 0 and self.y[i-1] < 0:
                average_y = (self.y[i] + self.y[i-1]) / 2
                average_x = (self.x[i] + self.x[i-1]) / 2
                plt.plot(average_x, average_y, 'o')
                np.set_printoptions(precision=3)
                plt.text(average_x, average_y, [float(np.round(average_x,
                                                               decimals=3)),
                                                float(np.round(average_y,
                                                               decimals=3))])
                plt.gcf().canvas.draw()

    def tangent(self):
        """ Plots the tangent of the last function at an entered point"""
        self.compute_formula(0.0005,float(self.tangent_val.get())-0.0001,
                             float(self.tangent_val.get())+0.0001)
        plt.plot(self.x,self.y,'o')
        np.set_printoptions(precision=3)
        plt.text(self.x, self.y, [float(np.round(self.x, decimals=3)),
                                  float(np.round(self.y, decimals=3))])
        #plt.gcf().canvas.draw()
        self.differentiate(self.tangent_val.get())
        #angle = np.arctan(float(self.slope))
        plt.plot([self.x+1,self.x-1],[self.y+self.slope,self.y-self.slope])
        #plt.plot([1,2],[1,2])
        plt.gcf().canvas.draw()
        
        
    def differentiate(self, val):
        """ Calculates the differential for plotting the tangent """
        x = sp.Symbol('x')
        formula = self.formula_finish
        form = self.formula_finish.replace('np.', '')
        sympy_exp = parse_expr(form)
        df = sympy_exp.diff(x)
        self.slope = df.evalf(subs={x:val})   
        
    def set_x_min(self, val):
        """ Set x-min value with the slider """
        value = int(float(val))
        self.x_min.set(value)

    def get_x_min(self):
        """ Return x-min value """
        return self.x_min.get()

    def set_x_max(self, val):
        """ Set x-max value with the slider """
        value = int(float(val))
        self.x_max.set(value)

    def get_x_max(self):
        """ Return x-max value """
        return self.x_max.get()
        
    def instructions(self):
        """ Opens a info-window and shows the content of usage.txt """
        instruction = open('usage.txt').read()
        showinfo(title='Usage', message=instruction)


def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()


if __name__ == '__main__':
    main()
