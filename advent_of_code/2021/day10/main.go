// https://adventofcode.com/2021/day/10

package main

import (
	"fmt"
	"os"
	"sort"
	"utils/utils"
)

func IsIllegal(data []rune) (bool, rune, []rune) {
	seen := make([]rune, 0)
	for _, curr := range data {
		if curr == '(' || curr == '[' || curr == '{' || curr == '<' {
			seen = append(seen, curr)
		} else {
			switch seen[len(seen)-1] {
			case '(':
				if curr != ')' {
					return true, curr, seen
				}
			case '[':
				if curr != ']' {
					return true, curr, seen
				}
			case '{':
				if curr != '}' {
					return true, curr, seen
				}
			case '<':
				if curr != '>' {
					return true, curr, seen
				}
			}
			if len(seen) == 1 {
				seen = make([]rune, 0)
			} else {
				seen = seen[:len(seen)-1]
			}
		}
	}

	return false, ' ', seen
}

func PartA(data [][]rune, result chan interface{}) {
	illegal := map[rune]int{
		')': 3,
		']': 57,
		'}': 1197,
		'>': 25137,
	}

	sum := 0
	for _, line := range data {
		bad, value, _ := IsIllegal(line)
		if bad {
			sum += illegal[value]
		}
	}

	result <- sum
}

func GetCompleterScore(data []rune) int {
	completion := make([]rune, 0)
	for i := len(data) - 1; i >= 0; i-- {
		curr := data[i]
		switch curr {
		case '(':
			completion = append(completion, ')')
		case '[':
			completion = append(completion, ']')
		case '{':
			completion = append(completion, '}')
		case '<':
			completion = append(completion, '>')
		}
	}

	completer := map[rune]int{
		')': 1,
		']': 2,
		'}': 3,
		'>': 4,
	}

	score := 0
	for _, curr := range completion {
		score *= 5
		score += completer[curr]
	}

	return score
}

func PartB(data [][]rune, result chan interface{}) {
	scores := make([]int, 0)
	for _, line := range data {
		bad, _, incomplete := IsIllegal(line)
		if !bad {
			scores = append(scores, GetCompleterScore(incomplete))
		}
	}

	sort.Ints(scores)
	middleIndex := (len(scores) - 1) / 2

	result <- scores[middleIndex]
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

	a := make(chan interface{})
	b := make(chan interface{})

	go PartA(data, a)
	go PartB(data, b)

	fmt.Println("Part A:", <-a)
	fmt.Println("Part B:", <-b)
}
