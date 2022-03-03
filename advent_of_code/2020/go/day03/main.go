// https://adventofcode.com/2020/day/3

package main

import (
	"fmt"
	"os"
	"utils/utils"
)

type Instruction struct {
	right int
	down  int
}

func CountTrees(data [][]rune, instruction Instruction) int {
	x := 0
	y := 0
	count := 0

	for {
		x = (x + instruction.right) % len(data[y])
		y = y + instruction.down

		if y >= len(data) {
			break
		}

		if data[y][x] == '#' {
			count++
		}
	}

	return count
}

func PartA(data [][]rune, right int, down int, result chan interface{}) {
	result <- CountTrees(data, Instruction{right: 3, down: 1})
}

func PartB(data [][]rune, result chan interface{}) {
	product := 1
	instructions := []Instruction{
		Instruction{right: 1, down: 1},
		Instruction{right: 3, down: 1},
		Instruction{right: 5, down: 1},
		Instruction{right: 7, down: 1},
		Instruction{right: 1, down: 2},
	}
	for _, instruction := range instructions {
		product = product * CountTrees(data, instruction)
	}
	result <- product
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Input filename required.")
		return
	}

	data, err := utils.ReadFileAsRuneSlices(os.Args[1], "\n")
	if err != nil {
		fmt.Println(err)
		return
	}

	a := make(chan interface{})
	b := make(chan interface{})

	go PartA(data, 3, 1, a)
	go PartB(data, b)

	fmt.Println("Part A:", <-a)
	fmt.Println("Part B:", <-b)
}
