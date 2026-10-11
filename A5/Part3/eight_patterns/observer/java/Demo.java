import java.util.*;
public class Demo {
    interface Observer {
        void update(String event);
    }
    static class Audit implements Observer {
        List<String> events=new ArrayList<>();
        public void update(String e) {
            events.add(e);
        }
    }
    static class Publisher {
        Set<Observer> observers=new HashSet<>();
        void subscribe(Observer o) {
            observers.add(o);
        }
        void unsubscribe(Observer o) {
            observers.remove(o);
        }
        void publish(String e) {
            for(Observer o:observers)o.update(e);
        }
    }
    public static void main(String[]a) {
        Publisher p=new Publisher();
        Audit o=new Audit();
        p.subscribe(o);
        p.publish("lab.ready");
        p.unsubscribe(o);
        p.publish("other");
        if(o.events.size()!=1||!o.events.get(0).equals("lab.ready"))throw new AssertionError();
    }
}
