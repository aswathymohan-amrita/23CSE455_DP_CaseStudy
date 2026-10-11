import java.util.*;
public class Demo {
    interface Gateway {
        String order(String p,String t);
    }
    static class Vendor {
        Map<String,Object> last;
        String submit(Map<String,Object> p) {
            last=p;
            return "LAB-1";
        }
    }
    static class Adapter implements Gateway {
        Vendor v;
        Adapter(Vendor v) {
            this.v=v;
        }
        public String order(String p,String t) {
            if(p.isEmpty()||t.isEmpty())throw new IllegalArgumentException();
            return v.submit(Map.of("patient",Map.of("id",p),"test",Map.of("code",t)));
        }
    }
    public static void main(String[]a) {
        Vendor v=new Vendor();
        if(!new Adapter(v).order("P1","CBC").equals("LAB-1")||v.last==null)throw new AssertionError();
    }
}
