// https://adventofcode.com/2020/day/2

package main

import (
	"fmt"
	"os"
	"regexp"
	"strconv"
	"strings"
	"utils/utils"
)

type Password struct {
	first_int  int
	second_int int
	letter     string
	password   string
}

func ParseData(data string) []Password {
	re := regexp.MustCompile("(\\d+)-(\\d+) (.): (.*)")
	parsed := make([]Password, 0)
	for _, match := range re.FindAllStringSubmatch(data, -1) {
		first_int, _ := strconv.Atoi(match[1])
		second_int, _ := strconv.Atoi(match[2])
		parsed = append(parsed, Password{
			first_int:  first_int,
			second_int: second_int,
			letter:     match[3],
			password:   match[4]})
	}

	return parsed
}

func PartA(passwords []Password, result chan interface{}) {
	valid := 0
	var count int

	for _, password := range passwords {
		count = strings.Count(password.password, password.letter)
		if password.first_int <= count && count <= password.second_int {
			valid++
		}
	}

	result <- valid
}

func PartB(passwords []Password, result chan interface{}) {
	valid := 0
	var a, b, letter byte

	for _, password := range passwords {
		a = []byte(password.password)[password.first_int-1]
		b = []byte(password.password)[password.second_int-1]
		letter = []byte(password.letter)[0]

		if (a == letter || b == letter) && a != b {
			valid++
		}
	}

	result <- valid
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Input filename required.")
		return
	}

	data, err := utils.ReadFileAsString(os.Args[1])
	if err != nil {
		fmt.Println(err)
		return
	}

	parsed := ParseData(data)

	a := make(chan interface{})
	b := make(chan interface{})

	go PartA(parsed, a)
	go PartB(parsed, b)

	fmt.Println("Part A:", <-a)
	fmt.Println("Part B:", <-b)
}
