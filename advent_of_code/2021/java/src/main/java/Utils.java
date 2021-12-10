


import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;

/**
 * Utility class used between all the puzzles.
 */
public class Utils {

  /**
   * Reads input file and returns the data in it.
   *
   * @param   filename                the name of the file to read
   * @return                          the data in the file
   * @throws FileNotFoundException    if input file doesn't exist
   * @throws IOException              if reader fails to read file
   */
  static ArrayList<String> readInputFile(String filename)
      throws FileNotFoundException, IOException {
    InputStream inputStream = Utils.class.getClassLoader().getResourceAsStream(filename);

    if (inputStream == null) {
      throw new FileNotFoundException("Could not find " + filename + ".");
    }

    InputStreamReader streamReader = new InputStreamReader(inputStream);
    BufferedReader reader = new BufferedReader(streamReader);
    ArrayList<String> data = new ArrayList<>();

    try {
      for (String line; (line = reader.readLine()) != null;) {
        data.add(line);
      }
    } catch (IOException e) {
      throw new IOException("Could not read " + filename + ".");
    }

    inputStream.close();
    streamReader.close();
    reader.close();

    return data;
  }
}