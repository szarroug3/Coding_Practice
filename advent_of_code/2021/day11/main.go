// https://adventofcode.com/2021/day/11

package main

import (
	"fmt"
	"os"
	"utils/utils"
)

func IncreaseAll(data [][]int) [][]int {
	for row, line := range data {
		for column, _ := range line {
			if data[row][column] == 10 {
				continue
			}
			data[row][column]++
		}
	}
	return data
}

func AlreadyFlashed(flashed map[int][]int, row int, column int) bool {
	columns, ok := flashed[row]
	if !ok {
		return false
	}

	for _, value := range columns {
		if column == value {
			return true
		}
	}

	return false
}

func MarkFlashed(flashed map[int][]int, row int, column int) map[int][]int {
	if _, ok := flashed[row]; !ok {
		flashed[row] = []int{column}
		return flashed
	}

	flashed[row] = append(flashed[row], column)
	return flashed
}

func Flash(data [][]int, flashed map[int][]int) ([][]int, map[int][]int, int) {
	count := 0
	decrease := make(map[int]map[int]int)

	for row, line := range data {
		for column, value := range line {
			if AlreadyFlashed(flashed, row, column) {
				continue
			}
			if value == 10 {
				count++
				if _, ok := decrease[row]; !ok {
					decrease[row] = make(map[int]int)
					decrease[row][column] = 0
				}
				decrease[row][column]++
				flashed = MarkFlashed(flashed, row, column)
			}
		}
	}

	for row, columns := range decrease {
		for column, count := range columns {
			data = IncreaseSurroundings(data, row, column, count)
		}
	}

	return data, flashed, count
}

func IncreaseSurroundings(data [][]int, row int, column int, count int) [][]int {
	currRow := row - 1
	if currRow < 0 {
		currRow = 0
	}
	for currRow < len(data) && currRow <= row+1 {
		currColumn := column - 1
		if currColumn < 0 {
			currColumn = 0
		}
		for currColumn < len(data[currRow]) && currColumn <= column+1 {
			if currColumn == column && currRow == row {
				currColumn++
				continue
			}

			data[currRow][currColumn] += count
			if data[currRow][currColumn] > 10 {
				data[currRow][currColumn] = 10
			}

			currColumn++
		}
		currRow++
	}

	return data
}

func Process(data [][]int) (int, int) {
	count := 0
	synchronized := -1
	for step := 1; step <= 100 || synchronized == -1; step++ {
		data = IncreaseAll(data)
		currCount := 1
		flashed := make(map[int][]int)
		for currCount > 0 {
			data, flashed, currCount = Flash(data, flashed)
			if step <= 100 {
				count += currCount
			}
		}
		for row, columns := range flashed {
			for _, column := range columns {
				data[row][column] = 0
			}

		}

		if synchronized == -1 && Synchronized(data) {
			synchronized = step
		}
	}
	return count, synchronized
}

func Synchronized(data [][]int) bool {
	for _, line := range data {
		for _, value := range line {
			if value != 0 {
				return false
			}
		}
	}
	return true
}

func PartB(result chan interface{}) {
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

	converted := utils.ConvertAllToInts(data)

	count, synchronized := Process(converted)

	fmt.Println("Part A:", count)
	fmt.Println("Part B:", synchronized)
}
