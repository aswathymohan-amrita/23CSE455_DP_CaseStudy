import java.util.*;
public class Demo {
    interface Store {
        int save(String p,String d);
    }
    static class Memory implements Store {
        int n=0;
        public int save(String p,String d) {
            return ++n;
        }
    }
    interface Notice {
        void send(String p,String m);
    }
    static class Recorder implements Notice {
        int n=0;
        public void send(String p,String m) {
            n++;
        }
    }
    static class Facade {
        Store s;
        Notice n;
        Facade(Store s,Notice n) {
            this.s=s;
            this.n=n;
        }
        int book(String p,String d) {
            if(p.isEmpty()||d.isEmpty())throw new IllegalArgumentException();
            int id=s.save(p,d);
            n.send(p,""+id);
            return id;
        }
    }
    public static void main(String[]a) {
        Memory s=new Memory();
        Recorder n=new Recorder();
        if(new Facade(s,n).book("P1","D1")!=1||n.n!=1)throw new AssertionError();
    }
}
