import glob
import json
import re
import numpy as np
import matplotlib.pyplot as plt

metricProps = {
    'messageID': '',
    'originatorHostID': '',
    'totalNanoTime': '',
    'lastDeliveryHop': '',
}


class Metric(object):
    def __init__(self, props=metricProps):
        self.messageID = props['messageID']
        self.originatorHostID = props['originatorHostID']
        self.totalNanoTime = int(props['totalNanoTime'])
        self.lastDeliveryHop = float(props['lastDeliveryHop'])


def graph_dissemination_hist(path=None, figlabel=0, limits=None):
    """ Graph a histogram of message dissemination times. Use a wildcard in
    path overlay multiple test results of a series into one graph. Example:
    `path=phase1_processed_data/analysis2*` for series 2. ``limits`` sets the
    x-axis limits.

    Returns:
        fig -- matplotlib figure
        ax  -- matplotlib axes
    """

    if path is None:
        pubsubAnalysisFiles = glob.glob('*.json')
    else:
        pubsubAnalysisFiles = glob.glob('{}'.format(path))
        pubsubAnalysisFiles.sort()

    fig, ax = plt.subplots(num=figlabel)

    for pubsubAnalysisFile in pubsubAnalysisFiles:
        print(pubsubAnalysisFile)
        nanoTimes = []
        ldh = []

        with open(pubsubAnalysisFile) as json_file:
            data = json.load(json_file)
            for metric in data:
                m = Metric(metric)

                nanoTimes.append(m.totalNanoTime)
                ldh.append(m.lastDeliveryHop)

        plt.hist(nanoTimes, bins='auto', histtype='step')
    phaseNum = re.search('(?<=phase)(\w{1})', path)
    seriesNum = re.search('(?<=\/analysis)(\w{1})', path)
    plt.title("Phase {} Series {}\n"
              .format(phaseNum.group(0), seriesNum.group(0)) + "Histogram of" +
              " Message Dissemination Times (Total Nano Times)")
    plt.xlabel('Dissemination Time (ns)')
    plt.ylabel('Number of Messages')

    if limits is not None:
        ax.set_xlim(limits)

    ax.ticklabel_format(style='sci', axis='x', scilimits=(9, 9))
    ax_top = ax.twiny()
    ax_top.set_xlabel('Dissemination Time (ms)')
    low, high = ax.get_xlim()
    ax_top.set_xlim(low * 1e-6, high * 1e-6)
    ax.legend(['Test A', 'Test B', 'Test C', 'Test D'])

    fig.tight_layout()

    return fig, ax


def graph_cum_and_compute_metrics(filename=None, fig=0, save=False):
    nanoTimes = []
    ldh = []

    if filename is None:
        pubsubAnalysisFiles = glob.glob('*.json')
    else:
        pubsubAnalysisFiles = sorted(glob.glob('{}'.format(filename)))

    for pubsubAnalysisFile in pubsubAnalysisFiles:

        with open(pubsubAnalysisFile) as json_file:
            data = json.load(json_file)
            for metric in data:
                m = Metric(metric)

                nanoTimes.append(m.totalNanoTime)
                ldh.append(m.lastDeliveryHop)

    fig1, ax1 = plt.subplots(num=fig)

    nanoTimesArr = np.asarray(nanoTimes)
    counts, bin_edges = np.histogram(nanoTimesArr, bins=2000, density=True)
    cdf = np.cumsum(counts)
    plt.plot(bin_edges[1:], cdf / cdf[-1], label='_nolegend_')
    vline_1 = np.percentile(nanoTimesArr, 50)
    vline_2 = np.percentile(nanoTimesArr, 99)
    m = re.search('(?<=\/analysis)(\w{2})', filename)
    phaseNum = re.search('(?<=phase)(\w{1})', filename)
    plt.title("Phase {} Series {} Cumulative Distribution of Dissemination "
              .format(phaseNum.group(0), m.group(0)) + "Times")
    ax1.set_xlabel('Dissemination Time (ns)')
    ax1.set_ylabel('Percent of Messages')
    ax1_top = ax1.twiny()
    ax1_top.set_xlabel('Dissemination Time (ms)')
    ax1.ticklabel_format(style='sci', axis='x', scilimits=(9, 9))
    low, high = ax1.get_xlim()
    ax1_top.set_xlim(low * 1e-6, high * 1e-6)
    ax1.axvline(vline_1, label='v1', linestyle='--', color='k')
    ax1.axvline(vline_2, label='v2', linestyle='--', color='r')
    ax1.legend(['50%  within {0:.1f}ms'.format(vline_1 * 1e-6),
                '99%  within {0:.1f}ms'.format(vline_2 * 1e-6)])

    fig1.tight_layout()

    if save is True:

        fig1.savefig('phase{}_series{}_cumulative_dis.png'
                     .format(phaseNum.group(0), m.group(0)))

    nanoMean = np.mean(nanoTimes)
    nanoMedian = np.median(nanoTimes)
    nanoStd = np.std(nanoTimes)

    ldhMean = np.mean(ldh)
    ldhMedian = np.median(ldh)
    ldhStd = np.std(ldh)

    print('Messages published: {}'.format(len(nanoTimes)))
    print('Total Nano Times - mean: {}, median: {}, std: {}'
          .format(nanoMean, nanoMedian, nanoStd))
    print('Last Delivery Hop - mean: {}, median: {}, std: {}'
          .format(ldhMean, ldhMedian, ldhStd))


def graph_series_cum_dist(dirname=None, starting_figlabel=0):
    """Graphs message dissemination cumulative distribution for an entire
    series. ``starting_figlabel`` is the starting integer label for the graphs.
    """
    if dirname is None:
        print("missing dirname")
        return

    num = starting_figlabel
    files = glob.glob(filename)
    files.sort()
    for file in files:
        print("\n\nfile:" + file)
        graph_cum_and_compute_metrics(file, num, save=True)
        num += 1


filename = 'phase2_processed_data/analysis1*'

# graph all message dissemination histograms of a series
fig, ax = graph_dissemination_hist(filename, figlabel=0,
                                   limits=(-0.050e9, 0.5e9))
seriesNum = re.search('(?<=\/analysis)(\w{1})', filename)
phaseNum = re.search('(?<=phase)(\w{1})', filename)
fig.savefig('phase{}_series{}_dissemination_times.png'
            .format(phaseNum.group(0), seriesNum.group(0)))

# graph all message dissemination cumulative distributions of a series
graph_series_cum_dist(filename, 1)

# graph entire phase into a single graph
graph_dissemination_hist('phase2_processed_data/analysis*', figlabel=5,
                         limits=(-0.050e9, 3e9))

plt.show()
