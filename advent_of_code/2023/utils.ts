import { readFileSync } from 'fs';
import { argv } from 'process';
import path from 'path';

const readInput = <T>(fn?: (data: string) => T): string | T => {
  const day = argv[1].split('/').reverse()[0].split('.')[0];
  const defaultFilename = path.join('inputs', `${day}input.txt`);
  const filename = argv[2] ? argv[2] : defaultFilename;
  const data = readFileSync(filename, { encoding: 'utf8', flag: 'r' }).trim();

  if (fn) {
    return fn(data);
  }

  return data;
}

export { readInput };
