# Class diagram layout backend selection

Select a layout algorithm without forcing the caller to know each backend's graph processing steps.

CucaDiagram.getTextBlock selects a CucaDiagramFileMaker based on TeaVM, ELK, Smetana and Graphviz availability, then delegates to getTextBlock with the same arguments. Svek uses the external dot pipeline; Smetana performs layout in Java. ELK and TeaVM branches are source-verified but not exercised by the A17 tests.

## Context: net.atmp.CucaDiagram

Methods: getTextBlock; dotIsAvailable. Source: `src/main/java/net/atmp/CucaDiagram.java:109-959`.

```java
 109 public abstract class CucaDiagram extends TitledDiagram implements GroupHierarchy, PortionShower, EntityFactory {
 110 
 111 	static class EntityHideOrShow {
 112 		private final EntityGender gender;
 113 		private final EntityPortion portion;
 114 		private final boolean show;
 115 
 116 		EntityHideOrShow(EntityGender gender, EntityPortion portion, boolean show) {
 117 			this.gender = gender;
 118 			this.portion = portion;
 119 			this.show = show;
```

## Strategy: net.sourceforge.plantuml.svek.CucaDiagramFileMaker

Methods: getTextBlock. Source: `src/main/java/net/sourceforge/plantuml/svek/CucaDiagramFileMaker.java:46-71`.

```java
  46 public abstract class CucaDiagramFileMaker {
  47 
  48 	protected final CucaDiagram diagram;
  49 	protected final Bibliotekon bibliotekon;
  50 	protected final ClusterManager clusterManager;
  51 
  52 	public CucaDiagramFileMaker(CucaDiagram diagram) {
  53 		this(diagram, diagram.getRootGroup());
  54 	}
  55 
  56 	public CucaDiagramFileMaker(CucaDiagram diagram, Entity root) {
```

## ConcreteStrategy: net.sourceforge.plantuml.svek.CucaDiagramFileMakerSvek

Methods: getTextBlock. Source: `src/main/java/net/sourceforge/plantuml/svek/CucaDiagramFileMakerSvek.java:52-116`.

```java
  52 public final class CucaDiagramFileMakerSvek extends CucaDiagramFileMaker {
  53 
  54 	public CucaDiagramFileMakerSvek(CucaDiagram diagram) throws IOException {
  55 		super(diagram);
  56 
  57 	}
  58 
  59 	@Override
  60 	public TextBlock getTextBlock(List<String> dotStrings, FileFormatOption fileFormatOption)
  61 			throws IOException, InterruptedException {
  62 
```

## ConcreteStrategy: net.sourceforge.plantuml.sdot.CucaDiagramFileMakerSmetana

Methods: getTextBlock. Source: `src/main/java/net/sourceforge/plantuml/sdot/CucaDiagramFileMakerSmetana.java:116-925`.

```java
 116 public class CucaDiagramFileMakerSmetana extends CucaDiagramFileMaker {
 117 	private final Map<Entity, ST_Agnode_s> nodes = new LinkedHashMap<Entity, ST_Agnode_s>();
 118 	private final Map<Entity, ST_Agnode_s> coreNodes = new LinkedHashMap<Entity, ST_Agnode_s>();
 119 	private final Map<Link, ST_Agedge_s> edges = new LinkedHashMap<Link, ST_Agedge_s>();
 120 	private final Map<Link, SmetanaEdge> smetanaPathes = new LinkedHashMap<Link, SmetanaEdge>();
 121 	private final Map<Entity, ST_Agraph_s> clusters = new LinkedHashMap<Entity, ST_Agraph_s>();
 122 
 123 	private final Rankdir rankdir;
 124 
 125 	private final Entity root;
 126 
```

## ConcreteStrategy: net.sourceforge.plantuml.elk.CucaDiagramFileMakerElk

Methods: getTextBlock. Source: `src/main/java/net/sourceforge/plantuml/elk/CucaDiagramFileMakerElk.java:138-501`.

```java
 138 public class CucaDiagramFileMakerElk extends CucaDiagramFileMaker {
 139 
 140 	private final Map<Entity, ElkNode> nodes = new LinkedHashMap<Entity, ElkNode>();
 141 	private final Map<Entity, ElkNode> clusters = new LinkedHashMap<Entity, ElkNode>();
 142 	private final Map<Link, ElkEdge> edges = new LinkedHashMap<Link, ElkEdge>();
 143 
 144 	public CucaDiagramFileMakerElk(CucaDiagram diagram) {
 145 		super(diagram);
 146 	}
 147 
 148 	// Duplication from SvekEdge
```

## ConcreteStrategy: net.sourceforge.plantuml.svek.CucaDiagramFileMakerTeaVM

Methods: getTextBlock. Source: `src/main/java/net/sourceforge/plantuml/svek/CucaDiagramFileMakerTeaVM.java:56-148`.

```java
  56 public final class CucaDiagramFileMakerTeaVM extends CucaDiagramFileMaker {
  57 	// ::remove file when JAVA8
  58 
  59 	public CucaDiagramFileMakerTeaVM(CucaDiagram diagram) {
  60 		super(diagram);
  61 	}
  62 
  63 	@Override
  64 	public TextBlock getTextBlock(List<String> dotStrings, FileFormatOption fileFormatOption)
  65 			throws IOException, InterruptedException {
  66 
```

