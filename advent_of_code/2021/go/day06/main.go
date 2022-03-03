// https://adventofcode.com/2021/day/6

package main

import (
	"fmt"
	"os"
	"utils/utils"
)

func ProcessTimers(timers []int, resultA chan int, resultB chan int) {
	newFishPerDay := make([]int, 7)
	for _, timer := range timers {
		newFishPerDay[(timer+1)%7]++
	}
	newFishQueue := make([]int, 2)

	count := len(timers)
	for day := 1; day <= 256; day++ {
		newFishIndex := day % 7
		count += newFishPerDay[newFishIndex]
		amountToAddToQueue := newFishPerDay[newFishIndex]
		newFishPerDay[newFishIndex] += newFishQueue[0]
		newFishQueue = append(newFishQueue[1:], amountToAddToQueue)
		if day == 80 {
			resultA <- count
		}
	}

	resultB <- count
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Input filename required.")
		return
	}

	data, err := utils.ReadFileAsSlices(os.Args[1], ",")
	if err != nil {
		fmt.Println(err)
		return
	}

	timers := utils.ConvertToInts(data)

	a := make(chan int)
	b := make(chan int)

	go ProcessTimers(timers, a, b)

	fmt.Println("Part A:", <-a)
	fmt.Println("Part B:", <-b)
}
