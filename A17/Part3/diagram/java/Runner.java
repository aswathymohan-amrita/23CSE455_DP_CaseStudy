import java.io.*;
import java.util.*;

public class Runner {
    public static void main(String[] args) throws Exception {
        List<String> lines = new BufferedReader(new InputStreamReader(System.in)).lines().toList();
        try {
            DiagramSystem.Diagram model = new DiagramSystem.DiagramParser().parse(lines);
            DiagramSystem.Renderer renderer = switch (args[0]) {
                case "bracketed" -> new DiagramSystem.Bracketed();
                case "json" -> new DiagramSystem.NamesAdapter();
                default -> new DiagramSystem.Compact();
            };
            System.out.println(new DiagramSystem.Exporter(renderer).export(model));
        } catch (IllegalArgumentException error) {
            System.out.println("ERROR:" + error.getMessage());
        }
    }
}
