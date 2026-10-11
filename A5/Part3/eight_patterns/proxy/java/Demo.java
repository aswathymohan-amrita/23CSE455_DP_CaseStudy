import java.util.*;
public class Demo {
    interface DataSource {
        String fetch(String id);
    }
    static class Source implements DataSource {
        int calls=0;
        public String fetch(String id) {
            calls++;
            return id;
        }
    }
    static class Proxy implements DataSource {
        DataSource s;
        Map<String,String> cache=new HashMap<>();
        Proxy(DataSource s) {
            this.s=s;
        }
        public String fetch(String id) {
            return cache.computeIfAbsent(id,s::fetch);
        }
        void invalidate(String id) {
            cache.remove(id);
        }
    }
    public static void main(String[]a) {
        Source s=new Source();
        Proxy p=new Proxy(s);
        p.fetch("P1");
        p.fetch("P1");
        if(s.calls!=1)throw new AssertionError();
        p.invalidate("P1");
        p.fetch("P1");
        if(s.calls!=2)throw new AssertionError();
    }
}
