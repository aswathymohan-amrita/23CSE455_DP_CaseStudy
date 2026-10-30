import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Proxy;
import java.util.Map;

/** Proxy (protection): Environment Secret Guard. */
public final class EnvGuard {
    private EnvGuard() {}

    /** Subject. */
    public interface Env {
        /** Value of the variable, or null when it is not set. */
        String get(String name);
    }

    /** RealSubject: validated variables. */
    public record RealEnv(Map<String, String> vars) implements Env {
        public String get(String name) {
            return vars.get(name);
        }
    }

    /** Creates a dynamic proxy that refuses server-only variables on the client. */
    public static Env guard(Env real, boolean isServer, boolean production) {
        InvocationHandler handler = (proxy, method, args) -> {
            String name = (String) args[0];
            if (!isServer && !name.startsWith("NEXT_PUBLIC_")) {
                throw new IllegalStateException(production
                        ? "Attempted to access a server-side environment variable on the client"
                        : "Attempted to access server-side environment variable '" + name + "' on the client");
            }
            return method.invoke(real, args);
        };
        return (Env) Proxy.newProxyInstance(Env.class.getClassLoader(), new Class<?>[] {Env.class}, handler);
    }
}
