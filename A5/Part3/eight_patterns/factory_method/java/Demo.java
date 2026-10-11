public class Demo {
    interface Exporter {
        String run(String id);
    }
    static class Json implements Exporter {
        public String run(String id) {
            return "{\"id\":\""+id+"\"}";
        }
    }
    static class Csv implements Exporter {
        public String run(String id) {
            return id+"\n";
        }
    }
    static abstract class Factory {
        abstract Exporter create();
        String exportRecord(String id) {
            return create().run(id);
        }
    }
    static class JsonFactory extends Factory {
        Exporter create() {
            return new Json();
        }
    }
    static class CsvFactory extends Factory {
        Exporter create() {
            return new Csv();
        }
    }
    public static void main(String[]a) {
        if(!new JsonFactory().exportRecord("P1").contains("P1")||!new CsvFactory().exportRecord("P1").equals("P1\n"))throw new AssertionError();
    }
}
