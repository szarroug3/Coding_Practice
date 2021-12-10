import static org.junit.Assert.assertEquals;

import java.io.FileNotFoundException;
import java.io.IOException;
import org.junit.Test;

/**
 * Unit test for simple App.
 */
public class Day01Test {

  /**
   * Make sure part A runs correctly.
   *
   * @throws IOException             if file can't be read
   * @throws FileNotFoundException   if file can't be found
   */
  @Test
  public void partATest() throws FileNotFoundException, IOException {
    int result = new Day01("resources/day01.txt").partA();
    assertEquals(7, result);
  }

  /**
   * Make sure part B runs correctly.
   *
   * @throws IOException             if file can't be read
   * @throws FileNotFoundException   if file can't be found
   */
  @Test
  public void partBTest() throws FileNotFoundException, IOException {
    int result = new Day01("resources/day01.txt").partB();
    assertEquals(5, result);
  }
}