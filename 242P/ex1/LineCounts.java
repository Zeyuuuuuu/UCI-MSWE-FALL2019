
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.io.LineNumberReader;

class LineCounts {
    public static void main(String args[]) {
        for (int i = 0; i < args.length; i++)
            countLines(args[i]);

    }

    public static void countLines(String path) {

        try {
            File file = new File(path);
            if (file.exists()) {
                FileReader fr = new FileReader(file);
                LineNumberReader lnr = new LineNumberReader(fr);
                int linenumber = 0;
                while (lnr.readLine() != null) {
                    linenumber++;
                }
                System.out.println(path + ": " + linenumber);
                lnr.close();
            } else {
                System.out.println("File \'" + path + "\' does not exists!");
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}