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
