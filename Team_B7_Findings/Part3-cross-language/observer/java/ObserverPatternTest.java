import java.util.List;

public class ObserverPatternTest {

    public static void main(String[] args) {
        testAllObserversReceiveFirstEvent();
        testUnsubscribedObserverMissesSecondEvent();
        testEventValuesArePreserved();
        System.out.println("Observer Java: 3 tests passed");
    }

    private static void testAllObserversReceiveFirstEvent() {
        var setup = new Setup();
        setup.publisher.publish(new ObserverPattern.Event("STOCK_LOW"));

        check(setup.one.getReceivedEvents().size() == 1, "observer 1 should receive first event");
        check(setup.two.getReceivedEvents().size() == 1, "observer 2 should receive first event");
        check(setup.three.getReceivedEvents().size() == 1, "observer 3 should receive first event");
    }

    private static void testUnsubscribedObserverMissesSecondEvent() {
        var setup = new Setup();
        setup.publisher.publish(new ObserverPattern.Event("STOCK_LOW"));
        setup.publisher.unsubscribe(setup.two);
        setup.publisher.publish(new ObserverPattern.Event("STOCK_REPLENISHED"));

        check(setup.one.getReceivedEvents().size() == 2, "observer 1 should receive both events");
        check(setup.two.getReceivedEvents().size() == 1, "observer 2 should miss second event");
        check(setup.three.getReceivedEvents().size() == 2, "observer 3 should receive both events");
    }

    private static void testEventValuesArePreserved() {
        var setup = new Setup();
        var low = new ObserverPattern.Event("STOCK_LOW");
        var replenished = new ObserverPattern.Event("STOCK_REPLENISHED");
        setup.publisher.publish(low);
        setup.publisher.unsubscribe(setup.two);
        setup.publisher.publish(replenished);

        check(types(setup.one.getReceivedEvents()).equals(List.of("STOCK_LOW", "STOCK_REPLENISHED")),
                "observer 1 event values");
        check(types(setup.two.getReceivedEvents()).equals(List.of("STOCK_LOW")), "observer 2 event values");
        check(types(setup.three.getReceivedEvents()).equals(List.of("STOCK_LOW", "STOCK_REPLENISHED")),
                "observer 3 event values");
        check(setup.one.getReceivedEvents().get(0) == low, "event object should be forwarded unchanged");
    }

    private static List<String> types(List<ObserverPattern.Event> events) {
        return events.stream().map(ObserverPattern.Event::getType).toList();
    }

    private static void check(boolean condition, String message) {
        if (!condition) {
            throw new AssertionError(message);
        }
    }

    private static final class Setup {
        final ObserverPattern.Publisher publisher = new ObserverPattern.Publisher();
        final ObserverPattern.RecordingObserver one = new ObserverPattern.RecordingObserver();
        final ObserverPattern.RecordingObserver two = new ObserverPattern.RecordingObserver();
        final ObserverPattern.RecordingObserver three = new ObserverPattern.RecordingObserver();

        Setup() {
            publisher.subscribe(one);
            publisher.subscribe(two);
            publisher.subscribe(three);
        }
    }
}
