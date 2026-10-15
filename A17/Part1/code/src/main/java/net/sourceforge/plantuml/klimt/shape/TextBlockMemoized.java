/* ========================================================================
 * PlantUML : a free UML diagram generator
 * ========================================================================
 *
 * (C) Copyright 2009-2024, Arnaud Roques
 *
 * Project Info:  https://plantuml.com
 * 
 * If you like this project or if you find it useful, you can support us at:
 * 
 * https://plantuml.com/patreon (only 1$ per month!)
 * https://plantuml.com/paypal
 * 
 * This file is part of PlantUML.
 *
 * PlantUML is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * PlantUML distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
 * or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
 * License for more details.
 *
 * You should have received a copy of the GNU General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301,
 * USA.
 *
 *
 * Original Author:  Arnaud Roques
 * 
 *
 */
package net.sourceforge.plantuml.klimt.shape;

import net.sourceforge.plantuml.klimt.font.StringBounder;
import net.sourceforge.plantuml.klimt.geom.XDimension2D;

/**
 * Abstract base class for TextBlock implementations where
 * calculateDimension() is expensive. The result is memoized and
 * automatically invalidated when the StringBounder type changes.
 * <p>
 * Subclasses must implement {@link #calculateDimensionSlow(StringBounder)}
 * with the real computation. Callers use the standard
 * {@link #calculateDimension(StringBounder)} which is final and cached.
 */
public abstract class TextBlockMemoized implements TextBlock {

	private XDimension2D cachedDimension;
	private Class<? extends StringBounder> lastCaller;

	@Override
	public final XDimension2D calculateDimension(StringBounder stringBounder) {
		final Class<? extends StringBounder> currentCaller = stringBounder.getClass();
		if (cachedDimension == null || lastCaller != currentCaller) {
			cachedDimension = calculateDimensionSlow(stringBounder);
			lastCaller = currentCaller;
		}
		return cachedDimension;
	}

	protected abstract XDimension2D calculateDimensionSlow(StringBounder stringBounder);

	protected void invalidateDimensionCache() {
		cachedDimension = null;
		lastCaller = null;
	}

}
