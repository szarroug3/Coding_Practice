// https://adventofcode.com/2020/day/18

package main

import (
	"fmt"
	"os"
	"regexp"
	"strconv"
	"utils/utils"
)

type Value struct {
	Value    int
	Position int
}

type Child struct {
	Value    *Pair
	Position int
}

type Pair struct {
	Values          []Value
	Children        []*Child
	Parent          *Pair
	PositionCounter int
	Depth           int
}

func prettyPrint(pair Pair, indentation string) string {
	result := fmt.Sprintf("%s[\n", indentation)
	result += fmt.Sprintf("%sDepth: %v", indentation+indentation, pair.Depth)
	if len(pair.Values) > 0 {
		result += fmt.Sprintf(", Values: %v", pair.Values)
	}
	result += "\n"

	if len(pair.Children) > 0 {
		result += fmt.Sprintf("%sChildren:\n", indentation+indentation)
		for _, child := range pair.Children {
			result += fmt.Sprintf("%d: %s\n", child.Position, prettyPrint(*child.Value, indentation+indentation))
		}
	}

	result += fmt.Sprintf("   %s]\n", indentation)
	return result
}

func Parse(pair Pair, data string) Pair {
	depth := 0
	curr := &pair

	for _, char := range data {
		currValue := ""
		for {
			if char == '[' || char == ']' || char == ',' {
				if currValue != "" {
					value, _ := strconv.Atoi(currValue)
					curr.Values = append(curr.Values, Value{Value: value, Position: curr.PositionCounter})
					curr.PositionCounter++
				}
				break
			}
			currValue += string(char)
		}

		if char == '[' {
			depth++
			newPair := Pair{Values: make([]Value, 0), Children: make([]*Child, 0), Parent: curr, PositionCounter: 0, Depth: depth}
			curr.Children = append(curr.Children, &Child{Value: &newPair, Position: curr.PositionCounter})
			curr.PositionCounter++
			curr = &newPair
		} else if char == ']' {
			depth--
			curr = curr.Parent
		}

	}

	fmt.Println(prettyPrint(pair, "  "))
	fmt.Println("---")

	return pair
}

func Add(data string, line string) string {
	return fmt.Sprintf("[%s,%s]", data, line)
}

func Explode(data string) (string, bool) {
	depth := 0
	commas := 0
	start := -1
	end := -1
	comma := -1

	for i, char := range data {
		if char == '[' {
			depth++
			commas = 0
			start = i
		} else if char == ']' {
			if commas == 1 && depth > 4 {
				end = i
				break
			}

			depth--
			commas = 0
		} else if char == ',' {
			commas++
			comma = i
		}
	}

	if end == -1 {
		return data, false
	}

	left, _ := strconv.Atoi(data[start+1 : comma])
	right, _ := strconv.Atoi(data[comma+1 : end])
	data = fmt.Sprintf("%s0%s", data[:start], data[end+1:])

	re := regexp.MustCompile(`\d+`)

	loc := re.FindStringIndex(data[start+1:])
	if loc != nil {
		value, _ := strconv.Atoi(data[start+loc[0]+1 : start+loc[1]+1])
		data = fmt.Sprintf("%s%d%s", data[:start+loc[0]+1], right+value, data[start+loc[1]+1:])
	}

	matches := re.FindAllStringIndex(data[:start], -1)
	if matches != nil {
		loc := matches[len(matches)-1]
		value, _ := strconv.Atoi(data[loc[0]:loc[1]])
		data = fmt.Sprintf("%s%d%s", data[:loc[0]], left+value, data[loc[1]:])
	}

	return data, true
}

func Split(data string) (string, bool) {
	re := regexp.MustCompile(`\d\d+`)
	loc := re.FindStringIndex(data)
	if loc == nil {
		return data, false
	}

	value, _ := strconv.Atoi(data[loc[0]:loc[1]])
	left := value / 2
	right := left
	if value%2 != 0 {
		right++
	}
	data = fmt.Sprintf("%s[%d,%d]%s", data[:loc[0]], left, right, data[loc[1]:])

	return data, true
}

func Reduce(data string) string {
	for {
		var explode bool
		var split bool

		data, explode = Explode(data)
		if explode {
			continue
		}

		data, split = Split(data)
		if !split {
			return data
		}
	}
}

func Calculate(data string) int {
	re := regexp.MustCompile(`\[(\d+),(\d+)\]`)
	for {
		matches := re.FindAllStringSubmatchIndex(data, -1)
		if matches == nil {
			break
		}

		for i := len(matches) - 1; i >= 0; i-- {
			loc := matches[i]
			left, _ := strconv.Atoi(data[loc[2]:loc[3]])
			right, _ := strconv.Atoi(data[loc[4]:loc[5]])
			magnitude := (3 * left) + (2 * right)
			data = fmt.Sprintf("%s%d%s", data[:loc[0]], magnitude, data[loc[1]:])
		}
	}

	magnitude, _ := strconv.Atoi(data)
	return magnitude
}

func PartA(data []string, result chan interface{}) {
	curr := data[0]
	for _, line := range data[1:] {
		curr = Add(curr, line)
		curr = Reduce(curr)
	}
	result <- Calculate(curr)
}

func PartB(data []string, result chan interface{}) {
	max := 0
	for i := 0; i < len(data)-1; i++ {
		for j := i + 1; j < len(data); j++ {
			curr := Add(data[i], data[j])
			curr = Reduce(curr)

			magnitude := Calculate(curr)
			if magnitude > max {
				max = magnitude
			}

			curr = Add(data[j], data[i])
			curr = Reduce(curr)

			magnitude = Calculate(curr)
			if magnitude > max {
				max = magnitude
			}
		}
	}
	result <- max
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

	a := make(chan interface{})
	b := make(chan interface{})

	go PartA(data, a)
	go PartB(data, b)

	fmt.Println("Part A:", <-a)
	fmt.Println("Part B:", <-b)
}
