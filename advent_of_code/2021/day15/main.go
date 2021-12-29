// https://adventofcode.com/2020/day/15

package main

import (
	"fmt"
	"os"
	"utils/utils"
)

type Point struct {
	row    int
	column int
}

func GetNeighbors(data [][]int, point Point) []Point {
	points := make([]Point, 0)

	if point.row > 0 {
		points = append(points, Point{row: point.row - 1, column: point.column})
	}

	if point.row < len(data)-1 {
		points = append(points, Point{row: point.row + 1, column: point.column})
	}

	if point.column > 0 {
		points = append(points, Point{row: point.row, column: point.column - 1})
	}

	if point.column < len(data[point.row])-1 {
		points = append(points, Point{row: point.row, column: point.column + 1})
	}

	return points
}

func GetShortest(data [][]int) int {
	distances := make(map[Point]int)
	visit := []Point{Point{row: 0, column: 0}}

	for {
		newVisit := make([]Point, 0)
		for _, point := range visit {
			for _, neighbor := range GetNeighbors(data, point) {
				newDistance := distances[point] + data[neighbor.row][neighbor.column]
				if _, ok := distances[neighbor]; !ok {
					distances[neighbor] = newDistance
					newVisit = append(newVisit, neighbor)
				}

				if newDistance < distances[neighbor] {
					distances[neighbor] = newDistance
					newVisit = append(newVisit, neighbor)
				}
			}
		}

		if len(visit) == 0 {
			break
		}

		visit = newVisit

	}

	endingRow := len(data) - 1
	endingColumn := len(data[endingRow]) - 1

	return distances[Point{row: endingRow, column: endingColumn}]
}

func PartA(data [][]int, result chan interface{}) {
	result <- GetShortest(data)
}

func PartB(data [][]int, result chan interface{}) {
	rowLen := len(data)
	columnLen := len(data[0])
	newData := make([][]int, 0)

	for _, line := range data {
		newLine := make([]int, len(line))
		copy(newLine, line)
		newData = append(newData, newLine)
	}

	data = newData
	for step := 1; step < 5; step++ {
		for i := 0; i < rowLen; i++ {
			for j := 0; j < columnLen; j++ {
				newValue := data[i][j] + step
				for newValue > 9 {
					newValue -= 9
				}
				data[i] = append(data[i], newValue)
			}
		}
	}

	for step := 1; step < 5; step++ {
		for row := 0; row < rowLen; row++ {
			newRow := make([]int, 0)
			for column := 0; column < len(data[row]); column++ {
				newValue := data[row][column] + step
				for newValue > 9 {
					newValue -= 9
				}
				newRow = append(newRow, newValue)
			}
			data = append(data, newRow)
		}
	}

	result <- GetShortest(data)
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
