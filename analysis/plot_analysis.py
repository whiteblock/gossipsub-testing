import glob
import json
import re
import sys
import numpy as np
import matplotlib.pyplot as plt
# change this to your virtualenv path
sys.path.append('../../venv/gs-test/lib/python3.6/site-packages')

# %matplotlib inline

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


def computeMetricsHist(filename=None, fig=0):

    if filename is None:
        pubsubAnalysisFiles = glob.glob('*.json')
    else:
        pubsubAnalysisFiles = glob.glob('{}'.format(filename))
        pubsubAnalysisFiles.sort()

    fig2, ax2 = plt.subplots(num=fig)

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

    plt.title("Histogram of Message Dissemination Times (Total Nano Times)")
    plt.xlabel('Dissemination Time (ns)')
    plt.ylabel('Number of Messages')
    ax2.ticklabel_format(style='sci', axis='x', scilimits=(9, 9))
    ax2_top = ax2.twiny()
    ax2_top.set_xlabel('Dissemination Time (ms)')
    low, high = ax2.get_xlim()
    ax2_top.set_xlim(low * 1e-6, high * 1e-6)
    ax2.legend(['Test A', 'Test B', 'Test C', 'Test D'])
    fig2.tight_layout()
    return fig2, ax2


def computeMetricsCum(filename=None, fig=0):
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
    vline_1 = np.percentile(nanoTimesArr, 51)
    vline_2 = np.percentile(nanoTimesArr, 99)
    plt.title("Cumulative Distribution of Dissemination Times")
    ax1.set_xlabel('Dissemination Time (ns)')
    ax1.set_ylabel('Percent of Messages')
    ax1_top = ax1.twiny()
    ax1_top.set_xlabel('Dissemination Time (ms)')
    ax1.ticklabel_format(style='sci', axis='x', scilimits=(9, 9))
    low, high = ax1.get_xlim()
    ax1_top.set_xlim(low * 1e-6, high * 1e-6)
    ax1.axvline(vline_1, label='v1', linestyle='--', color='k')
    ax1.axvline(vline_2, label='v2', linestyle='--', color='r')
    print(ax1.lines)
    ax1.legend(['51%  within {0:.1f}ms'.format(vline_1 * 1e-6),
                '99%  within {0:.1f}ms'.format(vline_2 * 1e-6)])
    fig1.tight_layout()

    m = re.search('(?<=\/analysis)(\w{2})', filename)
    fig1.savefig('phase2_series{}_cumulative_dis.png'.format(m.group(0)))

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

num = 0
filename = 'analyzed_results_json/analysis6*'
fig, ax = computeMetricsHist(filename, num)
m = re.search('(?<=\/analysis)(\w{1})', filename)
fig.savefig('phase2_series{}_dissemination_times.png'.format(m.group(0)))

num += 1
files = glob.glob(filename)
print(files)
files.sort()
for file in files:
    try:
        print("\n\nfile:" + file)
        computeMetricsCum(file, num)
    except KeyError:
        # not sure why this is happening
        print("relativeMessageRedundancy key error, skipping analysis")
    num += 1

# plt.show()
