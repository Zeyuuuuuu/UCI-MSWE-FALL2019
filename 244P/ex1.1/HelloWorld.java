import java.util.*;

class myThread extends Thread {
    private volatile boolean isShutdown = true;

    public void shutdown() {
        this.isShutdown = false;
        interrupt();
    }

    @Override
    public void run() {
        while (this.isShutdown) {
            System.out.println("Hello World! I'm " + this.getName() + ". The time is " + System.currentTimeMillis());
            try {
                Thread.sleep(2000);
            } catch (InterruptedException e) {
                System.out.println("Stop " + this.getName());
            }
        }
    }
}

public class HelloWorld {
    public static void main(String[] args) {
        Scanner sc = null;
        boolean isRunning = true;
        HashMap<String, myThread> threadsGroup = new HashMap<String, myThread>();
        try {
            sc = new Scanner(System.in);
            while (isRunning) {
                System.out.println(
                        "\nHere are your options:\na - Create a new thread\nb - Stop a given thread (e.g. \"b 2\" kills thread 2)\nc - Stop all threads and exit this program\n");
                String input = sc.nextLine();
                if (input.equals("a")) {
                    myThread newThread = new myThread();
                    threadsGroup.put(newThread.getName().substring(7), newThread);
                    newThread.start();
                } else if (input.charAt(0) == 'b') {
                    String index = input.substring(2);
                    if (!threadsGroup.containsKey(index)) {
                        System.out.println("Invalid Input!\n");
                    } else {
                        threadsGroup.get(index).shutdown();
                        threadsGroup.remove(index);
                    }

                } else if (input.equals("c")) {
                    isRunning = false;
                    for (String index : threadsGroup.keySet()) {
                        threadsGroup.get(index).shutdown();
                    }
                    threadsGroup = null;

                } else {
                    System.out.println("Invalid Input!\n");
                }

            }
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            if (sc != null) {
                sc.close();
                sc = null;
            }
        }
    }
}