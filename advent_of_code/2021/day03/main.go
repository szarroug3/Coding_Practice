// https://adventofcode.com/2020/day/3

package main

import (
	"fmt"
	"os"
	"sort"
	"strconv"
	"utils/utils"
)

func GetBitCount(data []string, index int) (int, int) {
	zero := 0
	one := 0

	for _, value := range data {
		if value[index] == '0' {
			zero++
		} else {
			one++
		}
	}

	return zero, one
}

func PartA(data []string, result chan interface{}) {
	gamma := ""
	epsilon := ""

	for index := 0; index < len(data[0]); index++ {
		zero, one := GetBitCount(data, index)
		if zero > one {
			gamma += "0"
			epsilon += "1"
		} else {
			gamma += "1"
			epsilon += "0"
		}
	}

	gammaDecimal, err := strconv.ParseInt(gamma, 2, 64)
	if err != nil {
		result <- err
		return
	}

	epsilonDecimal, err := strconv.ParseInt(epsilon, 2, 64)
	if err != nil {
		result <- err
		return
	}

	result <- gammaDecimal * epsilonDecimal
}

func GetValuesWithBitAtIndex(data []string, index int, value byte) []string {
	var results []string
	for _, line := range data {
		if line[index] == value {
			results = append(results, line)
		}
	}

	return results
}

func EvaluateBitCriteria(data []string, tieBreaker byte, sortedPosition int, result chan int64) {
	for index := 0; index < len(data[0]); index++ {
		zero, one := GetBitCount(data, index)
		counts := []int{zero, one}
		sort.Ints(counts)

		if zero == one {
			data = GetValuesWithBitAtIndex(data, index, tieBreaker)
		} else if counts[sortedPosition] == zero {
			data = GetValuesWithBitAtIndex(data, index, '0')
		} else {
			data = GetValuesWithBitAtIndex(data, index, '1')
		}

		if len(data) == 1 {
			break
		}
	}

	decimal, _ := strconv.ParseInt(data[0], 2, 64)
	result <- decimal
}

func PartB(data []string, result chan interface{}) {
	oxygenValue := make(chan int64)
	co2Value := make(chan int64)

	go EvaluateBitCriteria(data, '1', 1, oxygenValue)
	go EvaluateBitCriteria(data, '0', 0, co2Value)

	result <- <-oxygenValue * <-co2Value
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

	a := make(chan interface{})
	b := make(chan interface{})

	go PartA(data, a)
	go PartB(data, b)

	fmt.Println("Part A:", <-a)
	fmt.Println("Part B:", <-b)
}
