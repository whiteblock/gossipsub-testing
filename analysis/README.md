# Analyze Test Logs


### Quick Start

Create a virtualenv and `pip install -r requirements.txt`.

(assumes last node is the orchestra node)

Clone `go-libp2p-pubsub-benchmark-tools` repository in the same directory as
this repository. Run `go build` in the `go-libp2p-pubsub-benchmark-tools/cmd/analysis`
directory.

Place a folder of logs in the top level logs/ directory of this repo. Change
`LOG_PATH` in `run_analysis.sh` to the log directory of interest. Then, run
`bash run_analysis.sh` in this directory. Use the `Analysis.ipynb` to analyze
the resulting `analysis.json`.

### Batched Analysis Processing.

To analyze the logs in the logs/ directory, run `bash batched_run_analysis.sh` 
in this directory. The description of each subdirectory of logs/ can be found
in logs/README.md
