// https://adventofcode.com/2020/day/4

package main

import (
	"fmt"
	"os"
	"regexp"
	"strconv"
	"utils/utils"
)

type Credentials struct {
	birth_year      int
	issue_year      int
	expiration_year int
	height          string
	hair_color      string
	eye_color       string
	passport_id     string
	country_id      string
}

func Parse(data []string) []Credentials {
	re := regexp.MustCompile("(\\S+):(\\S+)")
	parsed := make([]Credentials, 0)
	var int_value int
	for _, id := range data {
		var credentials Credentials
		for _, match := range re.FindAllStringSubmatch(id, -1) {
			key := match[1]
			value := match[2]

			switch key {
			case "byr":
				int_value, _ = strconv.Atoi(value)
				credentials.birth_year = int_value
			case "iyr":
				int_value, _ = strconv.Atoi(value)
				credentials.issue_year = int_value
			case "eyr":
				int_value, _ = strconv.Atoi(value)
				credentials.expiration_year = int_value
			case "hgt":
				credentials.height = value
			case "hcl":
				credentials.hair_color = value
			case "ecl":
				credentials.eye_color = value
			case "pid":
				credentials.passport_id = value
			case "cid":
				credentials.country_id = value
			}
		}
		parsed = append(parsed, credentials)
	}

	return parsed
}

func ValidHeight(data string) bool {
	re := regexp.MustCompile("(\\d+)(\\S+)")
	match := re.FindStringSubmatch(data)
	if len(match) < 3 {
		return false
	}

	unit := match[2]
	if unit != "cm" && unit != "in" {
		return false
	}

	height, err := strconv.Atoi(match[1])
	if err != nil {
		return false
	}

	if unit == "cm" {
		if height < 150 || height > 193 {
			return false
		}
	} else {
		if height < 59 || height > 76 {
			return false
		}
	}

	return true
}

func ValidHairColor(color string) bool {
	re := regexp.MustCompile("#[a-f0-9]{6}")
	match := re.MatchString(color)
	if !match {
		return false
	}
	return true
}

func ValidEyeColor(color string) bool {
	if color == "amb" {
		return true
	}
	if color == "blu" {
		return true
	}
	if color == "brn" {
		return true
	}
	if color == "gry" {
		return true
	}
	if color == "grn" {
		return true
	}
	if color == "hzl" {
		return true
	}
	if color == "oth" {
		return true
	}
	return false
}

func ValidPassportId(data string) bool {
	if len(data) != 9 {
		return false
	}

	_, err := strconv.Atoi(data)
	if err != nil {
		return false
	}

	return true
}

func PartA(credentials []Credentials, result chan interface{}) {
	count := 0

	for _, id := range credentials {
		switch {
		case id.birth_year == 0:
			continue
		case id.issue_year == 0:
			continue
		case id.expiration_year == 0:
			continue
		case id.height == "":
			continue
		case id.hair_color == "":
			continue
		case id.eye_color == "":
			continue
		case id.passport_id == "":
			continue
		default:
			count++
		}
	}

	result <- count
}

func PartB(credentials []Credentials, result chan interface{}) {
	count := 0

	for _, id := range credentials {
		switch {
		case id.birth_year < 1920 || id.birth_year > 2002:
			continue
		case id.issue_year < 2010 || id.issue_year > 2020:
			continue
		case id.expiration_year < 2020 || id.expiration_year > 2030:
			continue
		case !ValidHeight(id.height):
			continue
		case !ValidHairColor(id.hair_color):
			continue
		case !ValidEyeColor(id.eye_color):
			continue
		case !ValidPassportId(id.passport_id):
			continue
		default:
			count++
		}
	}

	result <- count
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Input filename required.")
		return
	}

	data, err := utils.ReadFileAsSlices(os.Args[1], "\n\n")
	if err != nil {
		fmt.Println(err)
		return
	}

	parsed := Parse(data)

	a := make(chan interface{})
	b := make(chan interface{})

	go PartA(parsed, a)
	go PartB(parsed, b)

	fmt.Println("Part A:", <-a)
	fmt.Println("Part B:", <-b)
}
