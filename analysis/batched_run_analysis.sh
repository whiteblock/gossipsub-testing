#!/bin/sh
cur_dir=`pwd`
log_path="../logs/"

cd $log_path

for dir in */ ; do
    cd $dir
    echo "analyzing directory" `pwd`
    #last node is node just running orchestra
    orchestra_node=`ls node*[0-9]* -1v | tail -1`
    mv $orchestra_node orchestra_node
    cat node* > concat_nodes.txt
    ../../../go-libp2p-pubsub-benchmark-tools/cmd/analysis/analysis concat_nodes.txt -o analysis.json
    mv orchestra_node $orchestra_node
    rm concat_nodes.txt
    test_series=`echo ${PWD##*/} | cut -d'_' -f 2`
    mv analysis.json $cur_dir/analysis_$test_series.json
    cd ..
done
