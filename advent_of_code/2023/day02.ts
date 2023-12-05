import { readInput } from './utils';

const data = readInput((data) => {
  const gameIdPattern = /Game (\d+):/g;
  const gameDataPattern = /(\d+) (red|green|blue)/g;

  return data.split('\n').reduce((games, game) => {
    const gameId = Number(gameIdPattern.exec(game)![1]);
    gameIdPattern.lastIndex = 0;

    const gameData = game.split(': ')[1].split('; ').reduce((colors, iteration) => {
      const processed = Array.from(iteration.matchAll(gameDataPattern)).reduce((acc, match) => {
        return {
          ...acc,
          [match[2]]: Number(match[1])
        }
      }, {});

      colors.push(processed);
      return colors;
    }, [] as Array<Record<string, number>>);

    return {
      ...games,
      [gameId]: gameData
    };
  }, {});
}) as Record<string, Record<string, number>[]>;

const partA = () => {
  const allowed: Record<string, number> = {
    'red': 12,
    'green': 13,
    'blue': 14 
  }

  return Object.entries(data).reduce((total, [id, iterations]) => {
    return total + (iterations.some((iteration: Record<string, number>) => {
      return Object.keys(iteration).some((color: string) => {
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