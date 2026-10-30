import java.util.List;
import java.util.Map;
import java.util.Set;

/** Chain of Responsibility: Content Access Rule Chain (Region -> Maturity -> Premium). */
public final class ContentAccess {
    private ContentAccess() {}

    public record Show(int id, boolean premium, boolean adult, Set<Integer> genres) {}

    public record Viewer(int planTier, String region, String maturity) {}

    public record Decision(boolean allowed, String reason, String visibility) {
        static final Decision ALLOW = new Decision(true, null, null);

        @Override
        public String toString() {
            return allowed ? "ALLOW" : "DENY:" + reason + ":" + visibility;
        }
    }

    /** Handler. check() is also a template method: evaluate() is the primitive step. */
    public abstract static class AccessRule {
        private AccessRule next;

        public AccessRule setNext(AccessRule rule) {
            this.next = rule;
            return rule;
        }

        public final Decision check(Show show, Viewer viewer) {
            Decision denial = evaluate(show, viewer);
            if (denial != null) return denial;
            return next == null ? Decision.ALLOW : next.check(show, viewer);
        }

        protected abstract Decision evaluate(Show show, Viewer viewer);
    }

    public static final class RegionRule extends AccessRule {
        private static final Map<Integer, Set<String>> BLOCKED = Map.of(550, Set.of("CN"));
        private static final Map<Integer, Set<String>> ALLOWED = Map.of(1399, Set.of("US", "GB", "IN"));

        @Override
        protected Decision evaluate(Show show, Viewer viewer) {
            Set<String> allowed = ALLOWED.get(show.id());
            Set<String> blocked = BLOCKED.get(show.id());
            boolean denied = (allowed != null && !allowed.contains(viewer.region()))
                    || (blocked != null && blocked.contains(viewer.region()));
            return denied ? new Decision(false, "REGION_BLOCKED", "hidden") : null;
        }
    }

    public static final class MaturityRule extends AccessRule {
        private record Policy(boolean allowAdult, Set<Integer> blockedGenres) {}

        private static final Map<String, Policy> POLICIES = Map.of(
                "KIDS", new Policy(false, Set.of(27, 53, 80, 10752)),
                "TEEN", new Policy(false, Set.of(27)),
                "ADULT", new Policy(true, Set.of()),
                "NONE", new Policy(true, Set.of()));

        @Override
        protected Decision evaluate(Show show, Viewer viewer) {
            Policy policy = POLICIES.get(viewer.maturity());
            if (policy == null) throw new IllegalArgumentException("unknown maturity");
            boolean denied = (show.adult() && !policy.allowAdult())
                    || show.genres().stream().anyMatch(policy.blockedGenres()::contains);
            return denied ? new Decision(false, "MATURITY_BLOCKED", "hidden") : null;
        }
    }

    public static final class PremiumContentRule extends AccessRule {
        private static final int MIN_TIER = 3;

        @Override
        protected Decision evaluate(Show show, Viewer viewer) {
            return show.premium() && viewer.planTier() < MIN_TIER
                    ? new Decision(false, "PREMIUM_REQUIRED", "locked") : null;
        }
    }

    /** Links the rules in the application order and returns the head. */
    public static AccessRule contentAccessChain() {
        List<AccessRule> rules = List.of(new RegionRule(), new MaturityRule(), new PremiumContentRule());
        for (int i = 0; i + 1 < rules.size(); i++) rules.get(i).setNext(rules.get(i + 1));
        return rules.get(0);
    }
}
