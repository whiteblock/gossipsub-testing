package main

import (
	"os"
	"fmt"
	"log"
	"sort"
	"bufio"
	"regexp"
	"strings"
	"strconv"
	"io/ioutil"
	"encoding/json"
)

/*
LINE OF resource.log
[CONTAINER ID, NAME, CPU %, MEM USAGE / LIMIT, MEM %, NET I/O, BLOCK I/O, PIDS]

0: 1be4c7aab2a1		[CONTAINER ID]
1: whiteblock-node39-1	[NAME]
2: 0.00%		[CPU%]
3: 1.613MiB		[MEM USAGE]
4: /			[MEM USAGE]
5: 354.3GiB		[MEM USAGE]
6: 0.00%		[MEM %]
7: 2.46kB		[NET I/O]
8: /			[NET I/O]
9: 0B			[NET I/O]
10: 0B			[BLOCK I/O]
11: /			[BLOCK I/O]
12: 0B			[BLOCK I/O]
13: 1			[PIDS]
*/

type message struct {
	node           string    `json:"node"`
	cpuPercentage  []string  `json:"cpuPercentage"`
	memUsageLimit  []string  `json:"memUsageLimit"`
        memPercentage  []string  `json:"memPercentage"`
	netIO          []string  `json:"netIO"`
	blockIO        []string  `json:"blockIO"`
}

		
func writeFile(resourceName string, node string, data interface{}) error {
	f, err := json.Marshal(data)
	if err != nil {
		return err
	}
	if _, err := os.Stat(fmt.Sprintf("resource/%s", resourceName)); os.IsNotExist(err) {
              err := os.MkdirAll(fmt.Sprintf("resource/%s", resourceName), 0755)
              if err != nil {
                      return err
              }
	}
	err = ioutil.WriteFile(fmt.Sprintf("./resource/%s/%s", resourceName, node), f, 0644)
	if err != nil {
		return err
	}
	return nil
}

func calcMedian(l []float64) float64 {
	sort.Float64s(l)
	midNum := len(l)/2
	//check if the length is even or not
	if (len(l)%2 != 0) {
		return l[midNum]
	} else {
		return (l[midNum-1] + l[midNum] / 2)
	}
}

func parse(filePath string) error {
	file, err := os.Open(fmt.Sprintf("%s/resource.log",filePath))
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)

	re := regexp.MustCompile(`\s+`)
	
    	cpuPercentage := make(map[string][]string)
	memoryRatio := make(map[string][]string)
	memoryPercentage := make(map[string][]string)
	netIO := make(map[string][]string)
	blockIO := make(map[string][]string)

	for scanner.Scan() {
		s := re.ReplaceAllString(scanner.Text(), " ")
		spl := strings.Split(s, " ")
		if (string(spl[1]) == "ID") {
			continue
		} else {
			cpuPercentage[string(spl[1])] = append(cpuPercentage[string(spl[1])], fmt.Sprintf("%s", spl[2]))
			memoryRatio[string(spl[1])] = append(memoryRatio[string(spl[1])], fmt.Sprintf("%s/%s", spl[3], spl[5]))
			memoryPercentage[string(spl[1])] = append(memoryPercentage[string(spl[1])], fmt.Sprintf("%s", spl[6]))
			netIO[string(spl[1])] = append(netIO[string(spl[1])], fmt.Sprintf("%s/%s", spl[7], spl[9]))
			blockIO[string(spl[1])] = append(blockIO[string(spl[1])], fmt.Sprintf("%s/%s", spl[10], spl[12]))
		}
  	}
	
	for key, _ := range cpuPercentage {
		writeFile("cpuPercentage", key, cpuPercentage[key])
		writeFile("memoryRatio", key, memoryRatio[key])
		writeFile("memoryPercentage", key, memoryPercentage[key])
		writeFile("netIO", key, netIO[key])
		writeFile("blockIO", key, blockIO[key])
		
		sumCPU := float64(0)
		aggrCPU := make(map[string]map[string]float64)
		tmparrCPU := []float64{}

		sumRAM := float64(0)
		aggrRAM := make(map[string]map[string]float64)
		tmparrRAM := []float64{}

		for i := 0; i < len(cpuPercentage) ; i++ {
                	cpuPercentage[key][i] = strings.ReplaceAll(cpuPercentage[key][i],"%","")
			valCPU, err := strconv.ParseFloat(cpuPercentage[key][i], 64)
			if err != nil {
				log.Fatal(err)
			}
			tmparrCPU = append(tmparrCPU, valCPU)
			sumCPU += valCPU

			memoryPercentage[key][i] = strings.ReplaceAll(memoryPercentage[key][i],"%","")
                        valRAM, err := strconv.ParseFloat(memoryPercentage[key][i], 64)
                        if err != nil {
                                log.Fatal(err)
                        }
                        tmparrRAM = append(tmparrRAM, valRAM)
                        sumRAM += valRAM

			
        	}
		aggrCPU[key] = make(map[string]float64)
		aggrCPU[key]["average"] = sumCPU/float64(len(tmparrCPU))
		aggrCPU[key]["median"] = calcMedian(tmparrCPU)
		writeFile("cpuPercentageAggr", key, aggrCPU)

		aggrRAM[key] = make(map[string]float64)
                aggrRAM[key]["average"] = sumCPU/float64(len(tmparrRAM))
                aggrRAM[key]["median"] = calcMedian(tmparrRAM)
                writeFile("memoryPercentageAggr", key, aggrRAM)
	}

    	if err := scanner.Err(); err != nil {
        	log.Fatal(err)
    	}

	return nil
}
