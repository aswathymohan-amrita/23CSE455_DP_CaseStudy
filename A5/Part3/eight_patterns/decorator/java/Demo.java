public class Demo {
    interface Reader {
        String read(String id);
    }
    static class Base implements Reader {
        public String read(String id) {
            return id;
        }
    }
    static class Audited implements Reader {
        Reader inner;
        int reads=0;
        Audited(Reader inner) {
            this.inner=inner;
        }
        public String read(String id) {
            String r=inner.read(id);
            reads++;
            return r;
        }
    }
    public static void main(String[]a) {
        Audited r=new Audited(new Base());
        if(!r.read("P1").equals("P1")||r.reads!=1)throw new AssertionError();
    }
}
