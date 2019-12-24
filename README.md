# Eth2 - LibP2P Gossipsub Testing

### Overview
The purpose of this initiative is to test the performance of the libp2p gossipsub implementation. With time constraints present in Eth2, it is important to verify that messages will be able to be disseminated throughout the network in a timely manner. This effort is supported by an [Eth2.0 Grant co-funded by the Ethereum Foundation and ConsenSys](https://blog.ethereum.org/2019/08/26/announcing-ethereum-foundation-and-co-funded-grants/).


## Community Feedback

We invite all community members interested in providing feedback to visit our discourse on this topic at the following link: https://community.whiteblock.io/t/gossipsub-tests/17/10.

## Table of Contents
- [Introduction - Understanding Testing Scope](#Introduction-Understanding-Testing-Scope)
    - [Important Test Parameter Constants](#Important-Test-Parameter-Constants)
    - [System Specifications](#System-Specifications)
- []()
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

## Implementation Details

Overview:
- Testing via Whiteblock Genesis platform
- Uses libp2p gossipsub host implementation
    - https://github.com/libp2p/go-libp2p-pubsub
- Incorporates profiling tools
    - pprof
    - callgrind

### Resourcing 
| Resource Allocation  |
| --------  | --------  |
| CPU Resources Per Node: __number_of_cpu__ |  |
| Memory Resources Per Node: __number_of_ram__ |  |
| Total CPU: __total_cpus__ |  |
| Total Memory: __total_memory__ |  |

In the [prior study](https://github.com/whiteblock/p2p-tests), results showed high CPU utilization when running the `go-libp2p-daemon` in a Docker containers with one CPU allocated per node. In addition, a [preliminary study](https://github.com/protolambda/go-libp2p-gossip-berlin) showed that SHA-256 and general secio cryptography are the largest resource consumers when using `libp2p-gossipsub`. To address these issues, we will use a direct libp2p host implementation and log resource consumption (cpu, memory, and I/O) to ensure CPU usage is not a bottleneck in the performance of `libp2p-gossipsub`.

### Host and Client Implementation

For all tests, each node will use a fork of the following host and client implementation will be used: https://github.com/agencyenterprise/go-libp2p-pubsub-benchmark-tools. This implementation includes tools for generating messages at each node and analysis tools for parsing and plotting metrics described in the next section. The fork consists only of modified configuration files.

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

### Test Deployment Framework

Tests shall be deployed using the framework provided in the following repository: https://github.com/whiteblock/gossip_deployer. This testing framework communicates with [`whiteblock/genesis`](https://github.com/whiteblock/genesis), a testing platform for blockchain-based distributed systems running on a cloud infrastructure, to deploy network nodes.

## Testing Metrics

In [[2]](#References), Leitao et. al present the following metrics to evaluate gossip protcols. The test metrics are collected and analyzed using the tools provided in `agencyenterprise/go-libp2p-pubsub-benchmark-tools`, and the description below is taken directly from the same repository.

The metrics computed are:
1. **TotalNanoTime** - the time (in nano seconds) for the message to propogate the network
2. **LastDeliveryHop** - the hop count of the last message that is delivered by a [pubsub] protocol or, in other words, is the maximum number of hops that a message must be forwarded in the overlay before it is delivered.
3. **RelativeMessageRedundancy (not yet implemented due to constraints of libp2p-gossipsub implementation)** RelativeMessageRedundancy (RMR) this metric measures the messages overhead in a [pubsub] protocol. It is defined as: (m / (n - 1)) - 1. where m is the total number of payload messages exchanged during the broadcast procedure and n is the total number of nodes that received that broadcast. This metric is only applicable when at least 2 nodes receive the message. A RMR value of zero means that there is exactly one payload message exchange for each node in the system, which is clearly the optimal value. By opposition, high values of RMR are indicative of a broadcast strategy that promotes a poor network usage. Note that it is possible to achieve a very low RMR by failing to be reliable. Thus the aim is to combine low RMR values with high reliability. Furthermore, RMR values are only comparable for protocols that exhibit similar reliability. Finally, note that in pure [pubsub] approaches, RMR is closely related with the protocol fanout, as it tends to fanout−1. 

### Additional Collected Metrics

Upon completing tests, we will open source the following array of metrics collected to the public. This will increase transparency and allow for further offline analysis of the collected data.

- Message type - topic of the message
- Message origin - sending address 
- Message destination - receiving address
- Last hop node - address of previous node that sent the message
<!-- - (TBD) Message nonce - chronology of the sent message -->
- Message size - size in bytes
- Message ID - unique string associated with that message
- Hop Count - number of hops in the longest path of a message (i.e., from the source to the last subscribed node that receives it)

## Network Topology
To evaluate the performance and reliability of the gossipsub protocol, we test the host-client implementation against two types of topologies: fully connected and random-connected. While these topologies may present an oversimplification, it is unclear what the resulting topologies of Eth2 due to large contingency on the final discovery service protocol deployed. Thus, this research effort will attempt to test gossipsub in a fully connected network as well as random topologies generated by known methods in order to evaluate gossipsub's performance.

<!-- For example, a (cluster specific) node within Cluster 1 may be peered with N number of nodes within its own cluster, however, based on proximity, certain nodes on the edge of this cluster may also be peered with nodes within Cluster 2 (inter cluster nodes). If Node X within Cluster 1 would like to transmit a message to Node Y within Cluster 4, these messages must propogate through each consecutive cluster in order to reach its destination.

 we can expect the results to be reflective of real-world performance. As we establish an appropriate dataset that is indicative of baseline performance, we can develop additional test series' and cases for future test phases.

Since peer discovery is outside the scope of work for this test phase, peering within the client implementation presented within this repository is handled statically. -->

### Peering
Peering will need to be done in a manner that is reproducible for the community and deterministic to ensure the validity of the results.

#### 1. Fully Connected Topology:
To provide a baseline test, we benchmark gossipsub on a fully connected network. 
 1. Bootstrap every node in the network
 2. Add all nodes' IPs into the peer list of every node

#### 2. Random Scale-Free Network Topology (Barabasi-Albert or B-A):

In 1999, Barabasi and Albert observed that the world wide web exhibited a scale-free nature and preferential attachment. Scale-free networks follow a power-law degree distribution, and preferential attachment describes the likelihood of a node connecting to nodes with high degrees. Inspired by this observation, the [Barabasi-Albert](https://en.wikipedia.org/wiki/Barab%C3%A1si%E2%80%93Albert_model) (B-A) model was created to generate random network topologies with both a power-law degree distribution and preferential attachment. As described by Albert-Barabasi in [[3]](#References) topology generation is "grown" starting with a small number $m_0$ of nodes. At each time step, a new node with *m &le; m<sub>0</sub>* edges that link the new node to $m$ different nodes currently present in the network. *m* is the *input degree parameter*. When choosing nodes, the probability *&Pi;* that a new node will connect to some node $i$ depends on the degree *k<sub>i</sub>* of node *i* such that:

<a align="center" href="https://www.codecogs.com/eqnedit.php?latex=\fn_jvn&space;\Pi(k_i)&space;=&space;\frac{k_{i}}{\sum_{j}&space;k_{j}}" target="_blank"><img src="https://latex.codecogs.com/png.latex?\fn_jvn&space;\Pi(k_i)&space;=&space;\frac{k_{i}}{\sum_{j}&space;k_{j}}" title="\Pi(k_i) = \frac{k_{i}}{\sum_{j} k_{j}}" /></a>

Network topologies are generated using the [NetworkX](https://networkx.github.io/) python library with a constant seed to make results reproducible. Within the test series, we will sweep the input degree parameter $m$ across a range around the default GossipSubD parameter (i.e., [2, 6, 12, 16] as indicated in breakdown section [Test Series](#Test-Series)).

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
