// https://adventofcode.com/2020/day/21

package main

import (
	"fmt"
	"os"
	"sort"
	"strconv"
	"strings"
	"utils/utils"
)

func PartA(data []string, result chan interface{}) {
	scores := make([]int, len(data))
	locations := make([]int, 0)
	for _, line := range data {
		split := strings.Split(line, " ")
		starting, _ := strconv.Atoi(split[len(split)-1])
		locations = append(locations, starting)
	}

	player := 0
	score := 0
	count := 0
	roll := 1

	for score < 1000 {
		score = scores[player]
		location := locations[player]
		for i := 0; i < 3; i++ {
			location += roll
			if location > 10 {
				location %= 10
			}

			roll++
			if roll > 10 {
				roll %= 10
			}

			count++
		}
		score += location
		scores[player] = score
		locations[player] = location
		player = (player + 1) % len(data)
	}

	result <- scores[player] * count
}

func PlayWithDiracDice(player int, locations []int, scores []int, wins []int, paths int, possibilities map[int]int) {
	for total := 3; total <= 9; total++ {
		currPaths := paths * possibilities[total]
		currLocations := make([]int, 0)
		currLocations = append(currLocations, locations...)

		currScores := make([]int, 0)
		currScores = append(currScores, scores...)

		currLocations[player] += total
		if currLocations[player] > 10 {
			currLocations[player] %= 10
		}

		currScores[player] += currLocations[player]
		if currScores[player] >= 21 {
			wins[player] += currPaths
			continue
		}

		PlayWithDiracDice((player+1)%2, currLocations, currScores, wins, currPaths, possibilities)
	}
}

func PartB(data []string, result chan interface{}) {
	locations := make([]int, 0)
	wins := make([]int, len(data))
	scores := make([]int, len(data))
	possibilities := map[int]int{3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}

	for _, line := range data {
		split := strings.Split(line, " ")
		starting, _ := strconv.Atoi(split[len(split)-1])
		locations = append(locations, starting)
	}

	PlayWithDiracDice(0, locations, scores, wins, 1, possibilities)
	sort.Ints(wins)

	result <- wins[len(wins)-1]
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
