# Eth2 - LibP2P Gossipsub Testing

### Overview
The purpose of this initiative is to test the performance of Libp2p gossipsub protocol implementations. With time constraints present in Eth2, it is important to verify that messages will be able to be disseminated throughout the network in a timely manner. This effort is supported by an [Eth2.0 Grant co-funded by the Ethereum Foundation and ConsenSys](https://blog.ethereum.org/2019/08/26/announcing-ethereum-foundation-and-co-funded-grants/).


## Community Feedback

We invite all community members interested in providing feedback to visit our discourse on this topic at the following link: https://community.whiteblock.io/t/gossipsub-tests/17/10.

## Table of Contents
- [Introduction - Understanding Testing Scope](#Introduction-Understanding-Testing-Scope)
    - [Important Test Parameter Constants](#Important-Test-Parameter-Constants)
    - [System Specifications](#System-Specifications)
    - [Resource Allocation Motivation](#Resource-Allocation-Motivation)
## Introduction - Understanding Testing Scope

This document presents the first round of results of Whiteblock’s testing and analysis of the libp2p-gossipsub protocol under random topologies with different degree distributions generated using the [Barabasi-Albert (B-A) model](https://en.wikipedia.org/wiki/Barab%C3%A1si%E2%80%93Albert_model). Tests were run using the Whiteblock Genesis platform within a single cloud instance (see System Specifications). Here, a gossip node, or simply “node,” shall specifically refer to a container that participates in the gossip network as a libp2p host. The total memory of the instance was 360GB. For all tests in this report, the parameters of libp2p-gossipsub were left at default (e.g. GossipSubD=6).

While we understand the Ethereum 2.0 network is slated to consist of a much larger network size with nodes acting within several logical roles (e.g. validator), the intent of these tests were to analyze and benchmark the performance of the libp2p-gossipsub implementation. As such, it is important to emphasize overall trends in the results as opposed to individual values presented within the results themselves.

### Important Test Parameter Constants

Presented below is a list of the primary test parameters for consideration. Messages are generated globally. That is, for each message, a random node is selected to be the source node. The purpose of the warm-up time is to allow for the loading of containers and programs as well as the instantiation of topological connections. Nodes that complete warm-up remain idle until the test begins. The “Test Time” indicates the interval at which nodes generate gossip messages. When the test time is elapsed, the nodes continue operating until the “Cool-Down Time” is complete. The purpose of the cool-down period is to allow for any internal queues to empty. All nodes published and subscribed to a single topic.

- Gossip Nodes: 95
- Global Msg/Sec: 200
- Warm-up Time: 60s
- Test Time: 180s
- Cool-Down Time: 600s
- Msg Size: 1000 bytes
- Discovery (mDNS): Off
- Routing: Off
- Security: SECIO
- Peering: Barabasi-Albert (seed=42, varying input degree - parameters)  - { 2, 6, 12, 16 }

The remainder of this document is organized as follows. We have written a full analysis of the test results and readers should jump to the graphs and test result statistics section of each test number as a reference.

### System Specifications

| Resource | Allocation | 
| --------  | --------  |
| CPU op-mode(s) | 32-bit, 64-bit |
| CPU(s) | 96 |
| Thread(s) per core |2 |
| Core(s) per socket|24|
| Socket(s) | 2 |
| Model name | Intel(R) Xeon(R) CPU @ 2.00GHz |
| CPU MHz | 2000.168 |
| L1d cache | 32K |
| L1i cache | 32K |
| L2 cache | 1024K |
| L3 cache | 39424K |
| Memory block size | 1G |
| Total online memory | 360G |

Table 1 - System Specifications

### Resource Allocation Motivation

In the [prior study](https://github.com/whiteblock/p2p-tests), results showed high CPU utilization when running the `go-libp2p-daemon` in a Docker containers with one CPU allocated per node. In addition, a [preliminary study](https://github.com/protolambda/go-libp2p-gossip-berlin) showed that SHA-256 and general secio cryptography are the largest resource consumers when using `libp2p-gossipsub`. To address these issues, we will use a direct libp2p host implementation and log resource consumption (cpu, memory, and I/O) to ensure CPU usage is not a bottleneck in the performance of `libp2p-gossipsub`.

## Understanding Test Phases and Series

### Phases

This research effort is split into test phases to illustrate to the community the progress and results of this effort over time. The intent of phases is to release results iteratively and to engage the community. After each phase, community feedback is gathered and additional features are integrated into the next phase to enhance results based on this community feedback.

### Series

Within each phase, there will be a series of tests, each with a theme such as bandwidth variation and packet loss variation.

### Link: Google Doc with All Results

To help readability, all testing results have been compiled and organized into the Google Sheet linked below. 

- [Gossipsub Testing Results Compilation](https://docs.google.com/spreadsheets/d/1ZoY8Rz-BqKiX-ik9Wdd-zfR0mcoOj_CYUSz8tSwtb6w/edit#gid=0)

## Testing Metrics

In [[2]](#References), Leitao et. al present the following metrics to evaluate gossip protcols. The test metrics are collected and analyzed using the tools provided in `agencyenterprise/go-libp2p-pubsub-benchmark-tools`, and the description below is taken directly from the same repository.

The metrics computed are:
1. **TotalNanoTime** - the time (in nano seconds) for the message to propogate the network
2. **LastDeliveryHop** - the hop count of the last message that is delivered by a [pubsub] protocol or, in other words, is the maximum number of hops that a message must be forwarded in the overlay before it is delivered.

## Network Topology Generation

To evaluate the performance and reliability of the gossipsub protocol, we test the host-client implementation against two types of topologies: fully connected and random-connected using the [Barabasi-Albert (B-A)](https://en.wikipedia.org/wiki/Barab%C3%A1si%E2%80%93Albert_model) model. While these topologies may present an oversimplification, it is unclear what the resulting topologies of Eth2 due to large contingency on the final discovery service protocol deployed. Thus, this research effort will attempt to test gossipsub in a fully connected network as well as random topologies generated by known methods in order to evaluate gossipsub's performance.

#### Random Scale-Free Network Topology (Barabasi-Albert or B-A):

In 1999, Barabasi and Albert observed that the world wide web exhibited a scale-free nature and preferential attachment. Scale-free networks follow a power-law degree distribution, and preferential attachment describes the likelihood of a node connecting to nodes with high degrees. Inspired by this Barabasi-Albert (B-A) model was created to generate random network topologies with both a power-law degree distribution and preferential attachment. As described by Albert-Barabasi in [[3]](#References) topology generation is "grown" starting with a small number $m_0$ of nodes. At each time step, a new node with *m &le; m<sub>0</sub>* edges that link the new node to $m$ different nodes currently present in the network. *m* is the *input degree parameter*. When choosing nodes, the probability *&Pi;* that a new node will connect to some node $i$ depends on the degree *k<sub>i</sub>* of node *i* such that:

<a align="center" href="https://www.codecogs.com/eqnedit.php?latex=\fn_jvn&space;\Pi(k_i)&space;=&space;\frac{k_{i}}{\sum_{j}&space;k_{j}}" target="_blank"><img src="https://latex.codecogs.com/png.latex?\fn_jvn&space;\Pi(k_i)&space;=&space;\frac{k_{i}}{\sum_{j}&space;k_{j}}" title="\Pi(k_i) = \frac{k_{i}}{\sum_{j} k_{j}}" /></a>

Network topologies for testing are generated using the [NetworkX](https://networkx.github.io/) python library with a constant seed to make results reproducible. More specifics about the topology used are in explained in each Phase section.

## Phase 1 Testing and Results

### Phase 1 Setup Summary

For all tests, each node will use a fork of the following host and client implementation will be used: https://github.com/agencyenterprise/go-libp2p-pubsub-benchmark-tools. This implementation includes tools for generating messages at each node and analysis tools for parsing and plotting metrics described in the next section. The fork consists only of modified configuration files.

### Phase 1 Test Series

| Topology | Series 1a | Series 1b | Series 1c | Series 1d |
| -------- | ------ | ------ | ------ | ------ |
| Network Latency (ms) | 0 | 0 | 0 | 0 |
| Packet Loss (%) | 0 | 0 | 0 | 0 |
| Bandwidth (MB) | 1000 | 1000 | 1000 | 1000 |
| Total Nodes | 95 | 95 | 95 | 95
| Message Size (B) | 1000 | 1000 | 1000 | 1000 |
| Network-Wide Message Rate (msgs/s) | 200 | 200 | 200 | 200 |
| Topology | B-A | B-A | B-A | B-A |
| Input Deg. Param. | 2 | 6 | 12 | 16 |

### Message Delivery Ratio (MDR) Results

The primary observation of concern within Phase 1 tests was the message delivery ratio, or packet delivery ratio, was not 100%. At a message rate of 200 msgs/sec, we expected 36,000 messages to be generated per test. At lower message rates, the delivery ratio was 100%. In Test Series 1a, the number of messages received was 25365/30000 (70.4%) or a drop rate of ~30%. Further analysis verified that the dropped packets were not a result of insufficient cool-down time. This was verified using two methods. The first was processing the logs of each individual node to see if messages were still being gossipped prior to the tests shutting down. The logs indicated that each message ID was received 95 times (i.e., once per node with no messages in-transit). To further account for this, the second method was to run a test with a two hour cool-down time. This second method also yielded the same results, implying the drop rate caused by either the protocol itself or the test client implementation.

##### MDR Fix #1 for Phase 2 - Outbound Peer Queue Size

The first diagnosis of this problem was that the saturated network of gossip messages caused overflows of internal Golang channel queues. The go-libp2p-pubsub community provided a possible fix by adding a feature to change peer outbound channel queue size in the following pull request. The corresponding Godoc is also linked below.

* https://github.com/libp2p/go-libp2p-pubsub/pull/230
* https://godoc.org/github.com/libp2p/go-libp2p-pubsub#WithPeerOutboundQueueSize

After rerunning the tests which implemented this first fix in the test client, the message loss was reduced, however preliminary results still indicated a loss rate of ~22% (as opposed to ~30%). Fix #2 below and other changes introduced before Phase 2 successfully addressed the message loss issue. Further details are presented in section “[Phase 2 Testing and Results](#Phase-2-Testing-And-Results)”.

##### MDR Fix #2 for Phase 2 - Testing Logic Refactor

Traffic generation is orchestrated by a container separate from all gossiping nodes called the “Orchestra”. The Orchestra uses RPCs to instruct gossiping nodes to transmit a new message. In the initial implementation of Orchestra in [agencyenterprise/go-libp2p-pubsub-benchmark-tools](https://github.com/agencyenterprise/go-libp2p-pubsub-benchmark-tools), the testing logic timed messages via a Golang ticker set to tick at the intended intermessage interval (e.g. 5ms).The ticker was enabled only during the duration of the test, not during warmup or cooldown. Further analysis of the test logs demonstrated that not all ticks were successfully executed before the end of the test. To fix this, Orchestra was refactored in a fork of [agencyenterprise/go-libp2p-pubsub-benchmark-tools](https://github.com/agencyenterprise/go-libp2p-pubsub-benchmark-tools) to continue tests until the expected number of messages in a test  sent. The expected number of messages is calculated by taking the test duration and dividing it by the intermessage interval. The refactoring commit to make Orchestra send a defined number of messages is in the link below. This fork of the original repository agencyenterprise/go-libp2p-pubusub-benchmark-tools serves as the code used for Phase 2 and onward.

* https://github.com/whiteblock/go-libp2p-pubsub-benchmark-tools

Phase 2 results demonstrate that MDR Fix #1 and #2 successfully addressed the message loss issue. 

### Total Time to Dissemination (“Total Nano Time”)

In the test scenarios, the distribution graphs of total nano times included an initial spike followed by several “lobes” in a shape similar to a poisson distribution. One interesting result is the lobes in preliminary test runs where the message interval rate was 20msg/sec were absent. The distribution of total nano times followed a poisson distribution. Below is a graph which overlays all tests 1a-1d to illustrate the graphs in Sections III-VI appear to have varying lobe heights due to different Y-axis ranges

TODO: Graph 1 histogram

For each increase in B-A degree inputs, the initial spike of short nano times and heights of the first lobe did not follow a particular trend. The peaks of the initial spikes in tests 1a, 1b, 1c, and 1d are approximately 5650, 3950, 3550 and 2850, respectively. The peaks of the first lobe in tests 1a, 1b, 1c, and 1d are approximately 1400, 1500, 1650, and 1650, respectively. It is inconclusive what the effects of degree distributions are on total nano times. The presence of lobes cannot be explained by the GossipSubHeartbeatInterval[3], which is defaulted to 1 second at the time of these tests. The approximate times of the peaks of the spikes followed by the first three lobes are 6 ms, 75 ms, 170 ms, and 266 ms, respectively. These distances are far less than 1 second.

The average nano times (in milliseconds) for tests 1a-1d are 154 ms, 65 ms, 67 ms, 75 ms, respectively. While an input degree parameter of 2 shows larger average nano times (this can also be seen in the higher lobes in the nano time graphs), more statistical evidence is needed to determine if higher degrees of connectivity affect the average nano times using the default gossipsub parameters.

The average time for the messages to be received/propagated in test 1a was the highest and the average time decreased as the “degree of connectivity” increased in subsequent tests. This demonstrates a correlation to the number of messages that have been received. If the full number of messages were properly received, the average time for message propagation would become more skewed.


## Phase 2 Testing and Results

### Phase 2 Summary

* Testing via the Whiteblock Genesis platform
* Libp2p Host implementation (new fork): 
    * https://github.com/whiteblock/go-libp2p-pubsub-benchmark-tools
* Random topologies generated using Barabasi-Albert model
* Includes the implementation of network impairments

### Phase 2 Test Series

### Message Delivery Ratio (MDR)

### Last Delivery Hop Distribution

### Total Time to Dissemination (“Total Nano Time”)

### Configuration
For each set of tests, the corresponding configuration used in running the [`agencyenterprise/go-libp2p-pubsub-benchmark-tools`](https://github.com/agencyenterprise/go-libp2p-pubsub-benchmark-tools) implementation will be posted.

Example host.json:
```
{
  "host": {
    "privPEM": "",
    "transports": ["tcp", "ws"],
    "listens": ["/ip4/0.0.0.0/tcp/3000","/ip4/0.0.0.0/tcp/3001/ws"],
    "rpcAddress": "0.0.0.0:8080",
    "peers": [],
    "muxers": [["yamux", "/yamux/1.0.0"], ["mplex", "/mplex/6.7.0"]],
    "security": "secio",
    "pubsubAlgorithm": "gossip",
    "omitRelay": false,
    "omitConnectionManager": false,
    "omitNATPortMap": false,
    "omitRPCServer": false,
    "omitDiscoveryService": true,
    "omitRouting": true,
    "loggerLocation": ""
  }
}

```

Example orchestra.json:
```
{
  "orchestra": {
    "omitSubnet": true,
    "hostRPCAddressesIfOmitSubnet": [<list-of-IPs>],
    "messageNanoSecondInterval": 100000000,
    "clientTimeoutSeconds": 5,
    "messageLocation": "client.message.json",
    "messageByteSize": 1000,
    "testDurationSeconds": 90,
    "testWarmupSeconds": 10,
    "testCooldownSeconds": 10
  },
  "subnet": {
    "numHosts": 10,
    "pubsubCIDR": "127.0.0.1/8",
    "pubsubPortRange": [3000, 4000],
    "rpcCIDR": "127.0.0.1/8",
    "rpcPortRange": [8080, 9080],
    "peerTopology": "whiteblocks"
  },
  "host": {
    "transports": ["tcp", "ws"],
    "muxers": [["yamux", "/yamux/1.0.0"], ["mplex", "/mplex/6.7.0"]],
    "security": "secio",
    "pubsubAlgorithm": "gossip",
    "omitRelay": false,
    "omitConnectionManager": false,
    "omitNATPortMap": false,
    "omitRPCServer": false,
    "omitDiscoveryService": false,
    "omitRouting": false
  },
  "general": {
    "loggerLocation": ""
  }
}

```

/etc/docker/daemon.json
```
{
        "max-concurrent-uploads":1,
        "storage-driver": "overlay",
        "log-driver":"gcplogs"
}
```

## Testing Procedure
 1.   Provision nodes
 2.   Statically peer each node according to specified topology
 3.   Configure actions and behavior between nodes according to specified test case
 4.   Apply network conditions (if applicable)
 5.   Send messages from specified number of nodes
 6.   Log message data from each node
 7.   Timeout 10 seconds -- we have to make sure we do this
 8.   Make sure all data is saved in proper format
 9.   Backup data locally
 10.  Tear down network
 11.  Parse and aggregate data after each test
 
## Resource Profiling

During each test, a time series of resource utilization captured by `docker stats` will be logged.

## Test Series

For all tests, approximately one CPU shall be allocated for every node. Here, a node is defined as a participant in the gossip network. There will be an additional Docker container beyond the total nodes launched to facilitate the orchestration of the test (see orchestra in `agencyenterprise/go-libp2p-pubsub-benchmark-tools`).

### Series 11: Control Test (Fully Connected)

| Vars | Topology | Case A |
| ---- | -------- | ------ |
|  | Network Latency (ms) | 0 |
|  | Packet Loss (%) | 0 |
|  | Bandwidth (MB) | 1000 |
|  | Total Nodes | 95 |
|  | Message Size (B) | 1000 |
|  | Network-wide Message Rate (msgs/s) | 200 |
|  | Topology | Fully Connected|

### Series 21: 
| Vars | Topology | Case A | Case B | Case C | Case D |
| ---- | -------- | ------ | ------ | ------ | ------ |
|  | Network Latency (ms) | 0 | 0 | 0 | 0 |
|  | Packet Loss (%) | 0 | 0 | 0 | 0 |
|  | Bandwidth (MB) | 1000 | 1000 | 1000 | 1000 |
|  | Total Nodes | 95 | 95 | 95 | 95
|  | Message Size (B) | 1000 | 1000 | 1000 | 1000 |
|  | Network-wide Message Rate (msgs/s) | 200 | 200 | 200 | 200 |
|  | Topology | B-A | B-A | B-A | B-A |
|  | Input Deg. Param. | 2 | 6 | 12 | 16 |

## References



[1] R. Bakhshi, F. Bonnet, W. Fokkink, and B. Haverkort, “Formal analysis techniques for gossiping protocols,”SIGOPS Oper. Syst.Rev., vol. 41, no. 5, pp. 28–36, Oct. 2007.

[2] J. Leitão, J. Pereira, and L. Rodrigues, “Epidemic broadcast trees,” Proc. IEEE Symp. Reliab. Distrib. Syst., pp. 301–310, 2007.

[3] R.  Albert  and  A.-L.  Barabasi,  “Statistical  mechanics  of  complex  networks,”Reviews of Modern Physics, vol. 74, no. 1, p. 47–97, Jan 2002.

[4] A. Montresor, “Gossip and epidemic protocol,” Wiley Encyclopedia of Electrical and Electronics Engineering, vol. 1, 2017.

[5] eth2 phase 0 networking requirements, "https://notes.ethereum.org/zgzMxFNiSF-iW5wA5uKH0Q?view"
