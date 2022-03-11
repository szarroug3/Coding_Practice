package main

import "fmt"

func ackermann(a int, b int, c int, results map[int]map[int]int) int {
	if values, ok := results[a]; ok {
		if value, ok := values[b]; ok {
			return value
		}
	}

	result := 0
	if a == 0 {
		result = (b + 1) % 32768
	} else if b == 0 {
		result = ackermann(a-1, c, c, results)
	} else {
		result = ackermann(a, b-1, c, results)
		result = ackermann(a-1, result, c, results)
	}

	if _, ok := results[a]; !ok {
		results[a] = make(map[int]int)
	}
	results[a][b] = result

	return result
}

func main() {
	for i := 1; i < 32769; i++ {
		result := ackermann(4, 1, i, make(map[int]map[int]int))
		if result == 6 {
			fmt.Println(i)
			break
		}
	}
}
