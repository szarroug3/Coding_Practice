// https://adventofcode.com/2020/day/5

package main

import (
	"fmt"
	"os"
	"utils/utils"
)

func GetHalf(min int, max int, data rune)  (int, int) {
	diff := max - min
	lower := min
	upper := max
	lower_mid := int(float64(diff) / 2.0) + min
	upper_mid := lower_mid + 1

	if data == 'F' || data == 'L' {
		return lower, lower_mid
	} else {
		return upper_mid, upper
	}
}

func GetSeat(data []rune) int {
	var row, column int

	min := 0
	max := 127
	for i := 0; i < 6; i++ {
		min, max = GetHalf(min, max, data[i])
	}

	if data[6] == 'F' {
		row = min
	} else {
		row = max
	}

	min = 0
	max = 7
	for i := 7; i < 10; i++ {
		min, max = GetHalf(min, max, data[i])
	}

	if data[6] == 'L' {
		column = min
	} else {
		column = max
	}

	return (row * 8) + column
}

func GetSeatMap(data [][]rune) map[int][]rune {
	seat_map := make(map[int][]rune, 0)
	var id int

	for _, boarding_pass := range data {
		id = GetSeat(boarding_pass)
		seat_map[id] = boarding_pass
	}

	return seat_map
}

func GetMinMapKey(data map[int][]rune) int {
	var min int
	set := false

	for key := range data {
		if !set {
			min = key
			set = true
		}
		if key < min {
			min = key
		}
	}

	return min
}

func GetMaxMapKey(data map[int][]rune) int {
	var max int
	set := false

	for key := range data {
		if !set {
			max = key
			set = true
		}
		if key > max {
			max = key
		}
	}

	return max
}
func PartA(seat_map map[int][]rune, result chan interface{}) {
	result <- GetMinMapKey(seat_map)
}

func PartB(seat_map map[int][]rune, result chan interface{}) {
	min := GetMinMapKey(seat_map)
	max := GetMaxMapKey(seat_map)

	fmt.Println(min, max)
	for i := min+1; i < max; i++ {
		// This seat is taken
		if _, ok := seat_map[i]; ok {
			continue
		}

		// The seat with id one less than the current one isn't taken
		if _, ok := seat_map[i-1]; !ok {
			continue
		}

		// The seat with id one more than the current one isn't taken
		if _, ok := seat_map[i+1]; !ok {
			continue
		}

		result <- i
		return
	}

	result <- "Could not find valid seat ID."
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Input filename required.")
		return
	}

	data, err := utils.ReadFileAsRuneSlices(os.Args[1], "\n")
	if err != nil {
		fmt.Println(err)
		return
	}

	seat_map := GetSeatMap(data)
	a := make(chan interface{})
	b := make(chan interface{})

	go PartA(seat_map, a)
	go PartB(seat_map, b)

	fmt.Println("Part A:", <-a)
	fmt.Println("Part B:", <-b)
}
