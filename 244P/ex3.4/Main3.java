import java.util.concurrent.*;

public class Main3 {

    private static void nap(int millisecs) {
        try {
            Thread.sleep(millisecs);
        } catch (InterruptedException e) {
            System.err.println(e.getMessage());
        }
    }

    private static void addProc(HighLevelDisplay d, Semaphore s) {

        // Add a sequence of addRow operations with short random naps.
        int i = 0;
        while (true) {
            try {
                s.acquire();
            } catch (InterruptedException e) {
                System.err.println(e.getMessage());
            }
            d.addRow("AAAAAAAAAAAA  " + i);
            d.addRow("BBBBBBBBBBBB  " + i);
            s.release();
            i++;
            nap(500);
        }
    }

    private static void deleteProc(HighLevelDisplay d, Semaphore s) {

        // Add a sequence of deletions of row 0 with short random naps.
        while (true) {
            try {
                s.acquire();
            } catch (InterruptedException e) {
                System.err.println(e.getMessage());
            }
            d.deleteRow(0);
            s.release();
            nap(5000);
        }

    }

    public static void main(String[] args) {
        final HighLevelDisplay d = new JDisplay2();
        Semaphore s = new Semaphore(1);

        new Thread() {
            public void run() {
                addProc(d, s);
            }
        }.start();

        new Thread() {
            public void run() {
                deleteProc(d, s);
            }
        }.start();

    }
}