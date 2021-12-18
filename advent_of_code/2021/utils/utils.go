package utils

import (
	"strconv"
)

func ConvertToInts(data []string) []int {
	values := make([]int, 0)
	var converted int
	for _, value := range data {
		converted, _ = strconv.Atoi(value)
		values = append(values, converted)
	}

	return values
}

func ConvertAllToInts(data [][]string) [][]int {
	values := make([][]int, 0)
	for _, value := range data {
		values = append(values, ConvertToInts(value))
	}

	return values
}
