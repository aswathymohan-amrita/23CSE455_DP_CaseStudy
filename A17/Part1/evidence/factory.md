# Class diagram product creation

Let a specialized parser factory choose the diagram product while the superclass retains the parsing lifecycle.

PSystemCommandFactory.createSystem calls the abstract createEmptyDiagram hook. ClassDiagramFactory overrides it with a covariant ClassDiagram return and constructs that product. This is a virtual creation hook used by superclass code, not merely a helper named factory.

## Creator: net.sourceforge.plantuml.command.PSystemCommandFactory

Methods: createSystem; createEmptyDiagram. Source: `src/main/java/net/sourceforge/plantuml/command/PSystemCommandFactory.java:61-309`.

```java
  61 public abstract class PSystemCommandFactory extends PSystemAbstractFactory {
  62 
  63 	private final List<Command> cmds = new ArrayList<>();
  64 
  65 	protected abstract void initCommandsList(List<Command> cmds);
  66 
  67 	public abstract AbstractDiagram createEmptyDiagram(PathSystem pathSystem, UmlSource source, Previous previous,
  68 			PreprocessingArtifact preprocessing);
  69 
  70 	protected PSystemCommandFactory(DiagramType type) {
  71 		super(type);
```

## ConcreteCreator: net.sourceforge.plantuml.classdiagram.ClassDiagramFactory

Methods: createEmptyDiagram. Source: `src/main/java/net/sourceforge/plantuml/classdiagram/ClassDiagramFactory.java:88-173`.

```java
  88 public class ClassDiagramFactory extends PSystemCommandFactory {
  89 
  90 	public ClassDiagramFactory() {
  91 		super(DiagramType.CLASS);
  92 	}
  93 
  94 	@Override
  95 	public ClassDiagram createEmptyDiagram(PathSystem pathSystem, UmlSource source, Previous previous,
  96 			PreprocessingArtifact preprocessing) {
  97 		return new ClassDiagram(source, previous, preprocessing);
  98 	}
```

## Product: net.sourceforge.plantuml.core.AbstractDiagram

Methods: executeCommand; exportDiagram contract. Source: `src/main/java/net/sourceforge/plantuml/core/AbstractDiagram.java:67-273`.

```java
  67 public abstract class AbstractDiagram implements Diagram {
  68 
  69 	private final UmlSource source;
  70 	private Scale scale;
  71 	private int splitPagesHorizontal = 1;
  72 	private int splitPagesVertical = 1;
  73 	private final Map<String, String> md5map;
  74 
  75 	private final PreprocessingArtifact preprocessing;
  76 
  77 	public AbstractDiagram(UmlSource source, PreprocessingArtifact preprocessing) {
```

## ConcreteProduct: net.sourceforge.plantuml.classdiagram.ClassDiagram

Methods: constructor. Source: `src/main/java/net/sourceforge/plantuml/classdiagram/ClassDiagram.java:49-101`.

```java
  49 public class ClassDiagram extends AbstractClassOrObjectDiagram {
  50 
  51 	public ClassDiagram(UmlSource source, Previous previous, PreprocessingArtifact preprocessingArtifact) {
  52 		super(source, DiagramType.CLASS, previous, preprocessingArtifact);
  53 	}
  54 
  55 	private boolean allowMixing;
  56 
  57 	public void setAllowMixing(boolean allowMixing) {
  58 		this.allowMixing = allowMixing;
  59 	}
```

