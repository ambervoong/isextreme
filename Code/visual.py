from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import random
from PyQt5.QtWidgets import QSizePolicy

import io
from collections import Counter
from wordcloud import WordCloud
import numpy as np
import pandas as pd


class PlotCanvas(FigureCanvas):
    FILEPATH = './input_data/tweets.csv'
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        # self.plot()

    def plot(self):
        #self.axes = self.fig.add_subplot(111)
        data = [random.random() for i in range(25)]
        ax = self.figure.add_subplot(111)
        ax.plot(data, 'r-')
        ax.set_title('PyQt Matplotlib Example')
        self.draw()

    def plotWord(self): # Generate a wordcloud.
        train = pd.read_csv(PlotCanvas.FILEPATH, encoding='utf8')
        train["cleaned"].fillna('', inplace=True)

        x = np.array(train["cleaned"])
        words = ' '.join(x)

        word_cloud = WordCloud(width=1600, height=800,
                               font_path='./Symbola.ttf').generate(words)

        ax = self.figure.add_subplot(111)
        ax.imshow(word_cloud)
        ax.axis("off")
        #plt.imshow(word_cloud)
        #plt.axis("off")
        #plt.show()
        self.draw()
