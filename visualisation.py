# file to visualise all data produced from a SINGLE simulation run
# TODO: include support for ensemble runs

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# load in data from the history_logs dictionary
with open("data/history_logs.dat","r") as rfile:
    history_logs_list = [eval(k) for k in rfile] # one dict on each line

class TimeSeries(object):
    def __init__(self, series_list, title="",xlabel="Time", colour='k', axlst=None, fig=None):
        self.series_list = series_list
        self.size = len(series_list)
        self.xlabel = xlabel
        self.title = title
        self.timesteps = [t for t in range(series_list[0][0])] # assume all data series are the same size
        if axlst and fig:
            self.axlst = axlst
            self.fig = fig
        else:
            self.fig, self.axlst = plt.subplots(self.size,sharex=True)

        self.plot() # we create the object when we want the plot so call plot() in the constructor

    def plot(self):
        for series, series_label, i in enumerate(series_list):
            self.axlst[i].plot(self.timesteps, series,color=colour)
            self.axlst[i].set_ylabel(series_label)
        self.axlst[self.size-1].set_xlabel(self.xlabel)
        self.fig.suptitle(self.title)
        return self.fig, self.axlst

    def save(self, filename):
        self.fig.savefig("{filename}".format(filename=filename))
        return

class InsuranceFirmAnimation(object):
    '''class takes in a run of insurance data and produces animations '''
    def __init__(self, data):
        self.data = data
        self.fig, self.ax = plt.subplots()
        self.stream = self.data_stream()
        self.ani = animation.FuncAnimation(self.fig, self.update, repeat=False, interval=100,)
                                           #init_func=self.setup_plot)

    def setup_plot(self):
        # initial drawing of the plot
        casharr,idarr = next(self.stream)
        self.pie = self.ax.pie(casharr, labels=idarr,autopct='%1.0f%%')
        return self.pie,

    def data_stream(self):
        # unpack data in a format ready for update()
        for timestep in self.data:
            casharr = []
            idarr = []
            for (cash, id, operational) in timestep:
                if operational:
                    casharr.append(cash)
                    idarr.append(id)
            yield casharr,idarr

    def update(self, i):
        # clear plot and redraw
        self.ax.clear()
        self.ax.axis('equal')
        casharr,idarr = next(self.stream)
        self.pie = self.ax.pie(casharr, labels=idarr,autopct='%1.0f%%')
        self.ax.set_title("Timestep : {:,.0f} | Total cash : {:,.0f}".format(i,sum(casharr)))
        return self.pie,

    def save(self,filename):
        self.ani.save(filename, writer='ffmpeg', dpi=80)

    def show(self):
        plt.show()

class visualisation(object):
    def __init__(self, history_logs_list):
        self.history_logs_list = history_logs_list
        # unused data in history_logs
        #self.excess_capital = history_logs['total_excess_capital']
        #self.reinexcess_capital = history_logs['total_reinexcess_capital']
        #self.diffvar = history_logs['market_diffvar']
        #self.cumulative_bankruptcies = history_logs['cumulative_bankruptcies']
        #self.cumulative_unrecovered_claims = history_logs['cumulative_unrecovered_claims']
        return

    def insurer_pie_animation(self, run=0):
        data = self.history_logs_list[run]
        insurance_cash = np.array(data['insurance_firms_cash'])
        self.ins_pie_anim = InsuranceFirmAnimation(insurance_cash)
        return self.ins_pie_anim

    def reinsurer_pie_animation(self, run=0):
        data = self.history_logs_list[run]
        reinsurance_cash = np.array(data['reinsurance_firms_cash'])
        self.reins_pie_anim = InsuranceFirmAnimation(reinsurance_cash)
        return self.reins_pie_anim

    def insurer_time_series(self, runs=None, axlst=None, fig=None, title="Insurer", colour='black'):
        # runs should be a list of the indexes you want included in the ensemble for consideration
        if runs:
            data = [self.history_logs_list[x] for x in runs]
        else:
            data = self.history_logs_list
        
        # Take the element-wise means/medians of the ensemble set (axis=0)
        contracts = np.mean([history_logs['total_contracts'] for history_logs in self.history_logs_list],axis=0)
        profitslosses = np.mean([history_logs['total_profitslosses'] for history_logs in self.history_logs_list],axis=0)
        operational = np.median([history_logs['total_operational'] for history_logs in self.history_logs_list],axis=0)
        cash = np.median([history_logs['total_cash'] for history_logs in self.history_logs_list],axis=0)
        premium = np.median([history_logs['market_premium'] for history_logs in self.history_logs_list],axis=0)

        self.ins_time_series = TimeSeries([
                                        (contracts, 'Contracts')
                                        (profitslosses, 'Profitslosses')
                                        (operational, 'Operational') 
                                        (cash, 'Cash') 
                                        (premium, "Premium")
                                        ],title=title, xlabel = "Time", axlst=axlst, fig=fig, color=colour)
        return self.ins_time_series

    def reinsurer_time_series(self, runs=None, axlst=None, fig=None, title="Reinsurer", colour='black'):
        # runs should be a list of the indexes you want included in the ensemble for consideration
        if runs:
            data = [self.history_logs_list[x] for x in runs]
        else:
            data = self.history_logs_list

        # Take the element-wise means/medians of the ensemble set (axis=0)
        reincontracts = np.mean([history_logs['total_reincontracts'] for history_logs in self.history_logs_list],axis=0)
        reinprofitslosses = np.mean([history_logs['total_reinprofitslosses'] for history_logs in self.history_logs_list],axis=0)
        reinoperational = np.median([history_logs['total_reinoperational'] for history_logs in self.history_logs_list],axis=0)
        reincash = np.median([history_logs['total_reincash'] for history_logs in self.history_logs_list],axis=0)
        catbonds_number = np.median([history_logs['total_catbondsoperational'] for history_logs in self.history_logs_list],axis=0)

        self.reins_time_series = TimeSeries([
                                        (reincontracts, 'Contracts')
                                        (reinprofitslosses, 'Profitslosses')
                                        (reinoperational, 'Operational') 
                                        (reincash, 'Cash') 
                                        (catbonds_number, "Active Cat Bonds")
                                        ],title= title, xlabel = "Time", axlst=axlst, fig=fig, color=colour)
        return self.reins_time_series

    def metaplotter_timescale(self):
        # Take the element-wise means/medians of the ensemble set (axis=0)
        contracts = np.mean([history_logs['total_contracts'] for history_logs in self.history_logs_list],axis=0)
        profitslosses = np.mean([history_logs['total_profitslosses'] for history_logs in self.history_logs_list],axis=0)
        operational = np.median([history_logs['total_operational'] for history_logs in self.history_logs_list],axis=0)
        cash = np.median([history_logs['total_cash'] for history_logs in self.history_logs_list],axis=0)
        premium = np.median([history_logs['market_premium'] for history_logs in self.history_logs_list],axis=0)
        reincontracts = np.mean([history_logs['total_reincontracts'] for history_logs in self.history_logs_list],axis=0)
        reinprofitslosses = np.mean([history_logs['total_reinprofitslosses'] for history_logs in self.history_logs_list],axis=0)
        reinoperational = np.median([history_logs['total_reinoperational'] for history_logs in self.history_logs_list],axis=0)
        reincash = np.median([history_logs['total_reincash'] for history_logs in self.history_logs_list],axis=0)
        catbonds_number = np.median([history_logs['total_catbondsoperational'] for history_logs in self.history_logs_list],axis=0)
        return

    def show(self):
        plt.show()
        return

class compare_riskmodels(object):
    def __init__(vis_list, colour_list):
        # take in list of visualisation objects and call their plot methods
        self.vis_list = vis_list
        self.colour_list = colour_list
        
    def create_insurer_timeseries():
        # create the time series for each object in turn and superpose them?
        fig = axlst = None
        for vis,colour in zip(vis_list, colour_list):
            fig, axlst = vis.insurer_time_series(fig=fig, axlst=axlst, colour) # pass in an optional axis argument, to superpose plots
    def show():
        plt.show()
    def save():
        # logic to save plots
        pass
    
# first create visualisation object, then create graph/animation objects as necessary
vis = visualisation(history_logs_list)
#vis.insurer_pie_animation()
#vis.reinsurer_pie_animation()
#vis.insurer_time_series().save("insurer_time_series.pdf")
#vis.reinsurer_time_series().save("reinsurer_time_series.pdf")
N = len(history_logs_list)

# for each run, generate an animation and time series for insurer and reinsurer
# TODO: provide some way for these to be lined up nicely rather than having to manually arrange screen
for i in range(N):
    vis.insurer_pie_animation(run=i)
    vis.insurer_time_series(runs=[i])
    vis.reinsurer_pie_animation(run=i)
    vis.reinsurer_time_series(runs=[i])
    vis.show()

vis_list = [vis1,vis2,vis3,vis4]
colour_list = ['blue', 'yellow', 'red', 'green']
cmp_rsk = compare_riskmodels(vis_list, colour_list)
cmp_rsk.create_insurer_timeseries()
cmp_rsk.show()
