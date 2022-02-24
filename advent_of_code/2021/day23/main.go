// https://adventofcode.com/2020/day/23

package main

import (
	"fmt"
	"math"
	"os"
	"utils/utils"
)

func Parse(data []string) [][]uint8 {
	buckets := make([][]uint8, 0)
	for i := 3; i <= 9; i += 2 {
		buckets = append(buckets, []uint8{data[2][i], data[3][i]})
	}
	return buckets
}

func PartA(buckets [][]uint8, result chan interface{}) {
	costs := map[int]int{65: 1, 66: 10, 67: 100, 68: 1000}
	final := map[int]int{0: 0, 1: 0, 2: 0, 3: 0}

	for i, bucket := range buckets {
		for j := len(bucket) - 1; j >= 0; j-- {
			value := int(bucket[j])
			destination := value - 65
			if i != destination {
				break
			}
			final[destination]++
		}
	}

	fmt.Println(final)
	energy := 0
	for i, bucket := range buckets {
		move := false
		for j := len(bucket) - 1; j >= 0; j-- {
			value := int(bucket[j])
			destination := value - 65
			depth := 2 - final[destination]
			if int(value)-65-i != 0 {
				move = true
				steps := 0
				// move out of current room
				steps += j + 1
				// move across hallway
				steps += 2 * int(math.Abs(float64(destination-i)))
				// move into destination
				steps += depth

				energy += steps * costs[value]
				final[destination]++
				fmt.Println("Moving", value, i, j, steps*costs[value], energy)
			} else if move {
				steps := (2 * (j + 1)) + 2
				energy += steps * costs[value]
				fmt.Println("Moving", value, i, j, steps*costs[value], energy)
				final[destination]++
			}
		}
	}
	result <- energy
}

func PartB(buckets [][]uint8, result chan interface{}) {
	result <- "UPDATE THIS"
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

	buckets := Parse(data)
	fmt.Println(buckets)

	a := make(chan interface{})
	b := make(chan interface{})

	go PartA(buckets, a)
	go PartB(buckets, b)

	fmt.Println("Part A:", <-a)
	fmt.Println("Part B:", <-b)
}
