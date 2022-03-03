// https://adventofcode.com/2021/day/8

package main

import (
	"errors"
	"fmt"
	"os"
	"sort"
	"strconv"
	"strings"
	"utils/utils"
)

func PartA(output [][]string, result chan interface{}) {
	count := 0

	for _, line := range output {
		for _, data := range line {
			switch len(data) {
			case 2, 3, 4, 7:
				count++
			}
		}
	}

	result <- count
}

func GetUniqueValues(input []string) (string, string, string, string, error) {
	var one string
	var four string
	var seven string
	var eight string

	for _, data := range input {
		switch len(data) {
		case 2:
			one = data
		case 3:
			seven = data
		case 4:
			four = data
		case 7:
			eight = data
		}
		if one != "" && four != "" && seven != "" && eight != "" {
			return one, four, seven, eight, nil
		}
	}

	return "", "", "", "", errors.New("Could not find unique values")
}

func FindZero(input []string, six string, nine string) (string, error) {
	for _, data := range input {
		if len(data) == 6 && data != six && data != nine {
			return data, nil
		}
	}

	return "", errors.New("Could not find value for zero")
}

func FindTwo(input []string, three string, five string) (string, error) {
	for _, data := range input {
		if len(data) == 5 && data != three && data != five {
			return data, nil
		}
	}

	return "", errors.New("Could not find value for two")
}

func FindThree(input []string, five string) (string, error) {
	for _, data := range input {
		if len(data) != 5 || data == five {
			continue
		}

		count := 0
		good := true
		for _, char := range five {
			if strings.ContainsRune(data, char) {
				count++
			}

			if count > 4 {
				good = false
				break
			}
		}

		if !good || count != 4 {
			continue
		}

		return data, nil
	}

	return "", errors.New("Could not find value for three")
}

func FindFive(input []string, six string) (string, error) {
	for _, data := range input {
		if len(data) != 5 {
			continue
		}

		good := true
		for _, char := range data {
			if !strings.ContainsRune(six, char) {
				good = false
				break
			}
		}

		if !good {
			continue
		}

		return data, nil
	}

	return "", errors.New("Could not find value for five")
}

func FindSix(input []string, seven string) (string, error) {
	for _, data := range input {
		if len(data) != 6 {
			continue
		}

		count := 0
		good := true
		for _, char := range seven {
			if strings.ContainsRune(data, char) {
				count++
			}

			if count > 2 {
				good = false
				break
			}
		}

		if !good || count != 2 {
			continue
		}

		return data, nil
	}

	return "", errors.New("Could not find value for six")
}

func FindNine(input []string, five string, six string) (string, error) {
	for _, data := range input {
		if len(data) != 6 || data == six {
			continue
		}

		good := true
		for _, char := range five {
			if !strings.ContainsRune(data, char) {
				good = false
				break
			}
		}

		if !good {
			continue
		}

		return data, nil
	}

	return "", errors.New("Could not find value for nine")
}

func SortString(data string) string {
	split := strings.Split(data, "")
	sort.Strings(split)
	return strings.Join(split, "")
}

func PartB(input [][]string, output [][]string, result chan interface{}) {
	total := 0

	for index, line := range input {
		one, four, seven, eight, err := GetUniqueValues(line)
		if err != nil {
			result <- err
			return
		}

		six, err := FindSix(line, seven)
		if err != nil {
			result <- err
			return
		}

		five, err := FindFive(line, six)
		if err != nil {
			result <- err
			return
		}

		three, err := FindThree(line, five)
		if err != nil {
			result <- err
			return
		}

		two, err := FindTwo(line, three, five)
		if err != nil {
			result <- err
			return
		}

		nine, err := FindNine(line, five, six)
		if err != nil {
			result <- err
			return
		}

		zero, err := FindZero(line, six, nine)
		if err != nil {
			result <- err
			return
		}

		numbers := make(map[string]string)
		numbers[SortString(zero)] = "0"
		numbers[SortString(one)] = "1"
		numbers[SortString(two)] = "2"
		numbers[SortString(three)] = "3"
		numbers[SortString(four)] = "4"
		numbers[SortString(five)] = "5"
		numbers[SortString(six)] = "6"
		numbers[SortString(seven)] = "7"
		numbers[SortString(eight)] = "8"
		numbers[SortString(nine)] = "9"

		value := ""
		for _, curr := range output[index] {
			value += numbers[SortString(curr)]
		}

		converted, _ := strconv.Atoi(value)
		total += converted
	}

	result <- total
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

	input := make([][]string, 0)
	output := make([][]string, 0)
	for _, line := range data {
		split := strings.Split(line, " | ")
		input = append(input, strings.Split(split[0], " "))
		output = append(output, strings.Split(split[1], " "))
	}

	a := make(chan interface{})
	b := make(chan interface{})

	go PartA(output, a)
	go PartB(input, output, b)

	fmt.Println("Part A:", <-a)
	fmt.Println("Part B:", <-b)
}
