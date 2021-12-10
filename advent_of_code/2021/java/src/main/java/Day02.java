import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.ArrayList;

/**
 * Runs AOC day 2 problem.
 * https://adventofcode.com/2021/day/2
 */
public class Day02 {

  private ArrayList<String> instruction;
  private ArrayList<Integer> unit;

  /**
   * Initialize data for problem.
   *
   * @throws FileNotFoundException    if input file doesn't exist
   * @throws IOException              if reader fails to read file
   */
  public Day02(String filename) throws FileNotFoundException, IOException {
    ArrayList<String> data = Utils.readInputFile(filename);

    this.instruction = new ArrayList<>();
    this.unit = new ArrayList<>();

    for (int i = 0; i < data.size(); i++) {
      String[] split = data.get(i).split(" ");
      this.instruction.add(split[0]);
      this.unit.add(Integer.parseInt(split[1]));
    }
  }

  /**
   * Find position of submarine after calculating all
   * movements and multiply results.
   *
   * @return    result of horizontal position multiplied by depth
   */
  public int partOne() {
    int horizontal = 0;
    int depth = 0;

    for (int i = 0; i < this.instruction.size(); i++) {
      String currInstruction = this.instruction.get(i);
      Integer currUnit = this.unit.get(i);

      if (currInstruction.equals("forward")) {
        horizontal += currUnit;
      } else if (currInstruction.equals("down")) {
        depth += currUnit;
      } else {
        depth -= currUnit;
      }
    }

    return horizontal * depth;
  }

  /**
   * Find position of submarine after calculating all
   * movements accounting for aim and multiply results.
   *
   * @return    result of horizontal position multiplied by depth
   */
  public int partTwo() {
    int horizontal = 0;
    int depth = 0;
    int aim = 0;

    for (int i = 0; i < this.instruction.size(); i++) {
      String currInstruction = this.instruction.get(i);
      Integer currUnit = this.unit.get(i);

      if (currInstruction.equals("forward")) {
        horizontal += currUnit;
        depth += aim * currUnit;
      } else if (currInstruction.equals("down")) {
        aim += currUnit;
      } else {
        aim -= currUnit;
      }
    }

    return horizontal * depth;
  }
}