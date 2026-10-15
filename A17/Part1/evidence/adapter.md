# VizJs output-stream bridge

Expose a string-returning JavaScript layout engine through PlantUML's existing Graphviz output-stream interface.

GraphvizJs implements Graphviz.createFile3(OutputStream). It submits a VizJsEngine.execute(dotString) operation, obtains its SVG String, writes bytes to the requested stream and returns ProcessState. VizJsEngine reflectively calls ch.braincell.viz.VizJS. This incompatible-interface conversion establishes Adapter intent. Optional VizJs execution is not claimed.

## Target: net.sourceforge.plantuml.dot.Graphviz

Methods: createFile3. Source: `src/main/java/net/sourceforge/plantuml/dot/Graphviz.java:41-52`.

```java
  41 public interface Graphviz {
  42 	public String dotVersion();
  43 
  44 	public boolean graphviz244onWindows();
  45 
  46 	public ProcessState createFile3(OutputStream os);
  47 
  48 	public File getDotExe();
  49 
  50 	public ExeState getExeState();
  51 
```

## Adapter: net.sourceforge.plantuml.vizjs.GraphvizJs

Methods: createFile3; submitJob. Source: `src/main/java/net/sourceforge/plantuml/vizjs/GraphvizJs.java:52-153`.

```java
  52 public class GraphvizJs implements Graphviz {
  53     // ::remove folder when __HAXE__
  54 	
  55 
  56 	private final static ExecutorService executorService = Executors
  57 			.newSingleThreadScheduledExecutor(new ThreadFactory() {
  58 				public Thread newThread(Runnable runnable) {
  59 					return new JsThread(runnable);
  60 				}
  61 			});
  62 
```

## Adaptee facade: net.sourceforge.plantuml.vizjs.VizJsEngine

Methods: execute. Source: `src/main/java/net/sourceforge/plantuml/vizjs/VizJsEngine.java:41-68`.

```java
  41 public class VizJsEngine {
  42 
  43 	public static boolean isOk() {
  44 		try {
  45 			final Class classVizJS = Class.forName("ch.braincell.viz.VizJS");
  46 			return true;
  47 		} catch (Exception e) {
  48 			return false;
  49 		}
  50 	}
  51 
```

## Client: net.sourceforge.plantuml.svek.DotStringFactory

Methods: getSvg; createFile3 call. Source: `src/main/java/net/sourceforge/plantuml/svek/DotStringFactory.java:70-654`.

```java
  70 public final class DotStringFactory implements Moveable {
  71 
  72 	private final DiagramType diagramType;
  73 	private final ISkinParam skinParam;
  74 	private final Bibliotekon bibliotekon;
  75 	private final Cluster root;
  76 
  77 	public DotStringFactory(Bibliotekon bibliotekon, Cluster root, DiagramType diagramType, ISkinParam skinParam) {
  78 		this.bibliotekon = bibliotekon;
  79 		this.skinParam = skinParam;
  80 		this.diagramType = diagramType;
```

## Adapter selection: net.sourceforge.plantuml.dot.GraphvizRuntimeEnvironment

Methods: create. Source: `src/main/java/net/sourceforge/plantuml/dot/GraphvizRuntimeEnvironment.java:56-238`.

```java
  56 public class GraphvizRuntimeEnvironment {
  57 	
  58 
  59 	public static final String VIZJS = "vizjs";
  60 
  61 	private final static GraphvizRuntimeEnvironment singleton = new GraphvizRuntimeEnvironment();
  62 
  63 	private final Map<File, GraphvizVersion> map = new ConcurrentHashMap<File, GraphvizVersion>();
  64 	private String dotExecutable;
  65 	private String dotVersion;
  66 
```

