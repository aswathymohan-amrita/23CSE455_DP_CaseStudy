import java.io.ByteArrayOutputStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import net.sourceforge.plantuml.SourceStringReader;
import net.sourceforge.plantuml.FileFormat;
import net.sourceforge.plantuml.FileFormatOption;
import net.sourceforge.plantuml.classdiagram.ClassDiagram;

/** Integration checks use the real parser, model and renderer. */
public class EvolutionTest {
    private static int passed;
    private static String source(String body) {
        return "@startuml\n!pragma layout smetana\n" + body + "\n@enduml\n";
    }
    private static void check(boolean value, String name) {
        if (!value) throw new AssertionError(name);
        passed++;
        System.out.println("PASS " + name);
    }
    private static Object model(String body) {
        return new SourceStringReader(source(body)).getBlocks().get(0).getDiagram();
    }
    private static String svg(String body) throws Exception {
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        new SourceStringReader(source(body)).outputImage(out, new FileFormatOption(FileFormat.SVG));
        return out.toString(StandardCharsets.UTF_8.name());
    }
    public static void main(String[] args) throws Exception {
        int stage = Integer.parseInt(args[0]);
        Path evidence = Path.of(args[1]);
        Files.createDirectories(evidence);
        String plain = "class Order\nclass Customer\nOrder --> Customer";
        ClassDiagram base = (ClassDiagram) model(plain);
        check(base.leafs().size() == 2 && base.getLinks().size() == 1, "plain model has 2 nodes and 1 link");
        check(svg(plain).contains("Order"), "plain SVG contains class label");
        Files.writeString(evidence.resolve("plain.svg"), svg(plain));
        if (stage == 0) {
            check(!(model("class Order [review=pending]") instanceof ClassDiagram), "baseline rejects new syntax");
        } else {
            String reviewed = "class Order [review=pending]\nclass Customer [review=approved]\nOrder --> Customer";
            ClassDiagram d = (ClassDiagram) model(reviewed);
            check(d.leafs().size() == 2 && d.getLinks().size() == 1, "review preserves topology");
            check("pending".equals(d.leafs().iterator().next().getReviewStatus()), "status stored on entity");
            for (String status : new String[]{"pending", "approved", "rejected"})
                check(svg("class Order [review=" + status + "]").contains("[review: " + status + "]"), "visible " + status);
            check(!(model("class Order [review=unknown]") instanceof ClassDiagram), "unknown status rejected");
            ClassDiagram redeclared = (ClassDiagram) model("class Order [review=pending]\nclass Order");
            check("pending".equals(redeclared.leafs().iterator().next().getReviewStatus()), "plain redeclaration retains status");
            check(svg("class Order <<service>> #Pink [review=approved]").contains("#FFC0CB"), "existing stereotype and explicit color coexist");
            Files.writeString(evidence.resolve("review.puml"), source(reviewed));
            Files.writeString(evidence.resolve("review.svg"), svg(reviewed));
            ByteArrayOutputStream png = new ByteArrayOutputStream();
            new SourceStringReader(source(reviewed)).outputImage(png, new FileFormatOption(FileFormat.PNG));
            check(png.size() > 100 && png.toByteArray()[1] == 'P', "review renders PNG");
            Files.write(evidence.resolve("review.png"), png.toByteArray());
            if (stage >= 2) {
                String palette = "!pragma classReviewPalette pastel\n" + reviewed;
                check(svg(palette).contains("#FFF3CD") && svg(palette).contains("#D4EDDA"), "pastel colors follow review state");
                check(svg("!pragma classReviewPalette mono\n" + reviewed).contains("fill=\"#EEE\""), "mono policy selected");
                check(svg("!pragma classReviewPalette pastel\nclass Order #Pink [review=pending]").contains("#FFC0CB"), "explicit fill overrides policy");
                check(!(model("!pragma classReviewPalette invalid\nclass Order") instanceof ClassDiagram), "invalid palette rejected");
                Files.writeString(evidence.resolve("palette.puml"), source(palette));
                Files.writeString(evidence.resolve("palette.svg"), svg(palette));
            }
            if (stage >= 3) {
                String meta = "!pragma svgReviewMetadata true\n" + reviewed;
                check(svg(meta).contains("data-review-status=\"pending\""), "SVG metadata enabled");
                check(!svg(reviewed).contains("data-review-status="), "metadata default off");
                check(!svg("!pragma svgReviewMetadata false\n" + reviewed).contains("data-review-status="), "metadata explicit off");
                check(!svg("!pragma svgReviewMetadata true\nclass Order").contains("data-review-status="), "unreviewed nodes omit metadata");
                check(!(model("!pragma svgReviewMetadata maybe\nclass Order") instanceof ClassDiagram), "invalid metadata value rejected");
                Files.writeString(evidence.resolve("metadata.puml"), source(meta));
                Files.writeString(evidence.resolve("metadata.svg"), svg(meta));
            }
        }
        System.out.println("RESULT " + passed + "/" + passed);
    }
}
