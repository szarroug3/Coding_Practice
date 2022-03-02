// https://adventofcode.com/2021/day/25

package main

import (
	"fmt"
	"os"
	"utils/utils"
)

func PartA(data [][]string, result chan interface{}) {
	fmt.Println("---")
	for _, line := range data {
		fmt.Println(line)
	}
	fmt.Println("---")
	steps := 0
	for moved := true; moved; steps++ {
		moved = false
		curr := data[:]
		for i := 0; i < len(data); i++ {
			for j := 0; j < len(data[i]); j++ {
				if data[i][j] != ">" {
					continue
				}

				east := (j + 1) % len(data[i])
				if data[i][east] == "." {
					fmt.Println("moving", i, j, "to", i, east)
					moved = true
					curr[i][j] = "."
					curr[i][east] = data[i][j]
				}
			}
		}

		fmt.Println("AFTER EAST:")
		for _, line := range curr {
			fmt.Println(line)
		}
		fmt.Println("---")
		for i := 0; i < len(data); i++ {
			south := (i + 1) % len(data)
			for j := 0; j < len(data[i]); j++ {
				if data[i][j] != "v" {
					continue
				}

				if data[south][j] == "." {
					fmt.Println("moving", i, j, "to", south, j)
					moved = true
					curr[i][j] = "."
					curr[south][j] = data[i][j]
				}
			}
		}

		fmt.Println("AFTER SOUTH:")
		for _, line := range curr {
			fmt.Println(line)
		}
		fmt.Println("---")
		data = curr
	}
	result <- steps
}

func PartB(data [][]string, result chan interface{}) {
	result <- "UPDATE THIS"
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Input filename required.")
		return
	}

	data, err := utils.ReadFileAsStringSlices(os.Args[1], "\n", "")
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
