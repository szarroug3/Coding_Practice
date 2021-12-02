package utils

import (
	"io/ioutil"
	"strings"
)

func ReadFileAsString(filename string) (string, error) {
	data, err := ioutil.ReadFile(filename)
	if err != nil {
		return "", err
	}

	return strings.TrimSpace(string(data)), nil
}

func ReadFileAsSlices(filename string, delimiter string) ([]string, error) {
	data, err := ReadFileAsString(filename)
	if err != nil {
		return nil, err
	}

	return strings.Split(data, delimiter), nil
}

func ReadFileAsRuneSlices(filename string, delimiter string) ([][]rune, error) {
	split := make([][]rune, 0)

	data, err := ReadFileAsSlices(filename, delimiter)
	if err != nil {
		return split, err
	}

	for _, line := range data {
		split = append(split, []rune(line))
	}

	return split, nil
}

func ReadFileAsStringSlices(filename string, delimiter string, lineDelimiter string) ([][]string, error) {
	split := make([][]string, 0)

	data, err := ReadFileAsSlices(filename, delimiter)
	if err != nil {
		return split, err
	}

	for _, line := range data {
		curr := make([]string, 0)
		for _, char := range strings.Split(line, lineDelimiter) {
			char = strings.TrimSpace(char)

			if char != "" {
				curr = append(curr, char)
			}
		}
		split = append(split, curr)
	}

	return split, nil
}
