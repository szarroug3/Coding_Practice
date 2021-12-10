import java.io.FileNotFoundException;
import java.io.IOException;

/**
 * Run code for Advent of Code.
 */
public class Aoc {

  /**
   * Read input from Advent of Code problems and report results.
   *
   * @param args  input to main
   */
  public static void main(String[] args) {
    try {
      Day01 day = new Day01("day01.txt");
      System.out.printf("Part A: %s\n", day.partA());
      System.out.printf("Part B: %s", day.partB());
    } catch (FileNotFoundException e) {
      System.out.println(e.getMessage());
    } catch (IOException e) {
      System.out.println(e);
    }
  }
}
