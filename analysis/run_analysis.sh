#!/bin/sh
curr_dir=`pwd`
log_dir="series_1a.2_2019-10-25T22:37:07"
log_path="../logs/$log_dir"

cd $log_path

#last node is node just running orchestra
orchestra_node=`ls node*[0-9]* -1v | tail -1`

echo $orchestra_node

mv $orchestra_node orchestra_node
cat node* > concat_nodes.txt
../../../go-libp2p-pubsub-benchmark-tools/cmd/analysis/analysis concat_nodes.txt -o analysis.json

mv orchestra_node $orchestra_node
rm concat_nodes.txt
mv analysis.json $curr_dir