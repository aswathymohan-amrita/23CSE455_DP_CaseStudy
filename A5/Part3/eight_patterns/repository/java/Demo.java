import java.util.*;
public class Demo {
    record Patient(String id,String name) {
    }
    interface Repo {
        void save(Patient p);
        Patient find(String id);
    }
    static class Memory implements Repo {
        Map<String,Patient> rows=new HashMap<>();
        public void save(Patient p) {
            rows.put(p.id(),p);
        }
        public Patient find(String id) {
            return rows.get(id);
        }
    }
    static class Registry {
        Repo r;
        Registry(Repo r) {
            this.r=r;
        }
        void register(Patient p) {
            r.save(p);
        }
        Patient lookup(String id) {
            return r.find(id);
        }
    }
    public static void main(String[]a) {
        Registry r=new Registry(new Memory());
        r.register(new Patient("P1","Demo"));
        if(!r.lookup("P1").name().equals("Demo")||r.lookup("none")!=null)throw new AssertionError();
    }
}
