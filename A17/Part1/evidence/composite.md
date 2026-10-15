# Class header text-block composition

Treat a single drawable and an aggregate of drawables through the same measurement and drawing interface.

TextBlockHorizontal and TextBlockVertical hold lists of TextBlock children, recursively measure them, and draw each through the component interface with translated coordinates. CircledCharacter is the inspected leaf. EntityImageClassHeader builds the header from smaller blocks through TextBlockUtils. The entity/link graph itself is not the evidence for Composite.

## Component: net.sourceforge.plantuml.klimt.shape.TextBlock

Methods: calculateDimension; inherited drawU. Source: `src/main/java/net/sourceforge/plantuml/klimt/shape/TextBlock.java:47-67`.

```java
  47 public interface TextBlock extends UDrawable, UShape {
  48 
  49 	public XDimension2D calculateDimension(StringBounder stringBounder);
  50 
  51 	public default MinMax getMinMax(StringBounder stringBounder) {
  52 		throw new UnsupportedOperationException(getClass().toString());
  53 	}
  54 
  55 	public default XRectangle2D getInnerPosition(CharSequence member, StringBounder stringBounder) {
  56 		throw new UnsupportedOperationException("member=" + member + " " + getClass().toString());
  57 	}
```

## Composite base: net.sourceforge.plantuml.klimt.shape.TextBlockMemoized

Methods: calculateDimension; calculateDimensionSlow. Source: `src/main/java/net/sourceforge/plantuml/klimt/shape/TextBlockMemoized.java:50-72`.

```java
  50 public abstract class TextBlockMemoized implements TextBlock {
  51 
  52 	private XDimension2D cachedDimension;
  53 	private Class<? extends StringBounder> lastCaller;
  54 
  55 	@Override
  56 	public final XDimension2D calculateDimension(StringBounder stringBounder) {
  57 		final Class<? extends StringBounder> currentCaller = stringBounder.getClass();
  58 		if (cachedDimension == null || lastCaller != currentCaller) {
  59 			cachedDimension = calculateDimensionSlow(stringBounder);
  60 			lastCaller = currentCaller;
```

## Composite: net.sourceforge.plantuml.klimt.shape.TextBlockHorizontal

Methods: calculateDimensionSlow; drawU. Source: `src/main/java/net/sourceforge/plantuml/klimt/shape/TextBlockHorizontal.java:48-95`.

```java
  48 public class TextBlockHorizontal extends TextBlockMemoized {
  49 
  50 	private final List<TextBlock> blocks = new ArrayList<>();
  51 	private final VerticalAlignment alignment;
  52 
  53 	TextBlockHorizontal(TextBlock b1, TextBlock b2, VerticalAlignment alignment) {
  54 		this.blocks.add(b1);
  55 		this.blocks.add(b2);
  56 		this.alignment = alignment;
  57 	}
  58 
```

## Composite: net.sourceforge.plantuml.klimt.shape.TextBlockVertical

Methods: calculateDimensionSlow; drawU. Source: `src/main/java/net/sourceforge/plantuml/klimt/shape/TextBlockVertical.java:51-134`.

```java
  51 public class TextBlockVertical extends TextBlockMemoized implements WithPorts {
  52 
  53 	private final List<TextBlock> blocks = new ArrayList<>();
  54 	private final HorizontalAlignment horizontalAlignment;
  55 
  56 	TextBlockVertical(TextBlock b1, TextBlock b2, HorizontalAlignment horizontalAlignment) {
  57 		this.blocks.add(b1);
  58 		this.blocks.add(b2);
  59 		this.horizontalAlignment = horizontalAlignment;
  60 	}
  61 
```

## Representative leaf: net.sourceforge.plantuml.klimt.shape.CircledCharacter

Methods: calculateDimension; drawU. Source: `src/main/java/net/sourceforge/plantuml/klimt/shape/CircledCharacter.java:46-88`.

```java
  46 public class CircledCharacter implements TextBlock {
  47 
  48 	private final String c;
  49 	private final UFont font;
  50 	private final HColor spotBackColor;
  51 	private final HColor spotBorder;
  52 	private final HColor fontColor;
  53 	private final double radius;
  54 
  55 	public CircledCharacter(char c, double radius, UFont font, HColor spotBackColor, HColor spotBorder,
  56 			HColor fontColor) {
```

## Client: net.sourceforge.plantuml.svek.image.EntityImageClassHeader

Methods: constructor. Source: `src/main/java/net/sourceforge/plantuml/svek/image/EntityImageClassHeader.java:74-279`.

```java
  74 public class EntityImageClassHeader extends AbstractEntityImage {
  75 
  76 	final private HeaderLayout headerLayout;
  77 
  78 	@Override
  79 	public StyleSignature getStyleSignature() {
  80 		return StyleSignatureBasic.of(SName.root, SName.element, SName.classDiagram, SName.class_, SName.header);
  81 	}
  82 
  83 	public EntityImageClassHeader(Entity entity, PortionShower portionShower) {
  84 		super(entity);
```

## Assembly helper: net.sourceforge.plantuml.klimt.shape.TextBlockUtils

Methods: mergeLR; mergeTB. Source: `src/main/java/net/sourceforge/plantuml/klimt/shape/TextBlockUtils.java:55-183`.

```java
  55 public class TextBlockUtils {
  56 
  57 	public static final TextBlock EMPTY_TEXT_BLOCK = TextBlockUtils.empty(0, 0);
  58 
  59 	public static TextBlock bordered(TextBlock textBlock, UStroke stroke, HColor borderColor, HColor backgroundColor,
  60 			double cornersize, ClockwiseTopRightBottomLeft margins, String id) {
  61 		return new TextBlockBordered(textBlock, stroke, borderColor, backgroundColor, cornersize, margins, id);
  62 	}
  63 
  64 	public static TextBlock withMargin(TextBlock textBlock, double marginX, double marginY) {
  65 		if (marginX == 0 && marginY == 0)
```

