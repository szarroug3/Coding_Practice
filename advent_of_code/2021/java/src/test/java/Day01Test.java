import static org.junit.Assert.assertEquals;

import java.io.FileNotFoundException;
import java.io.IOException;
import org.junit.Test;

/**
 * Unit test for Day 1 of AOC 2021.
 */
public class Day01Test {

  /**
   * Make sure part A runs correctly.
   *
   * @throws IOException             if file can't be read
   * @throws FileNotFoundException   if file can't be found
   */
  @Test
  public void partOneTest() throws FileNotFoundException, IOException {
    int result = new Day01("resources/day01.txt").partOne();
    assertEquals(7, result);
  }

  /**
   * Make sure part B runs correctly.
   *
   * @throws IOException             if file can't be read
   * @throws FileNotFoundException   if file can't be found
   */
  @Test
  public void partTwoTest() throws FileNotFoundException, IOException {
    int result = new Day01("resources/day01.txt").partTwo();
    assertEquals(5, result);
  }
}