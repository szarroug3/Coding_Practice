// https://adventofcode.com/2020/day/#

package main

import (
	"fmt"
	"os"
	"utils/utils"
)

func PartA(result chan interface{}) {
	result <- "UPDATE THIS"
}

func PartB(result chan interface{}) {
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

	go PartA(a)
	go PartB(b)

	fmt.Println("Part A:", <-a)
	fmt.Println("Part B:", <-b)
}
