// https://adventofcode.com/2020/day/22

package main

import (
	"fmt"
	"math"
	"os"
	"sort"
	"strconv"
	"strings"
	"utils/utils"
)

type Instruction struct {
	on         bool
	xMin, xMax int
	yMin, yMax int
	zMin, zMax int
}

func (cube Instruction) volume() int {
	volume := math.Abs(float64(cube.xMax-cube.xMin) + 1.0)
	volume *= math.Abs(float64(cube.yMax-cube.yMin) + 1.0)
	volume *= math.Abs(float64(cube.zMax-cube.zMin) + 1.0)
	if cube.on {
		return int(volume)
	}
	return -int(volume)
}

func Parse(data []string) []Instruction {
	instructions := make([]Instruction, 0)

	for _, line := range data {
		split := strings.Split(line, " ")
		instruction := Instruction{on: split[0] == "on"}

		for _, curr := range strings.Split(split[1], ",") {
			pieces := strings.Split(curr, "=")

			values := make([]int, 0)
			for _, value := range strings.Split(pieces[1], "..") {
				currValue, _ := strconv.Atoi(value)
				values = append(values, currValue)
			}

			sort.Ints(values)
			min := values[0]
			max := values[len(values)-1]

			switch pieces[0] {
			case "x":
				instruction.xMin = min
				instruction.xMax = max
			case "y":
				instruction.yMin = min
				instruction.yMax = max

			case "z":
				instruction.zMin = min
				instruction.zMax = max
			}
		}

		instructions = append(instructions, instruction)
	}

	return instructions
}

func PartA(instructions []Instruction, result chan interface{}) {
	cubes := make(map[int]map[int]map[int]bool)
	count := 0

	for _, instruction := range instructions {
		if instruction.xMin > 50 || instruction.yMin > 50 || instruction.zMin > 50 {
			continue
		} else if instruction.xMax < -50 || instruction.yMax < -50 || instruction.zMax < -50 {
			continue
		}

		xMin := instruction.xMin
		if xMin < -50 {
			xMin = -50
		}

		xMax := instruction.xMax
		if xMax > 50 {
			xMax = 50
		}

		yMin := instruction.yMin
		if yMin < -50 {
			yMin = -50
		}

		yMax := instruction.yMax
		if yMax > 50 {
			yMax = 50
		}

		zMin := instruction.zMin
		if zMin < -50 {
			zMin = -50
		}

		zMax := instruction.zMax
		if zMax > 50 {
			zMax = 50
		}

		for i := xMin; i <= xMax; i++ {
			for j := yMin; j <= yMax; j++ {
				for k := zMin; k <= zMax; k++ {
					if _, ok := cubes[i]; !ok {
						cubes[i] = make(map[int]map[int]bool)
					}
					if _, ok := cubes[i][j]; !ok {
						cubes[i][j] = make(map[int]bool)
					}
					if _, ok := cubes[i][j][k]; !ok {
						cubes[i][j][k] = false
					}

					if !cubes[i][j][k] && instruction.on {
						count++
					} else if cubes[i][j][k] && !instruction.on {
						count--
					}
					cubes[i][j][k] = instruction.on
				}
			}
		}
	}

	result <- count
}

func Intersects(original Instruction, curr Instruction) bool {
	if original.xMax < curr.xMin || original.xMin > curr.xMax {
		return false
	}

	if original.yMax < curr.yMin || original.yMin > curr.yMax {
		return false
	}

	if original.zMax < curr.zMin || original.zMin > curr.zMax {
		return false
	}

	return true
}

func GetIntersection(original Instruction, curr Instruction) Instruction {
	xMin := original.xMin
	if curr.xMin > xMin {
		xMin = curr.xMin
	}

	xMax := original.xMax
	if curr.xMax < xMax {
		xMax = curr.xMax
	}

	yMin := original.yMin
	if curr.yMin > yMin {
		yMin = curr.yMin
	}

	yMax := original.yMax
	if curr.yMax < yMax {
		yMax = curr.yMax
	}

	zMin := original.zMin
	if curr.zMin > zMin {
		zMin = curr.zMin
	}

	zMax := original.zMax
	if curr.zMax < zMax {
		zMax = curr.zMax
	}

	on := curr.on
	if original.on == curr.on {
		on = !original.on
	}

	return Instruction{xMin: xMin, xMax: xMax, yMin: yMin, yMax: yMax, zMin: zMin, zMax: zMax, on: on}
}

func PartB(instructions []Instruction, result chan interface{}) {
	cubes := make([]Instruction, 0)
	count := 0

	for _, instruction := range instructions {
		for _, cube := range cubes {
			if Intersects(cube, instruction) {
				intersection := GetIntersection(cube, instruction)
				cubes = append(cubes, intersection)
				count += intersection.volume()
			}
		}

		if instruction.on {
			cubes = append(cubes, instruction)
			count += instruction.volume()
		}
	}

	result <- count
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

	instructions := Parse(data)

	a := make(chan interface{})
	b := make(chan interface{})

	go PartA(instructions, a)
	go PartB(instructions, b)

	fmt.Println("Part A:", <-a)
	fmt.Println("Part B:", <-b)
}
