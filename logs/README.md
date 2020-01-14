# Logs Directory

The subdirectory naming structure for logs follows the following format

    seriesXXY.Z

where XX indicates the series number, Y indicates the degree parameter input, 
and Z incidates the number of a repeated test run. 

- series_01: nodes = 95, fully connected network, 20 msgs/sec 
- series_11: nodes = 95, seed = 42, Barabasi-Albert degree parameter = 2, 20 msgs/sec
    - 11a: repeat
    - 11b: repeat
    - 11c: repeat
- series_21: nodes = 95, seed = 42, 20 msgs/sec
    - 21a: Barabasi-Albert degree parameter = 2
    - 21b: Barabasi-Albert degree parameter = 6
    - 21c: Barabasi-Albert degree parameter = 12
    - 21d: Barabasi-Albert degree parameter = 16
- series_31: nodes = 95, seed = 42, 200 msgs/sec
    - 31a: Barabasi-Albert degree parameter = 2
    - 31b: Barabasi-Albert degree parameter = 6
    - 31c: Barabasi-Albert degree parameter = 12
    - 31d: Barabasi-Albert degree parameter = 16