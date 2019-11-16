import java.util.concurrent.*;

public class TrafficController {
    private Integer l2r = 0;
    private Integer r2l = 0;

    public void enterLeft() {
        synchronized (this) {
            while (r2l != 0) {
                try {
                    wait();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
            l2r++;
            notifyAll();

        }

    }

    public void enterRight() {
        synchronized (this) {
            while (l2r != 0) {
                try {
                    wait();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
            r2l++;
            notifyAll();

        }
    }

    public void leaveLeft() {
        synchronized (this) {
            r2l--;
            notifyAll();
        }
    }

    public void leaveRight() {
        synchronized (this) {
            l2r--;
            notifyAll();
        }

    }

}