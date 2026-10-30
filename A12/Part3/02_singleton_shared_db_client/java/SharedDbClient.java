import java.util.Set;

/** Singleton: Shared Prisma Database Client (globalThis holder that survives hot reloads). */
public final class SharedDbClient {
    private SharedDbClient() {}

    private static final Set<String> ENVS = Set.of("development", "test", "production");

    /** Stand-in for PrismaClient; counts how many instances the process created. */
    public static final class DatabaseClient {
        DatabaseClient(ProcessGlobals process) {
            process.constructed++;
        }
    }

    /** Process-wide state that outlives module re-evaluation (globalThis). */
    public static final class ProcessGlobals {
        DatabaseClient prisma;
        int constructed;

        public int constructed() {
            return constructed;
        }
    }

    /** One evaluation of db.ts. */
    public static final class DbModule {
        private final DatabaseClient prisma;

        public DbModule(ProcessGlobals process, String nodeEnv) {
            if (!ENVS.contains(nodeEnv)) throw new IllegalArgumentException("invalid NODE_ENV");
            prisma = process.prisma != null ? process.prisma : new DatabaseClient(process);
            if (!nodeEnv.equals("production")) process.prisma = prisma;
        }

        public DatabaseClient prisma() {
            return prisma;
        }
    }
}
