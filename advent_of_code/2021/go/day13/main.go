// https://adventofcode.com/2021/day/13

package main

import (
	"fmt"
	"os"
	"sort"
	"strconv"
	"strings"
	"utils/utils"
)

type FoldInstruction struct {
	axis  string
	value int
}

func ParseData(data []string) (map[int][]int, []FoldInstruction) {
	sheet := make(map[int][]int)
	instructions := make([]FoldInstruction, 0)

	i := 0
	for i < len(data) {
		line := data[i]
		i++

		if line == "" {
			break
		}

		values := strings.Split(line, ",")
		column, _ := strconv.Atoi(values[0])
		row, _ := strconv.Atoi(values[1])

		if _, ok := sheet[row]; !ok {
			sheet[row] = make([]int, 0)
		}
		sheet[row] = append(sheet[row], column)
	}

	for i < len(data) {
		line := data[i]
		foldInstructions := strings.Split(strings.Split(line, " ")[2], "=")
		splitLocation, _ := strconv.Atoi(foldInstructions[1])
		foldData := FoldInstruction{
			axis:  foldInstructions[0],
			value: splitLocation,
		}
		instructions = append(instructions, foldData)
		i++
	}

	return sheet, instructions
}

func GetIndex(array []int, value int) int {
	for index, curr := range array {
		if curr == value {
			return index
		}
	}
	return -1
}

func FoldX(sheet map[int][]int, foldColumn int) map[int][]int {
	for row, columns := range sheet {
		index := GetIndex(columns, foldColumn)
		if index == -1 {
			continue
		}

		sheet[row] = append(columns[:index], columns[index+1:]...)
	}

	for row, _ := range sheet {
		rowLength := len(sheet[row])
		for index := 0; index < rowLength; index++ {
			column := sheet[row][index]
			if column <= foldColumn {
				continue
			}

			sheet[row] = append(sheet[row][:index], sheet[row][index+1:]...)
			index--
			rowLength--

			newColumn := foldColumn + foldColumn - column
			if GetIndex(sheet[row], newColumn) == -1 {
				sheet[row] = append(sheet[row], newColumn)
				rowLength++
			}

		}
	}

	return sheet
}

func FoldY(sheet map[int][]int, foldRow int) map[int][]int {
	if _, ok := sheet[foldRow]; ok {
		delete(sheet, foldRow)
	}

	maxRow := 0
	for row, _ := range sheet {
		if row > maxRow {
			maxRow = row
		}
	}

	for row := foldRow + 1; row <= maxRow; row++ {
		if _, ok := sheet[row]; !ok {
			continue
		}

		newRow := foldRow + foldRow - row
		if _, ok := sheet[newRow]; !ok {
			sheet[newRow] = make([]int, 0)
		}

		for _, column := range sheet[row] {
			if GetIndex(sheet[newRow], column) == -1 {
				sheet[newRow] = append(sheet[newRow], column)
			}
		}

		delete(sheet, row)
	}

	return sheet
}

func Fold(sheet map[int][]int, axis string, value int) map[int][]int {
	if axis == "x" {
		return FoldX(sheet, value)
	}
	if axis == "y" {
		return FoldY(sheet, value)
	}

	return nil
}

func FollowInstructions(sheet map[int][]int, instructions []FoldInstruction) (int, []string) {
	count := 0
	for index, instruction := range instructions {
		sheet = Fold(sheet, instruction.axis, instruction.value)
		if index == 0 {
			for _, columns := range sheet {
				count += len(columns)
			}
		}
	}

	rows := make([]int, 0)
	for row, _ := range sheet {
		rows = append(rows, row)
	}

	sort.Ints(rows)

	minColumn := 9999999
	maxColumn := 0

	for _, row := range rows {
		for _, column := range sheet[row] {
			if column < minColumn {
				minColumn = column
			}
			if column > maxColumn {
				maxColumn = column
			}
		}
	}

	result := make([]string, 0)
	for _, row := range rows {
		sort.Ints(sheet[row])
		curr := ""
		for index := minColumn; index <= maxColumn; index++ {
			if GetIndex(sheet[row], index) == -1 {
				curr += "."
			} else {
				curr += "#"
			}
		}
		result = append(result, curr)
	}

	return count, result
}

func PartB(data []string, result chan interface{}) {
	result <- "UPDATE THIS"
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

	sheet, instructions := ParseData(data)
	count, result := FollowInstructions(sheet, instructions)

	fmt.Println("Part A:", count)
	fmt.Println("Part B:")
	for _, line := range result {
		fmt.Println(line)
	}
}
