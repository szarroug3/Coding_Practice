import { readInput } from "./utils";

type WorkflowType = {
  workflow: string;
  fallback: boolean;
  value?: number;
  separator?: string;
  part?: string;
}

type RatingsType = Record<string, number>;
type QueueType = { values: Record<string, Record<string, number>>, name: string };

const { workflows, ratings } = readInput((data) => {
  let first = true;
  const workflows: Record<string, WorkflowType[]> = {};
  const ratings: RatingsType[] = [];

  for (let line of data.split('\n').map((line) => line.slice(0, -1))) {
    if (line === '') {
      first = false;
      continue;
    }

    if (first) {
      const [label, info] = line.split('{');
      workflows[label] = info.split(',').map((workflow) => {
        if (!workflow.includes(':')) {
          return { workflow, fallback: true }
        }

        const [rule, result] = workflow.split(':');
        const separator = workflow.includes('<') ? '<' : '>';
        const [part, value] = rule.split(separator);
        return { part, workflow: result, value: Number(value), separator, fallback: false };
      });
      continue;
    }

    ratings.push(line.slice(1).split(',').reduce((acc, info) => {
      const [label, value] = info.split('=');
      return {
        ...acc,
        [label]: Number(value)
      };
    }, {} as RatingsType));
  }

  return { workflows, ratings };
}) as { workflows: Record<string, WorkflowType[]>, ratings: RatingsType[] };

const partA = () => {
  let total = 0;
  for (let rating of ratings) {
    let curr = workflows['in'];
    let done = false;
    let index = 0;
    while (!done) {
      const { workflow, part, fallback, value, separator } = curr[index];
      if (fallback || separator === '<' && rating[part!] < value! || separator === '>' && rating[part!] > value!) {
        switch (workflow) {
          case 'A':
            done = true;
            total += Object.values(rating).reduce((acc, value) => acc + value, 0);
            break;
          case 'R':
            done = true;
            break;
          default:
            curr = workflows[workflow];
            index = 0;
            break;
        }
      } else {
        index++;
      }
    }
  }

  return total;
};

const copy = (original: Record<string, Record<string, number>>) => {
  return JSON.parse(JSON.stringify(original));
}

const partB = () => {
  let count = 0;
  const queue: QueueType[] = [{
    values: {
      x: { start: 1, end: 4000 },
      m: { start: 1, end: 4000 },
      a: { start: 1, end: 4000 },
      s: { start: 1, end: 4000 }
    },
    name: 'in'
  }];

  while (queue.length) {
    const { values, name } = queue.shift()!;
    for (let { part, value, separator, workflow, fallback } of workflows[name]) {
      const other = Object.entries(values).filter(([name]) => name !== part).reduce((acc, [, { end, start }]) => acc * (end - start + 1), 1)

      if (fallback) {
        switch (workflow) {
          case 'A':
            count += other;
            break;
          case 'R':
            break;
          default:
            queue.push({ values: copy(values), name: workflow });
            break;
        }
        break;
      }

      if (separator === '<') {
        if (values[part!].start >= value!) {
          continue;
        }

        if (values[part!].end >= value!) {
          switch (workflow) {
            case 'A':
              count += other * (value! - values[part!].start);
              break;
            case 'R':
              break;
            default:
              queue.push({ values: { ...copy(values), [part!]: { start: values[part!].start, end: value! - 1 } }, name: workflow })
              break;
          }
          values[part!].start = value!;
          continue;
        }

        let done = false;
        switch (workflow) {
          case 'A':
            count += other * (values[part!].end - values[part!].start + 1);
            break;
          case 'R':
            done = true;
            break;
          default:
            queue.push({ values: copy(values), name: workflow });
            break;
        }

        if (done) {
          break;
        }
        continue;
      }

      if (values[part!].end <= value!) {
        continue;
      }

      if (values[part!].start <= value!) {
        switch (workflow) {
          case 'A':
            count += other * (values[part!].end - value!);
            break;
          case 'R':
            break;
          default:
            queue.push({ values: { ...copy(values), [part!]: { start: value! + 1, end: values[part!].end } }, name: workflow })
            break;
        }
        values[part!].end = value!;
        continue;
      }

      let done = false;
      switch (workflow) {
        case 'A':
          count += other * (values[part!].end - values[part!].start + 1);
          break;
        case 'R':
          done = true;
          break;
        default:
          queue.push({ values: { ...values }, name: workflow });
          break;
      }

      if (done) {
        break;
      }
    }
  }

  return count;
};

console.log('Part A:', partA());
console.log('Part B:', partB());