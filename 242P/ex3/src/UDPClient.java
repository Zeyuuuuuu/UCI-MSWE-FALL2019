import java.io.BufferedReader;
import java.io.Console;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.*;

/**
 * @author zeyuhuang
 * @date 2019/11/19
 */
public class UDPClient {

    public static void main(String[] args) {
        DatagramSocket st = null;
        try {
            byte[] buf = new byte[UDPUtils.BUFFER_SIZE];
            InetAddress inetAd = InetAddress.getByName(UDPUtils.ADRESS);
            int num = 0 + (int) (Math.random() * (7999 + 1));

            st = new DatagramSocket(num, inetAd);
            System.out.println("Socket at port " + st.getLocalPort());
            st.setSoTimeout(UDPUtils.TIMEOUT);
            DatagramPacket packet = new DatagramPacket(buf, UDPUtils.BUFFER_SIZE, inetAd, UDPUtils.PORT);
            BufferedReader keyboardIn = new BufferedReader(new InputStreamReader(System.in));// from keyboard

            while (true) {
                System.out.print("client> ");
                String command = keyboardIn.readLine();
                if (command.equals("index") || command.startsWith("get ")) {
                    packet.setData(command.getBytes(), 0, command.getBytes().length);
                    st.send(packet);
                    packet.setData(buf, 0, buf.length);
                    st.receive(packet);
                    int packetCount = 1;
                    int reciveSize = 0;
                    StringBuilder sb = new StringBuilder();
                    if (command.equals("index")) {
                        String reply = new String(buf);
                        reply = reply.replace("\0", "");
                        sb.append(reply);
                    } else {
                        while ((reciveSize = packet.getLength()) != 0) {
                            // if a is exit sign is recived
                            String reply = new String(buf);
                            reply = reply.replace("\0", "");
                            if (reply.equals("exit")) {
                                System.out.println("End");
                                packet.setData("exit".getBytes(), 0, "exit".getBytes().length);
                                st.send(packet);
                                break;
                            }
                            sb.append(reply);
                            // System.out.print(sb.toString());
                            packet.setData("succ".getBytes(), 0, "succ".getBytes().length);
                            st.send(packet);
                            buf = new byte[UDPUtils.BUFFER_SIZE];
                            packet.setData(buf, 0, buf.length);
                            System.out.println("The No." + (packetCount++) + " packets received successfully.");
                            st.receive(packet);
                        }
                    }
                    sb.append("\n");
                    String res = sb.toString();
                    System.out.print(res);

                    if (command.startsWith("get ") && !res.startsWith("error")) {
                        break;
                    }
                } else {
                    System.err.println("Invalid command.");
                }
            }
        } catch (ConnectException e) {
            System.err.println("Timeout.");
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            try {
                if (st != null)
                    st.close();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }
}
