import java.util.concurrent.*;

public class Main3 {

    private static void nap(int millisecs) {
        try {
            Thread.sleep(millisecs);
        } catch (InterruptedException e) {
            System.err.println(e.getMessage());
        }
    }

    private static void addProc(HighLevelDisplay d) {

        // Add a sequence of addRow operations with short random naps.
        int i = 0;
        while (true) {
            d.addRow("AAAAAAAAAAAA  " + i);
            // d.addRow("BBBBBBBBBBBB " + i);
            i++;
            nap(50);
        }
    }

    private static void deleteProc(HighLevelDisplay d) {

        // Add a sequence of deletions of row 0 with short random naps.
        while (true) {
            d.deleteRow(0);
            nap(3000);
        }

    }

    public static void main(String[] args) {
        final HighLevelDisplay d = new JDisplay2();

        new Thread() {
            public void run() {
                addProc(d);
            }
        }.start();

        new Thread() {
            public void run() {
                deleteProc(d);
            }
        }.start();

    }
}