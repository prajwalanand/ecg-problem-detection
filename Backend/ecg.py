import wfdb
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
#import matplotlib.pyplot as plt
#plt.ioff()
#plt.axis('off')
import os

out_dir = 'plots/'
db_dir = 'db/'

interval = 1000
steps = 500

for root, dirs, files in os.walk(db_dir):
    ecg_files = list(set([x.split(".")[0] for x in files]))
    for file in ecg_files:
        print(file)
        record = wfdb.rdrecord(db_dir+file)
        signal = record.p_signal[0:len(record.p_signal)-(len(record.p_signal)%interval), 0]
        #print(len(signal))
        for i in range(0, len(signal), steps):
            fig = Figure()
            canvas = FigureCanvas(fig)
            ax_left = fig.add_subplot(111)
            ax_left.axis('off')
            ax_left.plot(signal[i:i+interval], color='#3979f0', label='Signal')
            fig.savefig(out_dir+file+'_'+str(i//steps)+'.png')