// https://adventofcode.com/2020/day/12

const { kill } = require('process');
const { readFile } = require('../utils/input');

function parse(line) {
  return [line[0], parseInt(line.substring(1))];
}

async function partA(data) {
  return new Promise((resolve) => {
    let directions = ['east', 'south', 'west', 'north'];
    let north = 0;
    let east = 0;
    let direction = 'east';
    data.forEach((element) => {
      if (element[0] == 'R') {
        let turns = element[1] / 90;
        direction = directions[(directions.indexOf(direction) + turns) % 4];
      } else if (element[0] == 'L') {
        let turns = element[1] / 90;
        direction = directions[(directions.indexOf(direction) + 4 - turns) % 4];
      } else if (
        element[0] == 'N' ||
        (direction == 'north' && element[0] == 'F')
      ) {
        north += element[1];
      } else if (
        element[0] == 'E' ||
        (direction == 'east' && element[0] == 'F')
      ) {
        east += element[1];
      } else if (
        element[0] == 'S' ||
        (direction == 'south' && element[0] == 'F')
      ) {
        north -= element[1];
      } else if (
        element[0] == 'W' ||
        (direction == 'west' && element[0] == 'F')
      ) {
        east -= element[1];
      }
    });

    resolve(Math.abs(north) + Math.abs(east));
  });
}

async function partB(data) {
  return new Promise((resolve) => {
    let north = 0;
    let east = 0;
    let waypointNorth = 1;
    let waypointEast = 10;
    data.forEach((element) => {
      if (element[0] == 'R') {
        for (let i = 0; i < element[1] / 90; i++) {
          let tmpEast = waypointEast;
          waypointEast = waypointNorth;
          waypointNorth = tmpEast * -1;
        }
      } else if (element[0] == 'L') {
        for (let i = 0; i < element[1] / 90; i++) {
          let tmpEast = waypointEast;
          waypointEast = waypointNorth * -1;
          waypointNorth = tmpEast;
        }
      } else if (element[0] == 'N') {
        waypointNorth += element[1];
      } else if (element[0] == 'E') {
        waypointEast += element[1];
      } else if (element[0] == 'S') {
        waypointNorth -= element[1];
      } else if (element[0] == 'W') {
        waypointEast -= element[1];
      } else if (element[0] == 'F') {
        north += waypointNorth * element[1];
        east += waypointEast * element[1];
      }
    });

    resolve(Math.abs(north) + Math.abs(east));
  });
}

async function main() {
  try {
    var data = readFile('\n', parse);
  } catch (error) {
    console.log(error.message);
    process.exit();
  }

  let answers = await Promise.all([partA(data), partB(data)])
    .then((answers) => {
      console.log(`Part A: ${answers[0]}`);
      console.log(`Part B: ${answers[1]}`);
    })
    .catch(console.log);
}

main();
