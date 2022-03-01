// https://adventofcode.com/2021/day/7

package main

import (
	"fmt"
	"os"
	"utils/utils"
)

func PartA(data []int, result chan interface{}) {
	min := data[0]
	max := data[0]

	for _, position := range data[1:] {
		if position > max {
			max = position
		}
		if position < min {
			min = position
		}
	}

	fuel := -1
	for i := min; i <= max; i++ {
		curr := 0
		for _, position := range data {
			if position < i {
				curr += i - position
			} else {
				curr += position - i
			}
		}
		if fuel == -1 || curr < fuel {
			fuel = curr
		}
	}

	result <- fuel
}

func GetCrabMovementFuel(position int, destination int) int {
	if position == destination {
		return 0
	} else if position < destination {
		return ((destination - position + 1) * (destination - position)) / 2
	} else {
		return ((1 + position - destination) * (position - destination)) / 2
	}
}

func PartB(data []int, result chan interface{}) {
	min := data[0]
	max := data[0]

	for _, position := range data[1:] {
		if position > max {
			max = position
		}
		if position < min {
			min = position
		}
	}

	fuel := -1
	for i := min; i <= max; i++ {
		curr := 0
		for _, position := range data {
			curr += GetCrabMovementFuel(position, i)
		}
		if fuel == -1 || curr < fuel {
			fuel = curr
		}
	}

	result <- fuel
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Input filename required.")
		return
	}

	data, err := utils.ReadFileAsSlices(os.Args[1], ",")
	if err != nil {
		fmt.Println(err)
		return
	}

	converted := utils.ConvertToInts(data)

	a := make(chan interface{})
	b := make(chan interface{})

	go PartA(converted, a)
	go PartB(converted, b)

	fmt.Println("Part A:", <-a)
	fmt.Println("Part B:", <-b)
}
