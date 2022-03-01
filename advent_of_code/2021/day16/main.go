// https://adventofcode.com/2021/day/16

package main

import (
	"fmt"
	"os"
	"utils/utils"
)

func PartA(data string, result chan interface{}) {
	result <- "UPDATE THIS"
}

func PartB(data string, result chan interface{}) {
	result <- "UPDATE THIS"
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Input filename required.")
		return
	}

	data, err := utils.ReadFileAsString(os.Args[1])
	if err != nil {
		fmt.Println(err)
		return
	}

	// TODO: REMOVE THIS
	fmt.Println(data)

	a := make(chan interface{})
	b := make(chan interface{})

	go PartA(data, a)
	go PartB(data, b)

	fmt.Println("Part A:", <-a)
	fmt.Println("Part B:", <-b)
}
