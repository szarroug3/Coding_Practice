import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.ArrayList;

/**
 * Runs AOC day 1 problem.
 * https://adventofcode.com/2021/day/1
 */
public class Day01 {

  private ArrayList<Integer> data;

  /**
   * Initialize data for problem.
   *
   * @throws FileNotFoundException    if input file doesn't exist
   * @throws IOException              if reader fails to read file
   */
  public Day01(String filename) throws FileNotFoundException, IOException {
    ArrayList<String> data = Utils.readInputFile(filename);

    this.data = new ArrayList<>();
    for (int i = 0; i < data.size(); i++) {
      this.data.add(Integer.parseInt(data.get(i)));
    }
  }

  /**
   * Get the number of times the list increases from
   * one value to the next.
   *
   * @return    the number of times value in array increase
   */
  public int partOne() {
    int count = 0;

    for (int i = 1; i < this.data.size(); i++) {
      if (this.data.get(i) > this.data.get(i - 1)) {
        count++;
      }
    }

    return count;
  }

  /**
   * Get the number of times the list increases from
   * one value to the next using a sliding window.
   *
   * @return    the number of times value in array increase
   */
  public int partTwo() {
    int count = 0;
    int currWindow = this.data.get(0) + this.data.get(1) + this.data.get(2);

    for (int i = 3; i < this.data.size(); i++) {
      int newWindow = currWindow - this.data.get(i - 3) + this.data.get(i);
      if (newWindow > currWindow) {
        count++;
      }
      currWindow = newWindow;
    }

    return count;
  }
}