import { readInput } from "./utils.js";

const data = readInput((data) => {
  const gameIdPattern = /Game (\d+):/g;
  const gameDataPattern = /(\d+) (red|green|blue)/g;

  return data.split('\n').reduce((games, game) => {
    const gameId = Number(gameIdPattern.exec(game)[1]);
    gameIdPattern.lastIndex = 0;

    const gameData = game.split(': ')[1].split('; ').reduce((colors, iteration) => {
      colors.push(Array.from(iteration.matchAll(gameDataPattern)).reduce((acc, match) => {
        return {
          ...acc,
          [match[2]]: Number(match[1])
        }
      }, {}));
      return colors;
    }, []);

    return {
      ...games,
      [gameId]: gameData
    };
  }, {});
});

const partA = () => {
  const allowed = {
    'red': 12,
    'green': 13,
    'blue': 14 
  }

  return Object.entries(data).reduce((total, [id, iterations]) => {
    return total + (iterations.some((iteration) => {
      return Object.keys(iteration).some((color) => {
        return iteration[color] > allowed[color];
      });
    }) ? 0 : Number(id));
  }, 0);
};

const partB = () => {
  return Object.values(data).reduce((total, game) => {
    const zeroes = {
      'red': 0,
      'green': 0,
      'blue': 0
    };

    const mins = game.reduce((acc, colors) => {
      Object.entries(colors).forEach(([color, value]) => {
        if (value > acc[color]) {
          acc[color] = value;
        }
      });
      return acc;
    }, zeroes);

    return total + (mins['red'] * mins['green'] * mins['blue']);
  }, 0);
}

console.log('Part A: ', partA());
console.log('Part B: ', partB());