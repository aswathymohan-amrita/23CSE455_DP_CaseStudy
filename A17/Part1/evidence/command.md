# Class diagram command dispatch

Encapsulate recognized source instructions as interchangeable executable objects, separating command selection from model mutation.

PSystemCommandFactory.getCandidate selects a Command using isValid; executeFewLines delegates through AbstractDiagram.executeCommand. CommandCreateClass.executeArg creates or updates an Entity; CommandLinkClass.executeArg creates a Link and adds it to the receiver. CommandPragma handles the layout directive in the traced input. No undo/history support is claimed.

## Command: net.sourceforge.plantuml.command.Command

Methods: isValid; execute. Source: `src/main/java/net/sourceforge/plantuml/command/Command.java:42-58`.

```java
  42 public interface Command<D extends Diagram> {
  43 
  44 	CommandExecutionResult execute(D diagram, BlocLines lines, ParserPass currentPass) throws NoSuchColorException;
  45 
  46 	default String explain(BlocLines lines) {
  47 		return null;
  48 	}
  49 
  50 	CommandControl isValid(BlocLines lines);
  51 
  52 	boolean isEligibleFor(ParserPass pass);
```

## Shared command implementation: net.sourceforge.plantuml.command.SingleLineCommand2

Methods: execute; executeArg. Source: `src/main/java/net/sourceforge/plantuml/command/SingleLineCommand2.java:51-193`.

```java
  51 public abstract class SingleLineCommand2<S extends Diagram> implements Command<S> {
  52 
  53 	private final IRegex pattern;
  54 	private final boolean doTrim;
  55 
  56 	public SingleLineCommand2(IRegex pattern) {
  57 		this(true, pattern);
  58 	}
  59 
  60 	public SingleLineCommand2(boolean doTrim, IRegex pattern) {
  61 		this.doTrim = doTrim;
```

## ConcreteCommand: net.sourceforge.plantuml.classdiagram.command.CommandCreateClass

Methods: getRegexConcat; executeArg. Source: `src/main/java/net/sourceforge/plantuml/classdiagram/command/CommandCreateClass.java:71-247`.

```java
  71 public class CommandCreateClass extends SingleLineCommand2<ClassDiagram> {
  72 
  73 	enum Mode {
  74 		EXTENDS, IMPLEMENTS
  75 	};
  76 
  77 	public CommandCreateClass() {
  78 		super(getRegexConcat());
  79 	}
  80 
  81 	private static IRegex getRegexConcat() {
```

## ConcreteCommand: net.sourceforge.plantuml.classdiagram.command.CommandLinkClass

Methods: executeArg; addLink. Source: `src/main/java/net/sourceforge/plantuml/classdiagram/command/CommandLinkClass.java:73-553`.

```java
  73 final public class CommandLinkClass extends SingleLineCommand2<AbstractClassOrObjectDiagram> {
  74 
  75 	// Issue #2685: a separator is any single character that is not part of an
  76 	// identifier (letter, digit, _, $) and not a PlantUML syntactic
  77 	// character (space, #, :, {},<>,").
  78 
  79 	// This lets 'set separator' accept !, -, ~, @, |, /, etc. anything an author
  80 	// might want while keeping the parsing of class names and relations
  81 	// unambiguous.
  82 
  83 	// Note:
```

## ConcreteCommand: net.sourceforge.plantuml.command.CommandPragma

Methods: executeArg. Source: `src/main/java/net/sourceforge/plantuml/command/CommandPragma.java:52-139`.

```java
  52 public class CommandPragma extends SingleLineCommand2<TitledDiagram> {
  53 
  54 	public static final CommandPragma ME = new CommandPragma();
  55 
  56 	private CommandPragma() {
  57 		super(getRegexConcat());
  58 	}
  59 
  60 	static IRegex getRegexConcat() {
  61 		return RegexConcat.build(CommandPragma.class.getName(), RegexLeaf.start(), //
  62 				new RegexLeaf("!pragma"), //
```

## Invoker/selector: net.sourceforge.plantuml.command.PSystemCommandFactory

Methods: getCandidate; executeFewLines. Source: `src/main/java/net/sourceforge/plantuml/command/PSystemCommandFactory.java:61-309`.

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

## Execution bridge: net.sourceforge.plantuml.core.AbstractDiagram

Methods: executeCommand. Source: `src/main/java/net/sourceforge/plantuml/core/AbstractDiagram.java:67-273`.

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

## Client/registration: net.sourceforge.plantuml.classdiagram.ClassDiagramFactory

Methods: initCommandsList. Source: `src/main/java/net/sourceforge/plantuml/classdiagram/ClassDiagramFactory.java:88-173`.

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

## Receiver: net.sourceforge.plantuml.classdiagram.ClassDiagram

Methods: inherited reallyCreateLeaf; addLink. Source: `src/main/java/net/sourceforge/plantuml/classdiagram/ClassDiagram.java:49-101`.

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

## Receiver base: net.sourceforge.plantuml.objectdiagram.AbstractClassOrObjectDiagram

Methods: class diagram shared model. Source: `src/main/java/net/sourceforge/plantuml/objectdiagram/AbstractClassOrObjectDiagram.java:60-365`.

```java
  60 public abstract class AbstractClassOrObjectDiagram extends AbstractEntityDiagram {
  61 
  62 	public AbstractClassOrObjectDiagram(UmlSource source, DiagramType type, Previous previous,
  63 			PreprocessingArtifact preprocessingArtifact) {
  64 		super(source, type, previous, preprocessingArtifact);
  65 		setNamespaceSeparator(".");
  66 	}
  67 
  68 	final public boolean insertBetween(LineLocation location, Entity entity1, Entity entity2, Entity node) {
  69 		final Link link = foundLink(entity1, entity2);
  70 		if (link == null)
```

## Model element: net.sourceforge.plantuml.abel.Entity

Methods: setColors; setStereotype. Source: `src/main/java/net/sourceforge/plantuml/abel/Entity.java:89-775`.

```java
  89 final public class Entity implements SpecificBackcolorable, Hideable, Removeable, LineConfigurable, Bag {
  90 
  91 	private final StyleBuilder currentStyleBuilder;
  92 	private final CucaDiagram diagram;
  93 
  94 	private final Quark<Entity> quark;
  95 
  96 	private Url url;
  97 
  98 	private final Bodier bodier;
  99 	private final String uid;
```

## Model relationship: net.sourceforge.plantuml.abel.Link

Methods: constructor. Source: `src/main/java/net/sourceforge/plantuml/abel/Link.java:65-580`.

```java
  65 public class Link extends WithLinkType implements Hideable, Removeable {
  66 
  67 	public final StyleBuilder getStyleBuilder() {
  68 		return styleBuilder;
  69 	}
  70 
  71 	final private Entity cl1;
  72 	final private Entity cl2;
  73 
  74 	private String port1;
  75 	private String port2;
```

