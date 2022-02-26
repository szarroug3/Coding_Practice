// https://adventofcode.com/2021/day/23

package main

import (
	"fmt"
	"math"
	"sort"
	"strconv"
)

func getModel(i int, z int, zPossibilities map[int]map[int][][]int, model string, max bool) string {
	if i == 14 {
		return model
	}

	sort.Slice(zPossibilities[i][z], func(j, k int) bool {
		if max {
			return zPossibilities[i][z][j][0] > zPossibilities[i][z][k][0]
		} else {
			return zPossibilities[i][z][j][0] < zPossibilities[i][z][k][0]
		}
	})

	for _, values := range zPossibilities[i][z] {
		model += strconv.Itoa(values[0])
		model = getModel(i+1, values[1], zPossibilities, model, max)
		if len(model) != 0 {
			return model
		}
	}
	return ""
}

func PartA() (string, string) {
	num1 := []int{1, 1, 1, 26, 26, 1, 1, 26, 1, 26, 1, 26, 26, 26}
	num2 := []int{12, 12, 12, -9, -9, 14, 14, -10, 15, -2, 11, -15, -9, -3}
	num3 := []int{9, 4, 2, 5, 1, 6, 11, 15, 7, 12, 15, 9, 12, 12}

	zPossibilities := map[int]map[int][][]int{14: {0: {}}}

	for i := 13; i >= 0; i-- {
		if _, ok := zPossibilities[i]; !ok {
			zPossibilities[i] = make(map[int][][]int)
		}

		for w := 9; w >= 1; w-- {
			for z := range zPossibilities[i+1] {
				for a := 0; a < num1[i]; a++ {
					oldz := z*num1[i] + a
					if oldz%26+num2[i] == w {
						if oldz/num1[i] == z {
							zPossibilities[i][oldz] = append(zPossibilities[i][oldz], []int{w, z})
						}
					}

					oldz = int(math.Round(float64((z-w-num3[i])/26*num1[i] + a)))
					if oldz%26+num2[i] != w {
						if oldz/num1[i]*26+w+num3[i] == z {
							zPossibilities[i][oldz] = append(zPossibilities[i][oldz], []int{w, z})
						}
					}
				}
			}
		}
	}

	return getModel(0, 0, zPossibilities, "", true), getModel(0, 0, zPossibilities, "", false)
}

func main() {
	a, b := PartA()

	fmt.Println("Part A:", a)
	fmt.Println("Part B:", b)
}
