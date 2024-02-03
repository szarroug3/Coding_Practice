import { readInput } from "./utils";

const { types, instructions } = readInput((data) => {
  const types: Record<string, string> = {};
  const instructions: Record<string, string[]> = {};

  for (let line of data.split('\n')) {
    const [label, outputs] = line.split(' -> ');
    const type = label === 'broadcaster' ? 'b' : label[0];
    const name = label === 'broadcaster' ? label : label.slice(1);
    const split = outputs.split(', ');
    types[name] = type;

    for (let output of split) {
      if (!(name in instructions)) {
        instructions[name] = [];
      }
      instructions[name].push(output)
    }
  }

  return { types, instructions };
}) as { types: Record<string, string>, instructions: Record<string, string[]> };


const flipFlop = (input: string, output: string, values: Record<string, boolean>, queue: string[]) => {
  if (!(input in values)) {
    values[input] = false;
  }

  if (!values[input]) {
    values[output] = !values[output];
    queue.push(output);
  }

  return { values, queue };
};

const conjunction = (input: string, output: string, values: Record<string, boolean>, connections: Record<string, Record<string, boolean>>, queue: string[]) => {
  if (!(input in values)) {
    values[input] = false;
  }

  connections[output][input] = values[input];
  const pulse = Object.values(connections[output]).some((value) => !value);
  values[output] = pulse;
  queue.push(output);
  return { values, connections, queue };
};

const getConnections = () => {
  return Object.entries(instructions).reduce((acc, [input, outputs]) => {
    for (let output of outputs) {
      if (types[output] !== '%') {
        if (!(output in acc)) {
          acc[output] = {};
        }
        acc[output][input] = false;
      }
    }
    return acc;
  }, {} as Record<string, Record<string, boolean>>);
}

const partA = () => {
  let connections = getConnections();
  let values: Record<string, boolean> = {};
  let low = 0;
  let high = 0;

  for (let i = 0; i < 1000; i++) {
    let queue: string[] = ['broadcaster'];
    values.broadcaster = false;
    low++;

    while (queue.length) {
      const input = queue.shift()!;
      const outputs = instructions[input];
      if (!outputs) {
        continue;
      }

      for (let output of outputs) {
        if (values[input]) {
          high++;
        } else {
          low++;
        }

        if (types[output] === '%') {
          ({ values, queue } = flipFlop(input, output, values, queue));
        } else {
          ({ values, connections, queue } = conjunction(input, output, values, connections, queue));
        }
      }
    }
  }

  return low * high;
};

const partB = () => {
  let connections = getConnections();
  if (!('rx' in connections)) {
    return 'no rx';
  }

  let lcm = 1;
  const rxInput = Object.keys(connections.rx)[0];
  const ends = Object.keys(connections[rxInput]);

  for (let start of instructions.broadcaster) {
    let values: Record<string, boolean> = {};
    let cycle = 0;
    let done = false;

    while (!done) {
      cycle++;
      let queue: string[] = [];

      if (types[start] === '%') {
        ({ values, queue } = flipFlop('broadcaster', start, values, queue));
      } else {
        ({ values, connections, queue } = conjunction('broadcaster', start, values, connections, queue));
      }

      while (queue.length) {
        const input = queue.shift()!;
        const outputs = instructions[input];

        if (!outputs) {
          continue;
        }

        for (let output of outputs) {
          if (types[output] === '%') {
            ({ values, queue } = flipFlop(input, output, values, queue));
          } else {
            ({ values, queue } = conjunction(input, output, values, connections, queue));
          }

          if (ends.includes(output) && values[output]) {
            done = true;
            lcm *= cycle;
            break;
          }
        }

        if (done) {
          break;
        }
      }
    }

  };

  return lcm;
};

console.log('Part A:', partA());
console.log('Part B:', partB());
