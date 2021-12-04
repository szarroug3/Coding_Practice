// https://adventofcode.com/2020/day/4

package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
	"utils/utils"
)

func ParseInput(data []string) ([]int, [][][]int) {
	numbers := utils.ConvertToInts(strings.Split(data[0], ","))
	boards := make([][][]int, 0)
	currBoard := make([][]int, 0)

	for _, line := range data[2:] {
		if line == "" {
			continue
		}

		currLine := make([]int, 0)
		for _, number := range strings.Split(line, " ") {
			if number == "" {
				continue
			}
			numberAsInt, _ := strconv.Atoi(number)
			currLine = append(currLine, numberAsInt)
		}

		currBoard = append(currBoard, currLine)

		if len(currBoard) == 5 {
			boards = append(boards, currBoard)
			currBoard = make([][]int, 0)
		}

	}
	return numbers, boards
}

func MarkBoards(boards [][][]int, marked [][][]bool, number int) [][][]bool {
	for boardIndex, board := range boards {
		for lineIndex, line := range board {
			for numberIndex, value := range line {
				if value == number {
					marked[boardIndex][lineIndex][numberIndex] = true
				}
			}
		}
	}

	return marked
}

func CheckBoard(marked [][]bool) bool {
	for i := 0; i < 5; i++ {
		goodRow := true
		goodColumn := true
		for j := 0; j < 5; j++ {
			if !marked[i][j] {
				goodRow = false
			}
			if !marked[j][i] {
				goodColumn = false
			}

			if !goodRow && !goodColumn {
				break
			}
		}

		if goodRow || goodColumn {
			return true
		}
	}

	return false
}

func GetBoardScore(board [][]int, marked [][]bool) int {
	result := 0
	for lineIndex, line := range marked {
		for markedIndex, value := range line {
			if !value {
				result += board[lineIndex][markedIndex]
			}
		}
	}

	return result
}

func MakeMarkedBoard(length int) [][][]bool {
	marked := make([][][]bool, 0)
	for i := 0; i < length; i++ {
		marked = append(marked, [][]bool{
			{false, false, false, false, false},
			{false, false, false, false, false},
			{false, false, false, false, false},
			{false, false, false, false, false},
			{false, false, false, false, false},
		})
	}

	return marked
}
func PartA(numbers []int, boards [][][]int, result chan interface{}) {
	marked := MakeMarkedBoard(len(boards))
	for _, number := range numbers {
		marked = MarkBoards(boards, marked, number)
		for index, board := range boards {
			if CheckBoard(marked[index]) {
				result <- GetBoardScore(board, marked[index]) * number
				return
			}
		}
	}

	result <- "No winner"
}

func PartB(numbers []int, boards [][][]int, result chan interface{}) {
	marked := MakeMarkedBoard(len(boards))
	winningBoards := make([]bool, len(boards))
	winningCount := 0

	for _, number := range numbers {

		marked = MarkBoards(boards, marked, number)
		for index, _ := range boards {
			if winningBoards[index] {
				continue
			}

			if CheckBoard(marked[index]) {
				winningBoards[index] = true
				winningCount++
				if len(boards) == winningCount {
					result <- GetBoardScore(boards[index], marked[index]) * number
					return
				}
			}
		}
	}

	result <- "No winner"
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

	numbers, boards := ParseInput(data)

	a := make(chan interface{})
	b := make(chan interface{})

	go PartA(numbers, boards, a)
	go PartB(numbers, boards, b)

	fmt.Println("Part A:", <-a)
	fmt.Println("Part B:", <-b)
}
