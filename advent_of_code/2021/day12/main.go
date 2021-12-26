// https://adventofcode.com/2020/day/12

package main

import (
	"fmt"
	"os"
	// "reflect"
	"strings"
	"utils/utils"
)

func CreateMap(data [][]string) map[string][]string {
	paths := make(map[string][]string)

	for _, line := range data {
		pointA := line[0]
		pointB := line[1]
		if pointA == pointB {
			continue
		}

		if _, ok := paths[pointA]; !ok {
			paths[pointA] = make([]string, 0)
		}
		if _, ok := paths[pointB]; !ok {
			paths[pointB] = make([]string, 0)
		}

		add := true
		for _, added := range paths[pointA] {
			if added == pointB {
				add = false
				break
			}
		}

		if !add {
			continue
		}

		if pointB != "start" {
			paths[pointA] = append(paths[pointA], pointB)
		}
		if pointA != "start" {
			paths[pointB] = append(paths[pointB], pointA)
		}
	}

	return paths
}

func CanVisitA(point string, visited []string) bool {
	if strings.ToUpper(point) == point {
		return true
	}

	for _, location := range visited {
		if point == location {
			return false
		}
	}

	return true
}

func GetPossiblePathsA(paths map[string][]string, starting string, visited []string, possiblePaths [][]string) [][]string {
	for _, point := range paths[starting] {
		visitedCopy := make([]string, len(visited))
		copy(visitedCopy, visited)

		if !CanVisitA(point, visitedCopy) {
			continue
		}

		visitedCopy = append(visitedCopy, point)

		if point == "end" {
			possiblePaths = append(possiblePaths, visitedCopy)
			continue
		}

		possiblePaths = GetPossiblePathsA(paths, point, visitedCopy, possiblePaths)
	}

	return possiblePaths
}

func PartA(data [][]string, result chan interface{}) {
	pathMap := CreateMap(data)
	visited := []string{"start"}
	possiblePaths := make([][]string, 0)

	possiblePaths = GetPossiblePathsA(pathMap, "start", visited, possiblePaths)
	result <- len(possiblePaths)
}

func CanVisitB(point string, visitCount map[string]int, skip []string) bool {
	if strings.ToUpper(point) == point {
		return true
	}

	if _, ok := visitCount[point]; !ok {
		return true
	}

	for location, count := range visitCount {
		if strings.ToUpper(location) == location {
			continue
		}

		if count == 2 {
			return false
		}

		if location != point {
			continue
		}

		for _, skipPoint := range skip {
			if skipPoint == point {
				return false
			}
		}

	}

	return true
}

func GetPossiblePathsB(paths map[string][]string, starting string, visitCount map[string]int, skip []string, count int) int {
	for _, point := range paths[starting] {
		visitCountCopy := make(map[string]int)
		for location, count := range visitCount {
			visitCountCopy[location] = count
		}

		if !CanVisitB(point, visitCountCopy, skip) {
			continue
		}

		if _, ok := visitCountCopy[point]; !ok {
			visitCountCopy[point] = 0
		}
		visitCountCopy[point]++

		if point == "end" {
			if len(skip) == 0 {
				count++
			}
			continue
		}

		count = GetPossiblePathsB(paths, point, visitCountCopy, skip, count)

		if strings.ToLower(point) == point && point != "start" {
			skipCopy := append(skip, point)
			count = GetPossiblePathsB(paths, point, visitCountCopy, skipCopy, count)
		}
	}

	return count
}

func PartB(data [][]string, result chan interface{}) {
	pathMap := CreateMap(data)
	visitCount := make(map[string]int)
	skip := make([]string, 0)

	count := GetPossiblePathsB(pathMap, "start", visitCount, skip, 0)
	result <- count
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Input filename required.")
		return
	}

	data, err := utils.ReadFileAsStringSlices(os.Args[1], "\n", "-")
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
