// https://adventofcode.com/2020/day/6

package main

import (
	"fmt"
	"os"
	"strings"
	"utils/utils"
)

func GetUniqueResponses(data [][]string) []string {
	responses := make([]string, 0)
	group := ""

	for _, answers := range data {
		if len(answers) == 0 {
			responses = append(responses, group)
			group = ""
			continue
		}

		for _, answer := range strings.Join(answers, "") {
			if !strings.Contains(group, string(answer)) {
				group = group + string(answer)
			}
		}
	}
	responses = append(responses, group)

	return responses
}

func GetMatchingResponses(data [][]string) []string {
	responses := make([]string, 0)
	people := 0
	group := make(map[string]int, 0)

	for _, answers := range data {
		if len(answers) == 0 {
			curr := ""
			for answer, count := range group {
				if count == people {
					curr = curr + answer
				}
			}
			responses = append(responses, curr)

			people = 0
			group = make(map[string]int, 0)
			continue
		}

		people = people + 1
		for _, answer := range strings.Join(answers, "") {
			answer_str := string(answer)
			if _, ok := group[answer_str]; ok {
				group[answer_str] = group[answer_str] + 1
			} else {
				group[answer_str] = 1
			}
		}
	}

	curr := ""
	for answer, count := range group {
		if count == people {
			curr = curr + answer
		}
	}
	responses = append(responses, curr)

	return responses
}

func PartA(data [][]string, result chan interface{}) {
	responses := GetUniqueResponses(data)
	total := 0

	for _, group := range responses {
		total = total + len(group)
	}

	result <- total
}

func PartB(data [][]string, result chan interface{}) {
	responses := GetMatchingResponses(data)
	total := 0

	for _, group := range responses {
		total = total + len(group)
	}

	result <- total
	result <- "UPDATE THIS"
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Input filename required.")
		return
	}

	data, err := utils.ReadFileAsStringSlices(os.Args[1], "\n")
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
