
/**
 * @author zeyuhuang
 * @date 2019/11/19
 */
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.nio.file.Files;
import java.nio.file.Path;
import java.io.IOException;

public class TCPClient {
    public static void main(String[] args) {
        try {
            Socket st = new Socket("localhost", 8000);
            PrintWriter out = new PrintWriter(st.getOutputStream(), true);// to server
            BufferedReader in = new BufferedReader(new InputStreamReader(st.getInputStream()));// from server
            BufferedReader keyboardIn = new BufferedReader(new InputStreamReader(System.in));// from keyboard
            while (true) {
                System.out.print("client> ");
                String command = keyboardIn.readLine();
                if (command.equals("index") || command.startsWith("get ")) {
                    out.println(command);
                    String firstLine = "";
                    String line = "";
                    while (!(line = in.readLine()).equals("EOF")) {
                        if (firstLine.equals("")) {
                            firstLine = line;
                        }
                        System.out.println(line);
                    }

                    if (command.startsWith("get ") && !firstLine.startsWith("error")) {
                        break;
                    }
                } else {
                    System.err.println("Invalid command.");
                }
                out.flush();
            }
            
            out.close();
            in.close();
            st.close();
        } catch (Exception e) {
            e.printStackTrace();
        }

    }
}
