// https://adventofcode.com/2020/day/23

package main

import (
	"fmt"
	"os"
	"utils/utils"
)

var hallwayIndex map[uint8]int = map[uint8]int{65: 2, 66: 4, 67: 6, 68: 7}
var roomIndex map[uint8]int = map[uint8]int{65: 0, 66: 1, 67: 2, 68: 3}

func Parse(data []string) []Room {
	rooms := make([]Room, 0)
	roomType := uint8('A')
	costs := map[uint8]int{65: 1, 66: 10, 67: 100, 68: 1000}

	for i := 3; i <= 9; i += 2 {
		amphipods := make([]*Amphipod, 0)
		needMoves := false

		for j := 1; j <= 2; j++ {
			if data[j][i] == roomType {
				amphipods = append(amphipods, &Amphipod{kind: data[j][i], energy: costs[data[j][i]], home: true})
			} else {
				amphipods = append(amphipods, &Amphipod{kind: data[j][i], energy: costs[data[j][i]], home: false})
				needMoves = true
			}
		}

		if needMoves {
			rooms = append(rooms, Room{kind: roomType, amphipods: amphipods})
		}

		roomType++
	}

	return rooms
}

type Amphipod struct {
	kind        uint8
	home        bool
	energy      int
	// destination int
}

type Room struct {
	kind      uint8
	amphipods []*Amphipod
}

func Dijkstra() {

}

func MoveOutOfHallway(hallway []*Amphipod, rooms []Room, energy int) ([]*Amphipod, []Room, int) {
	for {
		movedOutOfHallway := false
		for i, amphipod := range hallway {
			if amphipod == nil {
				continue
			}

			var moved bool
			moved, hallway, rooms, energy = CanMoveToRoom(i, hallway, rooms, energy)
			if moved {
				movedOutOfHallway = true
				continue
			}
		}

		if !movedOutOfHallway {
			break
		}
	}

	return hallway, rooms, energy
}

func CanMoveToRoom(index int, hallway []*Amphipod, rooms []Room, energy int) (bool, []*Amphipod, []Room, int) {
	amphipod := hallway[index]
	destination := hallwayIndex[amphipod.kind]
	room := rooms[roomIndex[amphipod.kind]]

	left := index
	right := destination
	if index > destination {
		left = destination
		right = index
	}

	for i := left + 1; i <= right; i++ {
		if hallway[index] != nil {
			return false, hallway, rooms, energy
		}
		energy += amphipod.energy
	}

	for i := len(room.amphipods) - 1; i >= 0; i-- {
		if room.amphipods[i] != nil {
			if !room.amphipods[i].home {
				return false, hallway, rooms, energy
			}
			continue
		}

		room.amphipods[i] = amphipod
		amphipod.home = true
		hallway[index] = nil
		energy += (i + 1) * amphipod.energy
		return true, hallway, rooms, energy
	}

	return false, hallway, rooms, energy
}

// func SwapTopTwo(rooms []Room, energy int) ([]Room, int) {

// }

func PartA(rooms []Room, result chan interface{}) {
	energy := 0
	hallway := make([]*Amphipod, 11)

	for {
		changed := false
		var newEnergy int
		hallway, rooms, newEnergy = MoveOutOfHallway(hallway, rooms, energy)
		if newEnergy != energy {
			changed = true
			energy = newEnergy
		}

		if !changed {
			break
		}
	}

	for _, amphipod := range hallway {
		if amphipod != nil {
			fmt.Println("Something's wrong")
			fmt.Println(hallway)
			fmt.Println(rooms)
			break
		}
	}
	result <- energy
}

func PartB(rooms []Room, result chan interface{}) {
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

	rooms := Parse(data)

	a := make(chan interface{})
	b := make(chan interface{})

	go PartA(rooms, a)
	go PartB(rooms, b)

	fmt.Println("Part A:", <-a)
	fmt.Println("Part B:", <-b)
}
