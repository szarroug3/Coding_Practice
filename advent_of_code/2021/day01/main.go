// https://adventofcode.com/2021/day/1

package main

import (
	"fmt"
	"os"
	"utils/utils"
)

func PartA(measurements []int, result chan interface{}) {
	count := 0
	curr := measurements[0]

	for _, measurement := range measurements[1:] {
		if measurement > curr {
			count += 1
		}
		curr = measurement
	}

	result <- count
}

func PartB(measurements []int, result chan interface{}) {
	count := 0
	curr := utils.Sum(measurements[:3])

	for index, measurement := range measurements[3:] {
		// index here is already offset by 3 because we start
		// at 0 instead of 3 so we don't need to subtract 3
		new := curr - measurements[index] + measurement
		if new > curr {
			count += 1
		}
		curr = new
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

	measurements := utils.ConvertToInts(data)

	a := make(chan interface{})
	b := make(chan interface{})

	go PartA(measurements, a)
	go PartB(measurements, b)

	fmt.Println("Part A:", <-a)
	fmt.Println("Part B:", <-b)
}
