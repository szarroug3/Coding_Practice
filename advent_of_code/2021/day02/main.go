// https://adventofcode.com/2020/day/2

package main

import (
	"fmt"
	"os"
	"strconv"
	"utils/utils"
)

func PartA(directions [][]string, result chan interface{}) {
	depth := 0
	horizontal := 0

	for _, line := range directions {
		direction := line[0]

		unit, err := strconv.Atoi(line[1])
		if err != nil {
			result <- err
			return
		}

		switch direction {
		case "forward":
			horizontal += unit
		case "down":
			depth += unit
		case "up":
			depth -= unit
		}
	}

	result <- horizontal * depth
}

func PartB(directions [][]string, result chan interface{}) {
	depth := 0
	horizontal := 0
	aim := 0

	for _, line := range directions {
		direction := line[0]

		unit, err := strconv.Atoi(line[1])
		if err != nil {
			result <- err
			return
		}

		switch direction {
		case "forward":
			horizontal += unit
			depth += aim * unit
		case "down":
			aim += unit
		case "up":
			aim -= unit
		}
	}

	result <- horizontal * depth
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Input filename required.")
		return
	}

	data, err := utils.ReadFileAsStringSlices(os.Args[1], "\n", " ")
	if err != nil {
		fmt.Println(err)
		return
	}

	a := make(chan interface{})
	b := make(chan interface{})

	go PartA(data, a)
	go PartB(data, b)

	fmt.Println("Part A:", <-a)
	fmt.Println("Part B:", <-b)
}
