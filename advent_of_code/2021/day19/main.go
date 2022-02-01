// https://adventofcode.com/2020/day/19

package main

import (
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"
	"utils/utils"
)

type Adjustment struct {
	order   []int
	reverse []int
	move    []int
}

func Parse(data []string) [][][]int {
	results := make([][][]int, 0)
	curr := make([][]int, 0)

	for _, line := range data {
		if line == "" {
			continue
		}

		if line[:3] == "---" {
			if len(curr) != 0 {
				results = append(results, curr)
				curr = make([][]int, 0)
			}
			continue
		}

		split := strings.Split(line, ",")
		values := make([]int, 0)

		for _, value := range split {
			converted, _ := strconv.Atoi(value)
			values = append(values, converted)
		}

		curr = append(curr, values)
	}

	if len(curr) != 0 {
		results = append(results, curr)
		curr = make([][]int, 0)
	}
	return results
}

func GetPossibilities() []Adjustment {
	return []Adjustment{
		Adjustment{order: []int{0, 1, 2}, reverse: []int{1, 1, 1}, move: []int{0, 0, 0}},
		Adjustment{order: []int{0, 2, 1}, reverse: []int{1, 1, -1}, move: []int{0, 0, 0}},
		Adjustment{order: []int{0, 1, 2}, reverse: []int{1, -1, -1}, move: []int{0, 0, 0}},
		Adjustment{order: []int{0, 2, 1}, reverse: []int{1, -1, 1}, move: []int{0, 0, 0}},

		Adjustment{order: []int{1, 2, 0}, reverse: []int{1, 1, 1}, move: []int{0, 0, 0}},
		Adjustment{order: []int{1, 0, 2}, reverse: []int{1, 1, -1}, move: []int{0, 0, 0}},
		Adjustment{order: []int{1, 2, 0}, reverse: []int{1, -1, -1}, move: []int{0, 0, 0}},
		Adjustment{order: []int{1, 0, 2}, reverse: []int{1, -1, 1}, move: []int{0, 0, 0}},

		Adjustment{order: []int{2, 0, 1}, reverse: []int{1, 1, 1}, move: []int{0, 0, 0}},
		Adjustment{order: []int{2, 1, 0}, reverse: []int{1, 1, -1}, move: []int{0, 0, 0}},
		Adjustment{order: []int{2, 0, 1}, reverse: []int{1, -1, -1}, move: []int{0, 0, 0}},
		Adjustment{order: []int{2, 1, 0}, reverse: []int{1, -1, 1}, move: []int{0, 0, 0}},

		Adjustment{order: []int{0, 2, 1}, reverse: []int{-1, 1, 1}, move: []int{0, 0, 0}},
		Adjustment{order: []int{0, 1, 2}, reverse: []int{-1, 1, -1}, move: []int{0, 0, 0}},
		Adjustment{order: []int{0, 2, 1}, reverse: []int{-1, -1, -1}, move: []int{0, 0, 0}},
		Adjustment{order: []int{0, 1, 2}, reverse: []int{-1, -1, 1}, move: []int{0, 0, 0}},

		Adjustment{order: []int{1, 0, 2}, reverse: []int{-1, 1, 1}, move: []int{0, 0, 0}},
		Adjustment{order: []int{1, 2, 0}, reverse: []int{-1, 1, -1}, move: []int{0, 0, 0}},
		Adjustment{order: []int{1, 0, 2}, reverse: []int{-1, -1, -1}, move: []int{0, 0, 0}},
		Adjustment{order: []int{1, 2, 0}, reverse: []int{-1, -1, 1}, move: []int{0, 0, 0}},

		Adjustment{order: []int{2, 1, 0}, reverse: []int{-1, 1, 1}, move: []int{0, 0, 0}},
		Adjustment{order: []int{2, 0, 1}, reverse: []int{-1, 1, -1}, move: []int{0, 0, 0}},
		Adjustment{order: []int{2, 1, 0}, reverse: []int{-1, -1, -1}, move: []int{0, 0, 0}},
		Adjustment{order: []int{2, 0, 1}, reverse: []int{-1, -1, 1}, move: []int{0, 0, 0}},
	}
}

func ScannersMatch(original [][]int, curr [][]int, possibilities []Adjustment) (bool, Adjustment) {
	for _, adjustment := range possibilities {
		for i, currBeacon := range curr {
			adjusted := ApplyAdjustment(currBeacon, adjustment)
			for j, originalBeacon := range original {
				offsetA := originalBeacon[0] - adjusted[0]
				offsetB := originalBeacon[1] - adjusted[1]
				offsetC := originalBeacon[2] - adjusted[2]

				if math.Abs(float64(offsetA)) > 2000 || math.Abs(float64(offsetB)) > 2000 || math.Abs(float64(offsetC)) > 2000 {
					continue
				}

				offsets := []int{offsetA, offsetB, offsetC}
				currAdjustment := Adjustment{order: adjustment.order, reverse: adjustment.reverse, move: offsets}

				matches := 1
				for k, beaconA := range curr {
					if i == k {
						continue
					}

					beacon := ApplyAdjustment(beaconA, currAdjustment)
					for l, beaconB := range original {
						if l == j {
							continue
						}

						if beacon[0] != beaconB[0] || beacon[1] != beaconB[1] || beacon[2] != beaconB[2] {
							continue
						}

						matches++
						if matches == 12 {
							return true, currAdjustment
						}
						break
					}

					if len(original)-k-1 < 12-matches {
						break
					}
				}
			}
		}
	}

	return false, Adjustment{}
}

func GetAdjustment(original Adjustment, curr Adjustment) Adjustment {
	newOrder := make([]int, 0)
	for _, index := range curr.order {
		newOrder = append(newOrder, original.order[index])
	}

	newReverse := make([]int, 0)
	for index, value := range curr.reverse {
		newReverse = append(newReverse, original.reverse[index]*value)
	}

	newMove := make([]int, 0)
	for index, value := range curr.move {
		newMove = append(newMove, original.move[index]+value)
	}

	return Adjustment{order: newOrder, reverse: newReverse, move: newMove}
}

func ApplyAdjustments(beacon []int, adjustments []Adjustment) []int {
	for _, adjustment := range adjustments {
		beacon = ApplyAdjustment(beacon, adjustment)
	}

	return beacon
}

func ApplyAdjustment(beacon []int, adjustment Adjustment) []int {
	result := make([]int, 0)

	for i, index := range adjustment.order {
		result = append(result, beacon[index]*adjustment.reverse[i]+adjustment.move[i])
	}

	return result
}

func AddBeacons(beacons [][]int, scanner [][]int, adjustments []Adjustment) [][]int {
	for _, beacon := range scanner {
		adjusted := ApplyAdjustments(beacon, adjustments)

		found := false
		for _, existing := range beacons {
			matching := true
			for i, value := range existing {
				if adjusted[i] != value {
					matching = false
					break
				}
			}

			if matching {
				found = true
				break
			}
		}

		if !found {
			beacons = append(beacons, adjusted)
		}
	}

	return beacons
}

func GetFurthest(adjustments map[int][]Adjustment) int {
	longest := 0
	point := []int{0, 0, 0}
	for i := 0; i < len(adjustments)-1; i++ {
		beaconA := ApplyAdjustments(point, adjustments[i])
		for j := i + 1; j < len(adjustments); j++ {
			beaconB := ApplyAdjustments(point, adjustments[j])
			distance := int(math.Abs(float64(beaconA[0] - beaconB[0])))
			distance += int(math.Abs(float64(beaconA[1] - beaconB[1])))
			distance += int(math.Abs(float64(beaconA[2] - beaconB[2])))
			if distance > longest {
				longest = distance
			}
		}
	}

	return longest
}

func PartA(data [][][]int) (int, int) {
	complete := make(map[int][][]int)
	complete[0] = data[0]

	incomplete := make(map[int][][]int)
	for i, scanner := range data[1:] {
		incomplete[i+1] = scanner
	}

	adjustments := make(map[int][]Adjustment)
	order := make([]int, 0)
	reverse := make([]int, 0)
	move := make([]int, 0)

	for i := 0; i < len(data[0][0]); i++ {
		order = append(order, i)
		reverse = append(reverse, 1)
		move = append(move, 0)
	}
	adjustments[0] = []Adjustment{Adjustment{order: order, reverse: reverse, move: move}}
	possibleAdjustments := GetPossibilities()

	beacons := make([][]int, 0)
	for _, beacon := range data[0] {
		beacons = append(beacons, beacon)
	}

	lastCompleted := []int{0}
	for len(incomplete) > 0 {
		currCompleted := make([]int, 0)
		if len(lastCompleted) == 0 {
			panic("lastCompleted empty")
		}
		for _, completedScannerId := range lastCompleted {
			for incompleteScannerId, scanner := range incomplete {
				matches, adjustment := ScannersMatch(data[completedScannerId], scanner, possibleAdjustments)
				if matches {
					currCompleted = append(currCompleted, incompleteScannerId)
					currAdjustments := make([]Adjustment, 0)
					currAdjustments = append(currAdjustments, adjustment)
					currAdjustments = append(currAdjustments, adjustments[completedScannerId]...)
					adjustments[incompleteScannerId] = currAdjustments
					beacons = AddBeacons(beacons, scanner, adjustments[incompleteScannerId])
				}
			}

			for _, scannerId := range currCompleted {
				delete(incomplete, scannerId)
			}

			lastCompleted = currCompleted
		}
	}

	return len(beacons), GetFurthest(adjustments)
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

	parsed := Parse(data)

	beacons, furthest := PartA(parsed)

	fmt.Println("Part A:", beacons)
	fmt.Println("Part B:", furthest)
}
