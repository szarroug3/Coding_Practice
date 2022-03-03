// https://adventofcode.com/2020/day/1

package main

import (
	"errors"
	"fmt"
	"os"
	"utils/utils"
)

func GetCombinations(data []int, combinations [][]int, combination []int, index int, combination_len int) [][]int {
	for i := index; i < len(data); i++ {
		curr := combination
		curr = append(curr, data[i])

		if len(curr) == combination_len {
			combinations = append(combinations, curr)
		} else {
			combinations = GetCombinations(data, combinations, curr, i+1, combination_len)
		}
	}

	return combinations
}

func GetSumEqualTo(data [][]int, sum int) ([]int, error) {
	for _, values := range data {
		if utils.Sum(values) == sum {
			return values, nil
		}
	}

	return nil, errors.New(fmt.Sprintf("Could not find values that sum to %d.", sum))
}

func GetAnswer(data []int, combination_len int, sum int, result chan interface{}) {
	combinations := GetCombinations(data, make([][]int, 0), make([]int, 0), 0, combination_len)
	values, err := GetSumEqualTo(combinations, sum)

	if err != nil {
		result <- err
	} else {
		result <- utils.Product(values)
	}
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

	converted := utils.ConvertToInts(data)

	a := make(chan interface{})
	b := make(chan interface{})

	go GetAnswer(converted, 2, 2020, a)
	go GetAnswer(converted, 3, 2020, b)

	fmt.Println("Part A:", <-a)
	fmt.Println("Part B:", <-b)
}
