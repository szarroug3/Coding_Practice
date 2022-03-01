// https://adventofcode.com/2021/day/9

package main

import (
	"fmt"
	"os"
	"sort"
	"utils/utils"
)

func FindLowPoints(data [][]int) [][]int {
	lowPoints := make([][]int, 0)

	for row, line := range data {
		for column, value := range line {
			if row > 0 && data[row-1][column] <= value {
				continue
			} else if row < len(data)-1 && data[row+1][column] <= value {
				continue
			} else if column > 0 && data[row][column-1] <= value {
				continue
			} else if column < len(data[row])-1 && data[row][column+1] <= value {
				continue
			}
			lowPoints = append(lowPoints, []int{row, column})
		}
	}

	return lowPoints
}

func PartA(data [][]int, result chan interface{}) {
	sum := 0

	lowPoints := FindLowPoints(data)
	for _, point := range lowPoints {
		sum += data[point[0]][point[1]] + 1
	}

	result <- sum
}

func WasPointWasChecked(row int, column int, ignore map[int][]int) bool {
	if _, ok := ignore[row]; !ok {
		return false
	}

	for _, value := range ignore[row] {
		if value == column {
			return true
		}
	}

	return false
}

func IgnorePoint(row int, column int, ignore map[int][]int) map[int][]int {
	if _, ok := ignore[row]; !ok {
		ignore[row] = []int{column}
		return ignore
	}

	for _, value := range ignore[row] {
		if value == column {
			return ignore
		}
	}

	ignore[row] = append(ignore[row], column)
	return ignore
}

func AddSurroundingPoints(data [][]int, row int, column int, points [][]int, ignore map[int][]int) ([][]int, map[int][]int) {
	if row > 0 {
		if !WasPointWasChecked(row-1, column, ignore) {
			points = append(points, []int{row - 1, column})
			ignore = IgnorePoint(row-1, column, ignore)
		}
	}
	if row < len(data)-1 {
		if !WasPointWasChecked(row+1, column, ignore) {
			points = append(points, []int{row + 1, column})
			ignore = IgnorePoint(row+1, column, ignore)
		}
	}
	if column > 0 {
		if !WasPointWasChecked(row, column-1, ignore) {
			points = append(points, []int{row, column - 1})
			ignore = IgnorePoint(row, column-1, ignore)
		}
	}
	if column < len(data[row])-1 {
		if !WasPointWasChecked(row, column+1, ignore) {
			points = append(points, []int{row, column + 1})
			ignore = IgnorePoint(row, column+1, ignore)
		}
	}

	return points, ignore
}

func FindBasinSize(data [][]int, row int, column int) int {
	size := 0
	check := [][]int{[]int{row, column}}
	ignore := make(map[int][]int)

	for {
		currRow := check[0][0]
		currColumn := check[0][1]

		ignore = IgnorePoint(currRow, currColumn, ignore)

		if data[currRow][currColumn] != 9 {
			size++
			check, ignore = AddSurroundingPoints(data, currRow, currColumn, check, ignore)
		}

		if len(check) > 1 {
			check = check[1:]
		} else {
			break
		}
	}
	return size
}

func PartB(data [][]int, result chan interface{}) {
	sizes := make([]int, 0)

	lowPoints := FindLowPoints(data)
	for _, point := range lowPoints {
		sizes = append(sizes, FindBasinSize(data, point[0], point[1]))
	}

	sort.Sort(sort.Reverse(sort.IntSlice(sizes)))
	result <- sizes[0] * sizes[1] * sizes[2]
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

	a := make(chan interface{})
	b := make(chan interface{})

	go PartA(converted, a)
	go PartB(converted, b)

	fmt.Println("Part A:", <-a)
	fmt.Println("Part B:", <-b)
}
