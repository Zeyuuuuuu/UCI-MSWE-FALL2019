import java.util.Scanner;
import java.util.concurrent.*;
import java.util.ArrayList;

public class MessageQueue {
	private static int n_ids;

	// 1.
	public static void main1(String[] args) {
		BlockingQueue<Message> queue = new ArrayBlockingQueue<Message>(10);

		Producer p1 = new Producer(queue, n_ids++);
		Consumer c1 = new Consumer(queue, n_ids++);

		new Thread(p1).start();
		new Thread(c1).start();

		try {
			Thread.sleep(10000);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		p1.stop();
	}

	// 2.
	public static void main2(String[] args) {
		BlockingQueue<Message> queue = new ArrayBlockingQueue<Message>(10);

		Producer p1 = new Producer(queue, n_ids++);
		Consumer c1 = new Consumer(queue, n_ids++);
		Consumer c2 = new Consumer(queue, n_ids++);

		new Thread(p1).start();
		new Thread(c1).start();
		new Thread(c2).start();

		try {
			Thread.sleep(10000);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		p1.stop();
		try {
			queue.put(new Message("stop")); // Put this final message in the queue
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
	}

	// 3.
	public static void main3(String[] args) {
		BlockingQueue<Message> queue = new ArrayBlockingQueue<Message>(10);

		Producer p1 = new Producer(queue, n_ids++);
		Producer p2 = new Producer(queue, n_ids++);

		Consumer c1 = new Consumer(queue, n_ids++);
		Consumer c2 = new Consumer(queue, n_ids++);

		new Thread(p1).start();
		new Thread(p2).start();
		new Thread(c1).start();
		new Thread(c2).start();

		try {
			Thread.sleep(10000);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		p1.stop();
		p2.stop();
	}

	// 4.
	public static void main(String[] args) {
		BlockingQueue<Message> queue = new ArrayBlockingQueue<Message>(10);
		int N;
		int M;
		Scanner sc = new Scanner(System.in);
		M = sc.nextInt();
		N = sc.nextInt();
		ArrayList<Producer> Producers = new ArrayList<>();
		for (int i = 0; i < M; i++) {
			Producer p = new Producer(queue, n_ids++);
			Producers.add(p);
			new Thread(p).start();
		}
		for (int i = 0; i < N; i++) {
			new Thread(new Consumer(queue, n_ids++)).start();
		}
		try {
			Thread.sleep(10000);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		for (int i = 0; i < N - M; i++) {
			try {
				queue.put(new Message("stop")); // Put this final message in the queue
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
		for (int i = 0; i < M; i++) {
			Producers.get(i).stop();
		}

	}
}
