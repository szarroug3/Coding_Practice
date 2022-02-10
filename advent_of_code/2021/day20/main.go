// https://adventofcode.com/2020/day/20

package main

import (
	"fmt"
	"os"
	"strconv"
	"utils/utils"
)

func Enhance(data []string, cipher string, offset int) []string {
	newData := make([]string, 0)
	for i := 0 - offset; i < len(data)+offset; i++ {
		line := ""
		for j := 0 - offset; j < len(data[0])+offset; j++ {
			curr := ""
			for k := i - 1; k < i+2; k++ {
				if k < 0 || k >= len(data) {
					curr += "000"
					continue
				}
				for l := j - 1; l < j+2; l++ {
					if l < 0 || l >= len(data[k]) {
						curr += "0"
					} else {
						if data[k][l] == '.' {
							curr += "0"
						} else {
							curr += "1"
						}
					}
				}
			}
			index, _ := strconv.ParseInt(curr, 2, 64)
			line += string(cipher[index])
		}
		newData = append(newData, line)
		line = ""
	}

	return newData
}

func EnhanceImage(data []string, cipher string, enhanceCount int, result chan interface{}) {
	offsets := make([]int, 0)
	if cipher[0] == '.' {
		offsets = append(offsets, 2)
		offsets = append(offsets, 2)
	} else {
		offsets = append(offsets, 3)
		offsets = append(offsets, -1)
	}

	for i := 0; i < enhanceCount; i++ {
		data = Enhance(data, cipher, offsets[i%2])
	}

	count := 0
	for _, line := range data {
		for _, value := range line {
			if value == '#' {
				count++
			}
		}
	}
	result <- count
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Input filename required.")
		return
	}

	data, err := utils.ReadFileAsSlices(os.Args[1], "\n")
	if err != nil {
		fmt.Println(err)
		return
	}

	cipher := data[0]
	data = data[2:]

	a := make(chan interface{})
	b := make(chan interface{})

	go EnhanceImage(data, cipher, 2, a)
	go EnhanceImage(data, cipher, 50, b)

	fmt.Println("Part A:", <-a)
	fmt.Println("Part B:", <-b)
}
