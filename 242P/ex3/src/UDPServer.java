import java.io.BufferedWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.io.RandomAccessFile;
import java.io.StringWriter;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.nio.file.DirectoryStream;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.Files;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/**
 * @author zeyuhuang
 * @date 2019/11/19
 */
public class UDPServer {
    private static DatagramSocket st = null;
    private static String folderPathString = "";
    private static Path folderPath = null;

    private static class Task implements Callable<Void> {

        private DatagramPacket packet;
        private byte[] buf;
        private byte[] signBuf;
        private RandomAccessFile file;
        private String adress;

        Task(DatagramPacket packet, byte[] buf) {
            this.packet = packet;
            this.buf = buf;
            this.signBuf = new byte[4];
            this.adress = this.packet.getAddress().getHostAddress() + ":" + this.packet.getPort();
        }

        @Override
        public Void call() throws Exception {
            Thread.currentThread().setPriority(10);

            try {
                String command = new String(buf);
                command = command.replace("\0", "");
                System.out.println("Command received: " + command + " from " + adress);
                // System.out.println(command.length());
                // System.out.println(command.equals("index"));
                if (command.equals("index")) {
                    StringBuilder sb = new StringBuilder();
                    sb.append("Folder Path: " + folderPath.toAbsolutePath().toString() + "\n");
                    try (DirectoryStream<Path> stream = Files.newDirectoryStream(folderPath)) {
                        for (Path p : stream) {
                            sb.append(p.getFileName() + "\n");
                        }
                        String message = sb.toString();
                        System.out.print(message);
                        packet.setData(message.getBytes(), 0, message.getBytes().length);
                        st.send(packet);

                    } catch (IOException e) {
                        System.err.println("Invalid folder path.");
                        e.printStackTrace();
                    }
                } else if (command.startsWith("get ")) {
                    String filePathString = command.split(" ")[1];
                    Path filePath = Paths.get(folderPathString + "/" + filePathString);
                    if (Files.notExists(filePath)) {
                        packet.setData("error\nInvalid file name.".getBytes(), 0,
                                "error\nInvalid file name.".getBytes().length);
                        st.send(packet);
                        System.err.println("Invalid file name.");
                    } else {
                        file = new RandomAccessFile(folderPathString + "/" + filePathString, "r");
                        int packetCount = 1;
                        int reciveSize = -1;

                        while ((reciveSize = file.read(buf)) != -1) {
                            packet.setData(buf, 0, reciveSize);
                            st.send(packet);
                            // wait for succ respons
                            while (true) {
                                packet.setData(signBuf, 0, signBuf.length);
                                st.receive(packet);
                                String reply = new String(signBuf);
                                reply = reply.replace("\0", "");
                                if (reply.equals("succ")) {
                                    break;
                                } else {
                                    System.out.println("resent packet " + packetCount);
                                    packet.setData(buf, 0, reciveSize);
                                    st.send(packet);
                                }
                            }
                            System.out.println("The No." + (packetCount++) + " packets sent successfully.");
                        }
                        while (true) {
                            System.out.println("Send exit sign");
                            packet.setData("exit".getBytes(), 0, "exit".getBytes().length);
                            st.send(packet);

                            packet.setData(signBuf, 0, signBuf.length);
                            st.receive(packet);
                            // exit
                            String reply = new String(signBuf);
                            reply = reply.replace("\0", "");

                            if (reply.equals("exit")) {
                                break;
                            } else {
                                System.out.println("Resent exit sign");
                                packet.setData("exit".getBytes(), 0, "exit".getBytes().length);
                                st.send(packet);
                            }
                        }

                    }
                } else {
                    packet.setData("error\nInvalid file name.".getBytes(), 0,
                            "error\nInvalid file name.".getBytes().length);
                    st.send(packet);
                    System.err.println("Invalid command.");
                }

            } catch (Exception e) {
                e.printStackTrace();
            }
            return null;
        }
    }

    public static void main(String[] args) {
        // if (args.length != 1) {
        // System.err.println("Please input the folder path.");
        // return;
        // }
        // folderPathString = args[0];
        folderPathString = "/Users/zeyuhuang/Developer/UCI-MSWE-FALL2019/242P/ex3/data";
        folderPath = Paths.get(folderPathString);
        if (!Files.isDirectory(folderPath)) {
            System.err.println("Invalid folder path.");
            return;
        }

        ExecutorService pool = Executors.newFixedThreadPool(50);

        try {
            // UDP server socket has to be exposed to threads
            InetAddress inetAd = InetAddress.getByName(UDPUtils.ADRESS);
            st = new DatagramSocket(UDPUtils.PORT, inetAd);
            System.out.println("Socket at port " + st.getLocalPort());
            st.setSoTimeout(UDPUtils.TIMEOUT);

            while (true) {
                try {
                    byte[] buf = new byte[UDPUtils.BUFFER_SIZE];
                    DatagramPacket packet = new DatagramPacket(buf, UDPUtils.BUFFER_SIZE);
                    Thread.sleep(2000);
                    st.receive(packet);
                    String command = new String(buf);
                    command = command.replace("\0", "");
                    System.out.println(command);
                    if (command.equals("index") || command.startsWith("get ")) {
                        System.out.println("Packet received from " + packet.getAddress().getHostAddress() + ":"
                                + packet.getPort());
                        pool.submit(new Task(packet, buf));
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            try {
                if (st != null) {
                    st.close();
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }
}
