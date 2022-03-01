// https://adventofcode.com/2021/day/5

package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
	"utils/utils"
)

type point struct {
	x int
	y int
}

type line struct {
	start point
	end   point
}

func Line(data string) line {
	lineData := strings.Split(data, " -> ")
	return line{start: Point(lineData[0]), end: Point(lineData[1])}
}

func Point(data string) point {
	points := strings.Split(data, ",")
	x, _ := strconv.Atoi(points[0])
	y, _ := strconv.Atoi(points[1])
	return point{x: x, y: y}
}

func ParseInput(data []string) []line {
	coordinates := make([]line, 0)
	for _, line := range data {
		coordinates = append(coordinates, Line(line))
	}

	return coordinates
}

func TraverseStraightLine(count map[int]map[int]int, data line) map[int]map[int]int {
	xStart := data.start.x
	xEnd := data.end.x
	yStart := data.start.y
	yEnd := data.end.y

	if xStart > xEnd || yStart > yEnd {
		xStart = data.end.x
		xEnd = data.start.x
		yStart = data.end.y
		yEnd = data.start.y
	}

	for x := xStart; x <= xEnd; x++ {
		for y := yStart; y <= yEnd; y++ {
			if _, ok := count[x]; !ok {
				count[x] = make(map[int]int)
			}
			if _, ok := count[x][y]; !ok {
				count[x][y] = 0
			}
			count[x][y]++
		}
	}
	return count
}

func Add(value int) int {
	return value + 1
}

func Subtract(value int) int {
	return value - 1
}

func TraverseDiagonalLine(count map[int]map[int]int, data line) map[int]map[int]int {
	xStart := data.start.x
	xEnd := data.end.x
	yStart := data.start.y
	yEnd := data.end.y
	xFunc := Add
	yFunc := Add

	if xStart > xEnd {
		xStart = data.end.x
		xEnd = data.start.x
		yStart = data.end.y
		yEnd = data.start.y
	}
	if yStart > yEnd {
		yFunc = Subtract
	}

	x := xStart
	y := yStart
	for x <= xEnd {
		if _, ok := count[x]; !ok {
			count[x] = make(map[int]int)
		}
		if _, ok := count[x][y]; !ok {
			count[x][y] = 0
		}
		count[x][y]++
		x = xFunc(x)
		y = yFunc(y)
	}
	return count
}

func CountMultipleTraversals(count map[int]map[int]int) int {
	result := 0
	for _, data := range count {
		for _, value := range data {
			if value > 1 {
				result += 1
			}
		}
	}

	return result
}

func PartA(lines []line, result chan interface{}) {
	count := make(map[int]map[int]int)
	for _, line := range lines {
		if line.start.x != line.end.x && line.start.y != line.end.y {
			continue
		}

		count = TraverseStraightLine(count, line)
	}

	result <- CountMultipleTraversals(count)
}

func PartB(lines []line, result chan interface{}) {
	count := make(map[int]map[int]int)
	for _, line := range lines {
		if line.start.x != line.end.x && line.start.y != line.end.y {
			count = TraverseDiagonalLine(count, line)
		} else {
			count = TraverseStraightLine(count, line)
		}
	}

	result <- CountMultipleTraversals(count)
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

	points := ParseInput(data)

	a := make(chan interface{})
	b := make(chan interface{})

	go PartA(points, a)
	go PartB(points, b)

	fmt.Println("Part A:", <-a)
	fmt.Println("Part B:", <-b)
}
