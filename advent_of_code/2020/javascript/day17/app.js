// https://adventofcode.com/2020/day/17

const { readFile } = require('../utils/input');

function parse(data) {
  let cubes = {};
  for (let i = 0; i < data.length; i++) {
    if (!(i in cubes)) {
      cubes[i] = {};
    }
    for (let j = 0; j < data[i].length; j++) {
      cubes[i][j] = data[i][j];
    }
  }
  return cubes;
}

async function partA(data) {
  return new Promise((resolve) => {
    data = { 0: JSON.parse(JSON.stringify(data)) };
    for (let i = 0; i < 6; i++) {
      data = cycleA(data);
    }

    resolve(
      Object.values(data).reduce((arrayCount, array) => {
        return (
          arrayCount +
          Object.values(array).reduce((lineCount, line) => {
            return (
              lineCount +
              Object.values(line).reduce((cubeCount, cube) => {
                return cube === '#' ? cubeCount + 1 : cubeCount;
              }, 0)
            );
          }, 0)
        );
      }, 0)
    );
  });
}

function cycleA(data) {
  /*
    If a cube is active and exactly 2 or 3 of its neighbors are also active, the cube remains active. Otherwise, the cube becomes inactive.
    If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes active. Otherwise, the cube remains inactive.
  */
  data = padA(data);
  let newData = JSON.parse(JSON.stringify(data));

  for (const [z, array] of Object.entries(data)) {
    for (const [y, line] of Object.entries(array)) {
      for (const [x, cube] of Object.entries(line)) {
        let activeNeighbors = getActiveNeighborsA(
          data,
          parseInt(z),
          parseInt(y),
          parseInt(x)
        );

        if (cube === '#') {
          if (activeNeighbors === 2 || activeNeighbors === 3) {
            newData[z][y][x] = '#';
          } else {
            newData[z][y][x] = '.';
          }
        } else {
          if (activeNeighbors === 3) {
            newData[z][y][x] = '#';
          } else {
            newData[z][y][x] = '.';
          }
        }
      }
    }
  }
  return newData;
}

function padA(data) {
  let zKeys = Object.keys(data);
  zKeys.sort((a, b) => parseInt(a) - parseInt(b));
  let minZ = parseInt(zKeys[0]);
  let maxZ = parseInt(zKeys[zKeys.length - 1]);

  let yKeys = Object.keys(data[0]);
  yKeys.sort((a, b) => parseInt(a) - parseInt(b));
  let minY = parseInt(yKeys[0]);
  let maxY = parseInt(yKeys[yKeys.length - 1]);

  let xKeys = Object.keys(data[0][0]);
  xKeys.sort((a, b) => parseInt(a) - parseInt(b));
  let minX = parseInt(xKeys[0]);
  let maxX = parseInt(xKeys[xKeys.length - 1]);

  for (let i = minZ - 1; i <= maxZ + 1; i++) {
    if (!(i in data)) {
      data[i] = {};
    }

    for (let j = minY - 1; j <= maxY + 1; j++) {
      if (!(j in data[i])) {
        data[i][j] = {};
      }

      for (let k = minX - 1; k <= maxX + 1; k++) {
        if (!(k in data[i][j])) {
          data[i][j][k] = '.';
        }
      }
    }
  }

  return data;
}

function getActiveNeighborsA(data, z, y, x) {
  let count = data[z][y][x] === '#' ? -1 : 0;
  for (let i = z - 1; i < z + 2; i++) {
    if (!(i in data)) {
      continue;
    }
    for (let j = y - 1; j < y + 2; j++) {
      if (!(j in data[i])) {
        continue;
      }
      for (let k = x - 1; k < x + 2; k++) {
        if (!(k in data[i][j])) {
          continue;
        }
        if (data[i][j][k] === '#') {
          count++;
        }
      }
    }
  }
  return count;
}

async function partB(data) {
  return new Promise((resolve) => {
    data = { 0: { 0: JSON.parse(JSON.stringify(data)) } };
    for (let i = 0; i < 6; i++) {
      data = cycleB(data);
    }

    resolve(
      Object.values(data).reduce((arrayCount, array) => {
        return (
          arrayCount +
          Object.values(array).reduce((lineCount, line) => {
            return (
              lineCount +
              Object.values(line).reduce((cubeCount, cube) => {
                return (
                  cubeCount +
                  Object.values(cube).reduce((valCount, val) => {
                    return val === '#' ? valCount + 1 : valCount;
                  }, 0)
                );
              }, 0)
            );
          }, 0)
        );
      }, 0)
    );
  });
}

function cycleB(data) {
  /*
    If a cube is active and exactly 2 or 3 of its neighbors are also active, the cube remains active. Otherwise, the cube becomes inactive.
    If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes active. Otherwise, the cube remains inactive.
  */
  data = padB(data);
  let newData = JSON.parse(JSON.stringify(data));

  for (const [z, array] of Object.entries(data)) {
    for (const [y, line] of Object.entries(array)) {
      for (const [x, cube] of Object.entries(line)) {
        for (const [w, val] of Object.entries(cube)) {
          let activeNeighbors = getActiveNeighborsB(
            data,
            parseInt(z),
            parseInt(y),
            parseInt(x),
            parseInt(w)
          );

          if (val === '#') {
            if (activeNeighbors === 2 || activeNeighbors === 3) {
              newData[z][y][x][w] = '#';
            } else {
              newData[z][y][x][w] = '.';
            }
          } else {
            if (activeNeighbors === 3) {
              newData[z][y][x][w] = '#';
            } else {
              newData[z][y][x][w] = '.';
            }
          }
        }
      }
    }
  }

  return newData;
}

function padB(data) {
  let zKeys = Object.keys(data);
  zKeys.sort((a, b) => parseInt(a) - parseInt(b));
  let minZ = parseInt(zKeys[0]);
  let maxZ = parseInt(zKeys[zKeys.length - 1]);

  let yKeys = Object.keys(data[0]);
  yKeys.sort((a, b) => parseInt(a) - parseInt(b));
  let minY = parseInt(yKeys[0]);
  let maxY = parseInt(yKeys[yKeys.length - 1]);

  let xKeys = Object.keys(data[0][0]);
  xKeys.sort((a, b) => parseInt(a) - parseInt(b));
  let minX = parseInt(xKeys[0]);
  let maxX = parseInt(xKeys[xKeys.length - 1]);

  let wKeys = Object.keys(data[0][0][0]);
  wKeys.sort((a, b) => parseInt(a) - parseInt(b));
  let minW = parseInt(wKeys[0]);
  let maxW = parseInt(wKeys[wKeys.length - 1]);

  for (let i = minZ - 1; i <= maxZ + 1; i++) {
    if (!(i in data)) {
      data[i] = {};
    }

    for (let j = minY - 1; j <= maxY + 1; j++) {
      if (!(j in data[i])) {
        data[i][j] = {};
      }

      for (let k = minX - 1; k <= maxX + 1; k++) {
        if (!(k in data[i][j])) {
          data[i][j][k] = {};
        }

        for (let l = minW - 1; l <= maxW + 1; l++) {
          if (!(l in data[i][j][k])) {
            data[i][j][k][l] = '.';
          }
        }
      }
    }
  }

  return data;
}

function getActiveNeighborsB(data, z, y, x, w) {
  let count = data[z][y][x][w] === '#' ? -1 : 0;
  for (let i = z - 1; i < z + 2; i++) {
    if (!(i in data)) {
      continue;
    }
    for (let j = y - 1; j < y + 2; j++) {
      if (!(j in data[i])) {
        continue;
      }
      for (let k = x - 1; k < x + 2; k++) {
        if (!(k in data[i][j])) {
          continue;
        }

        for (let l = w - 1; l < w + 2; l++) {
          if (!(l in data[i][j][k])) {
            continue;
          }
          if (data[i][j][k][l] === '#') {
            count++;
          }
        }
      }
    }
  }
  return count;
}

async function main() {
  try {
    var data = parse(readFile('\n', null, ''));
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
