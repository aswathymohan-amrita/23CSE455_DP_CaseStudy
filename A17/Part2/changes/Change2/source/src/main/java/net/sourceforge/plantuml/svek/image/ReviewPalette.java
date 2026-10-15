package net.sourceforge.plantuml.svek.image;

/** Optional review-state fill policy. Explicit class colors take precedence. */
interface ReviewPalette {
	String background(String status);

	static ReviewPalette select(String name) {
		if ("pastel".equalsIgnoreCase(name))
			return new Pastel();
		if ("mono".equalsIgnoreCase(name))
			return new Mono();
		return null;
	}

	final class Pastel implements ReviewPalette {
		public String background(String status) {
			switch (status) {
			case "approved": return "#D4EDDA";
			case "rejected": return "#F8D7DA";
			default: return "#FFF3CD";
			}
		}
	}

	final class Mono implements ReviewPalette {
		public String background(String status) {
			return "#EEEEEE";
		}
	}
}
