
/**
 * @author zeyuhuang
 * @date 2019/11/19
 */

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.ServerSocket;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.DirectoryStream;
import java.io.IOException;

public class TCPServer {

    public static void main(String[] args) {
        if (args.length != 1) {
            System.err.println("Please input the folder path.");
            return;
        }
        String folderPathString = args[0];
        Path folderPath = Paths.get(folderPathString);
        if (!Files.isDirectory(folderPath)) {
            System.err.println("Invalid folder path.");
            return;
        }

        try {
            ServerSocket ss = new ServerSocket(8000);
            Socket st = ss.accept();
            System.out.println("Server connected");
            BufferedReader in = new BufferedReader(new InputStreamReader(st.getInputStream()));// from client
            PrintWriter out = new PrintWriter(st.getOutputStream(), true);// to client
            while (true) {
                String command = in.readLine();// read from the client
                // System.out.println(command);
                if (command.equals("index")) {
                    StringBuilder sb = new StringBuilder();
                    sb.append("Folder Path: " + folderPath.toAbsolutePath().toString() + "\n");
                    try (DirectoryStream<Path> stream = Files.newDirectoryStream(folderPath)) {
                        for (Path p : stream) {
                            sb.append(p.getFileName() + "\n");
                        }
                        sb.append("EOF\n");
                        String message = sb.toString();
                        // System.out.print(message);
                        out.print(message);
                    } catch (IOException e) {
                        System.err.println("Invalid folder path.");
                        e.printStackTrace();
                    }
                } else if (command.startsWith("get ")) {
                    String filePathString = command.split(" ")[1];
                    // System.out.println(filePathString);
                    Path filePath = Paths.get(folderPathString + "/" + filePathString);
                    if (Files.notExists(filePath)) {
                        out.println("error\nInvalid file name.");
                        System.err.println("Invalid file name.");
                    } else {
                        StringBuilder sb = new StringBuilder();
                        sb.append("ok\n");
                        for (String line : Files.readAllLines(filePath)) {
                            sb.append(line + "\n");
                        }
                        sb.append("EOF\n");
                        String message = sb.toString();
                        out.println(message);
                        System.out.println("Server disconnected");
                        break;
                    }
                } else {
                    out.println("error\nInvalid file name.");
                    System.err.println("Invalid command.");
                }
                out.flush();// 清空缓存区
            }
            out.close();
            in.close();
            st.close();
            ss.close();

        } catch (Exception e) {
            e.printStackTrace();
        }

    }
}
