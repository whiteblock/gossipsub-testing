# Eth2 - LibP2P Gossipsub Benchmarking

### Overview
The purpose of this testing initiative is to benchmark the performance of the libp2p gossipsub implementation. With time constraints present in Eth2, it is important to verify that messages will be able to be disseminated throughout the network in a timely manner. 

The libp2p gossipsub protocol falls under a broader class of information dissemination techniques known as epidemic protocols. This research effort intends to evaluate the performance of the gossipsub protocol to verify that it will support the specifications of Ethereum 2.0. One method to analyze the performance of epidemic protocols is to create a mathematical model. A model can provide insight into the correctness of the protocol and provide an abstract view of the protocol in action. The authors of [^bakshi2007] provide an overview of the various types of formal analysis techniques for epidemic protocols. However, capturing all the dynamics of a distributed protocol intended to be deployed on a very large network into a model requires a lot of effort and is extremely difficult. Often, assumptions are made to simplify analysis which inevitably affects the accuracy and meaningfulness of the results [^bakshi2007]. Mathematical analysis can be paired with simulations to validate and understand the system behavior of a protocol. However, mathematical modeling and simulations are inherently abstract which causes any results to not directly reflect real-world performance. The best option for testing a distributed protocol before the launch of an actual testnet would be to test a network of nodes in a cloud infrastructure. This collaborative research project will investigate meaningful methodologies of testing the libp2p protocol in an peer to peer network of real nodes. This includes determining useful metrics, topologies, network impairments, and gossipsub parameters.

## Technical Implementation
- use whiteblock genesis platform
- utilize the libp2p gossipsub host implementation
    - https://github.com/libp2p/go-libp2p-pubsub
- incorporate profiling tools
    - pprof
    - callgrind

### Resourcing 
| Resource Allocation  |  |
| --------  | --------  |
| CPU Resources Per Node: __number_of_cpu__ |  |
| Memory Resources Per Node: __number_of_ram__ |  |
| Total CPU: __total_cpus__ |  |
| Total Memory: __total_memory__ |  |

In the [prior study](https://github.com/whiteblock/p2p-tests), results showed high CPU utilization when running the `go-libp2p-daemon` in a Docker containers with one CPU allocated per node. To alleviate this issue, we intend allocate two CPUs per node and use a direct libp2p host implementation for all tests to reduce any bottlenecks.


### Configuration
- The LibP2P host configuration will be as follows to ensure that the client will be set up according to the correct specifications.
```
<!-- Add the configuration file (or parameters) here -->

```

### Host and Client Implementation

For all tests, each node will use a fork of the following host and client implementation will be used: https://github.com/agencyenterprise/go-libp2p-pubsub-benchmark-tools. This implementation includes tools for generating messages at each node and analysis tools for parsing and plotting metrics described in the next section. The fork consists only of modified configuration files.

### Test Deployment Framework

Tests shall be deployed using the framework provided in the following repository: https://github.com/whiteblock/gossip_deployer.

## Testing Metrics

The authors of [^leitao2007epidemic] present the following metrics to evaluate gossip protcols. The test metrics are collected and analyzed using the tools provided in `agencyenterprise/go-libp2p-pubsub-benchmark-tools`, and the description below is taken directly from the same repository.

The metrics computed are:
1. **TotalNanoTime** - the time (in nano seconds) for the message to propogate the network
2. **LastDeliveryHop** - the hop count of the last message that is delivered by a [pubsub] protocol or, in other words, is the maximum number of hops that a message must be forwarded in the overlay before it is delivered.
3. **RelativeMessageRedundancy** - RelativeMessageRedundancy (RMR) this metric measures the messages overhead in a [pubsub] protocol. It is defined as: (m / (n - 1)) - 1. where m is the total number of payload messages exchanged during the broadcast procedure and n is the total number of nodes that received that broadcast. This metric is only applicable when at least 2 nodes receive the message. A RMR value of zero means that there is exactly one payload message exchange for each node in the system, which is clearly the optimal value. By opposition, high values of RMR are indicative of a broadcast strategy that promotes a poor network usage. Note that it is possible to achieve a very low RMR by failing to be reliable. Thus the aim is to combine low RMR values with high reliability. Furthermore, RMR values are only comparable for protocols that exhibit similar reliability. Finally, note that in pure [pubsub] approaches, RMR is closely related with the protocol fanout, as it tends to fanout−1.

### Additional Collected Metrics

Upon completing tests, we will open source the following array of metrics collected to the public. This will increase transparency and allow for further offline analysis of the collected data.

- Message type - topic of the message
- Message origin - sending address 
- Message destination - receiving address
- Last relaying node - the previous node that sent the message
- Message nonce - chronology of the sent message
- Message size - the message size will be in bytes
- MessageID - unique string associated with that message
- HopCount - number of hops the message had to make in order to reach its destination

## Network Topology
To evaluate the performance and reliability of the gossipsub protocol, we test the host-client implementation against three different network topologies: linear, tree, and fully connected. While these topologies may present an oversimplification, it is unclear what the resulting topologies of Eth2 due to large contingency on the final discovery service protocol deployed. Peer discovery is outside of the scope of work. Nonetheless, these simplified topologies will allow the stress testing of gossipsub.

<!-- For example, a (cluster specific) node within Cluster 1 may be peered with N number of nodes within its own cluster, however, based on proximity, certain nodes on the edge of this cluster may also be peered with nodes within Cluster 2 (inter cluster nodes). If Node X within Cluster 1 would like to transmit a message to Node Y within Cluster 4, these messages must propogate through each consecutive cluster in order to reach its destination.

 we can expect the results to be reflective of real-world performance. As we establish an appropriate dataset that is indicative of baseline performance, we can develop additional test series' and cases for future test phases.

Since peer discovery is outside the scope of work for this test phase, peering within the client implementation presented within this repository is handled statically. -->

### Peering
Peering will need to be done in a manner that is reproducible for the community and deterministic to ensure the validity of the results.

#### 1. Linear Topology:
Our test framework takes as an input a number of nodes and launches a linear network topology that forms a chain similarly to the one depicted below. The purpose of this topology is to test the end-to-end delay in a network which requires a high number of hops. 

```
nodes ->  ㅁ  -  ㅁ  -  ㅁ  -  ㅁ  -  ㅁ  -  ㅁ  -  ㅁ  -  ㅁ  -  ㅁ ...
```
- [x] implementation complete
- [ ] analysis complete

> The number of hops a message can have between two nodes in the network:
 Maximum:  `n-1`
 Minimum:  `1`
 where n=number of nodes
 
#### 2. Tree Topology:
The purpose of creating a tree topology is to test gossipsub against a sparse connected network. The peering algorithm will be done in the following method:
 1. Create a node
 2. Have a node peer with a previously created node
 3. Each peer will have a maximum peer list of 4

```  
                     ... ... ... ... ... ... ...
                       . . . . . . . . . . . .
                           
                          ㅁ  ㅁ  ㅁ  ㅁ ㅁ ㅁ
                            \ | /    \ | /
                         ㅁ - ㅁ        ㅁ - ㅁ
                                \   / 
                                  ㅁ 
                                /   \  
                         ㅁ - ㅁ        ㅁ - ㅁ
                            / | \    / | \    
                          ㅁ  ㅁ  ㅁ  ㅁ ㅁ ㅁ
                          
                         . . . . . . . . . . . . 
                       ... ... ... ... ... ... ...
```
 > The number of hops a message can have from the furthest cluster to the other furthest cluster will be:
 Maximum:  `n`
 Minimum:  `2n`
 where n=number of hop nodes
 
- [ ] implementation complete
- [ ] analysis complete

#### 3. Fully Connected Topology:
For the fully connected network topology, every node in the network will be peered with every other node in the network
 1. Create every node in the network
 2. Add all nodes' IPs into the peer list of every node

 > The number of hops a message can have from the furthest node to the other furthest node will be:
 Maximum:  `1`*
 Minimum:  `1`

- [ ] implementation complete
- [ ] analysis complete

\* dependant on the degree parameter, `GossipSubD`, that is set in the gossipsub host implementation.
 
## Testing Procedure
 1.   Provision nodes
 2.   Statically peer each node according to specified topology
 3.   Configure actions and behavior between nodes according to specified test case
 4.   Apply network conditions (if applicable)
 5.   Send messages from specified number of nodes
 6.   Log message data from each node
 7.   Timeout 10 seconds -- we have to make sure we do this
 8.   Make sure all data is saved in proper format
 9.  Backup data locally
 10.  Tear down network
 11.  Parse and aggregate data after each test
 

## Test Series

For all tests, two CPUs* shall be allocated for every node.

### Series 1: Control
| Vars | Topology | Case A | Case B | Case C |
| ---- | -------- | ------ | ------ | ------ |
|  | Network Latency (ms) | 0 | 0 | 0 |
|  | Packet Loss (%) | 0 | 0 | 0 |
|  | Bandwidth (MB) | 1000 | 1000 | 1000 |
|  | Total Clients | ? | ? | ? |
|  | Message Size (B) | 500 | 500 | 500 |
|  | Messages sent per Sending Client (msg/s) | ? | ? | ? |
|  | Peering | Linear | Linear | Linear |

### Series 2: Network Latency
| Vars | Topology | Case A | Case B | Case C |
| ---- | -------- | ------ | ------ | ------ |
| X | Network Latency (ms) | 50 | 100 | 150 |
|  | Packet Loss (%) | 0 | 0 | 0 |
|  | Bandwidth (MB) | 1000 | 1000 | 1000 |
|  | Total Clients | ? | ? | ? |
|  | Message Size (B) | 500 | 500 | 500 |
|  | Messages sent per Sending Client (msg/s) | ? | ? | ? |
|  | Peering | Linear | Linear | Linear |

### Series 3: Increased Network Latency
| Vars | Topology | Case A | Case B | Case C |
| ---- | -------- | ------ | ------ | ------ |
| X | Network Latency (ms) | 300 | 500 | 1000 |
|  | Packet Loss (%) | 0 | 0 | 0 |
|  | Bandwidth (MB) | 1000 | 1000 | 1000 |
|  | Total Clients | ? | ? | ? |
|  | Message Size (B) | 500 | 500 | 500 |
|  | Messages sent per Sending Client (msg/s) | ? | ? | ? |
|  | Peering | Linear | Linear | Linear |

### Series 4: Packet Loss
| Vars | Topology | Case A | Case B | Case C |
| ---- | -------- | ------ | ------ | ------ |
|  | Network Latency (ms) | 0 | 0 | 0 |
| X | Packet Loss (%) | 0.01 | 0.1 | 1 |
|  | Bandwidth (MB) | 1000 | 1000 | 1000 |
|  | Total Clients | ? | ? | ? |
|  | Message Size (B) | 500 | 500 | 500 |
|  | Messages sent per Sending Client (msg/s) | ? | ? | ? |
|  | Peering | Linear | Linear | Linear |

### Series 5: Bandwidth
| Vars | Topology | Case A | Case B | Case C |
| ---- | -------- | ------ | ------ | ------ |
|  | Network Latency (ms) | 0 | 0 | 0 |
|  | Packet Loss (%) | 0 | 0 | 0 |
| X | Bandwidth (MB) | 10 | 50 | 100 |
|  | Total Clients | ? | ? | ? |
|  | Message Size (B) | 500 | 500 | 500 |
|  | Messages sent per Sending Client (msg/s) | ? | ? | ? |
|  | Peering | Linear | Linear | Linear |

#### Series 6: Stress Test
| Vars | Topology | Case A | Case B | Case C |
| ---- | -------- | ------ | ------ | ------ |
| X | Network Latency (ms) | 150 | 150 | 150 |
| X | Packet Loss (%) | 0.01 | 0.01 | 0.01 |
| X | Bandwidth (MB) | 10 | 10 | 10 |
|  | Total Clients | ? | ? | ? |
|  | Message Size (B) | 500 | 500 | 500 |
|  | Messages sent per Sending Client (msg/s) | ? | ? | ? |
|  | Peering | Linear | Linear | Linear |

### Series 7: Total Clients
| Vars | Topology | Case A | Case B | Case C |
| ---- | -------- | ------ | ------ | ------ |
|  | Network Latency (ms) | 0 | 0 | 0 |
|  | Packet Loss (%) | 0 | 0 | 0 |
|  | Bandwidth (MB) | 1000 | 1000 | 1000 |
| X | Total Clients | ? | ? | ? |
|  | Message Size (B) | 500 | 500 | 500 |
|  | Messages sent per Sending Client (msg/s) | ? | ? | ? |
|  | Peering | Linear | Linear | Linear |

### Series 8: Message Size [^ethmessage]
| Vars | Topology | Case A | Case B | Case C |
| ---- | -------- | ------ | ------ | ------ |
|  | Network Latency (ms) | 0 | 0 | 0 |
|  | Packet Loss (%) | 0 | 0 | 0 |
|  | Bandwidth (MB) | 1000 | 1000 | 1000 |
|  | Total Clients | ? | ? | ? |
| X | Message Size (B) | 50000 | 100000 | 1000000 |
|  | Messages sent per Sending Client (msg/s) | ? | ? | ? |
|  | Peering | Linear | Linear | Linear |

### Series 9: Messages Sent
| Vars | Topology | Case A | Case B | Case C |
| ---- | -------- | ------ | ------ | ------ |
|  | Network Latency (ms) | 0 | 0 | 0 |
|  | Packet Loss (%) | 0 | 0 | 0 |
|  | Bandwidth (MB) | 1000 | 1000 | 1000 |
|  | Total Clients | ? | ? | ? |
|  | Message Size (B) | 500 | 500 | 500 |
| X | Messages sent per Sending Client (msg/s) | ? | ? | ? |
|  | Peering | Linear | Linear | Linear |

### Series 10: Peering Topology
| Vars | Topology | Case A | Case B | Case C |
| ---- | -------- | ------ | ------ | ------ |
|  | Network Latency (ms) | 0 | 0 | 0 |
|  | Packet Loss (%) | 0 | 0 | 0 |
|  | Bandwidth (MB) | 1000 | 1000 | 1000 |
|  | Total Clients | ? | ? | ? |
|  | Message Size (B) | 500 | 500 | 500 | 
|  | Messages sent per Sending Client (msg/s) | ? | ? | ? |
| X | Peering | Linear | Tree | Full Mesh|

### Series 11: Transport Security
| Vars | Topology | Case A | Case B |
| ---- | -------- | ------ | ------ |
|  | Network Latency (ms) | 0 | 0 |
|  | Packet Loss (%) | 0 | 0 |
|  | Bandwidth (MB) | 1000 | 1000 |
|  | Total Clients | ? | ? |
|  | Message Size (B) | 500 | 500 |
|  | Messages sent per Sending Client (msg/s) | ? | ? |
|  | Peering | Linear | Linear | 
| X | Transport Security | NONE | SECIO | 

\* need to discuss the CPU resourcing for each node

## Appendix

[^montresor2017]: A. Montresor, “Gossip and epidemic protocol,” Wiley Encyclopedia of Electrical and Electronics Engineering, vol. 1, 2017.

[^bakshi2007]: R. Bakhshi, F. Bonnet, W. Fokkink, and B. Haverkort, “Formal analysis techniques for gossiping protocols,”SIGOPS Oper. Syst.Rev., vol. 41, no. 5, pp. 28–36, Oct. 2007.

[^leitao2007epidemic]: J. Leitão, J. Pereira, and L. Rodrigues, “Epidemic broadcast trees,” Proc. IEEE Symp. Reliab. Distrib. Syst., pp. 301–310, 2007.

[^ethmessage]: eth2 phase 0 networking requirements, "https://notes.ethereum.org/zgzMxFNiSF-iW5wA5uKH0Q?view."
