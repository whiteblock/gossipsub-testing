#!/bin/sh
CWD=`pwd`
LOG_PATH="../logs/series__2019-10-24T18:26:27/"
ANALYSIS_BIN='../../../go-libp2p-pubsub-benchmark-tools/cmd/analysis/analysis concat_nodes.txt'

cd $LOG_PATH

#last node is node just running orchestra
ORCHESTRA_NODE=`ls nodes[0-9]* -1v | tail -1`

mv $ORCHESTRA_NODE orchestra_node
cat node* > concat_nodes.txt
$ANALYSIS_BIN -o analysis.json
mv orchestra_node $ORCHESTRA_NODE
rm concat_nodes.txt
mv analysis.json $CWD