// https://adventofcode.com/2020/day/14

package main

import (
	"fmt"
	"os"
	"strings"
	"utils/utils"
)

func ParseInput(data []string) (string, map[string]string) {
	template := data[0]
	rules := make(map[string]string)

	for _, rule := range data[2:] {
		ruleData := strings.Split(rule, " -> ")
		rules[ruleData[0]] = ruleData[1]
	}

	return template, rules
}

func GetDifference(count map[string]int) int {
	min := -1
	max := -1

	for _, count := range count {
		if count == 0 {
			continue
		}
		if count < min || min == -1 {
			min = count
		}
		if count > max || max == -1 {
			max = count
		}
	}

	return max - min
}

func Process(template string, rules map[string]string) (int, int) {
	_ = "Template:     NNCB"
	_ = "After step 1: NCNBCHB"
	_ = "After step 2: NBCCNBBBCBHCB"
	_ = "After step 3: NBBBCNCCNBBNBNBBCHBHHBCHB"
	_ = "After step 4: NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB"

	var a int
	var b int

	count := make(map[string]int)
	pieces := make(map[string]int)

	for index := 0; index < len(template); index++ {
		currForCount := string(template[index])
		if _, ok := count[currForCount]; !ok {
			count[currForCount] = 0
		}
		count[currForCount]++

		if index < len(template)-1 {
			currForPieces := template[index : index+2]
			if _, ok := pieces[currForPieces]; !ok {
				pieces[currForPieces] = 0
			}
			pieces[currForPieces]++
		}
	}

	for step := 0; step < 40; step++ {
		newPieces := make(map[string]int)
		for curr, pieceCount := range pieces {
			if pieceCount == 0 {
				continue
			}

			if _, ok := newPieces[curr]; !ok {
				newPieces[curr] = pieceCount
			} else {
				newPieces[curr] += pieceCount
			}

			if _, ok := rules[curr]; !ok {
				continue
			}

			newPiece := string(curr[0]) + rules[curr]
			if _, ok := newPieces[newPiece]; !ok {
				newPieces[newPiece] = 0
			}
			newPieces[newPiece] += pieceCount

			newPiece = rules[curr] + string(curr[1])
			if _, ok := newPieces[newPiece]; !ok {
				newPieces[newPiece] = 0
			}
			newPieces[newPiece] += pieceCount

			if _, ok := count[rules[curr]]; !ok {
				count[rules[curr]] = 0
			}
			count[rules[curr]] += pieceCount

			if newPieces[curr] >= pieceCount {
				newPieces[curr] -= pieceCount
			}
		}

		if step == 9 {
			a = GetDifference(count)
		}
		if step == 39 {
			b = GetDifference(count)
		}

		pieces = newPieces
	}

	return a, b
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

	template, rules := ParseInput(data)

	a, b := Process(template, rules)

	fmt.Println("Part A:", a)
	fmt.Println("Part B:", b)
}
