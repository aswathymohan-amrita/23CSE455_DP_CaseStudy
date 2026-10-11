import unittest

from observer import Event, Publisher, RecordingObserver


class ObserverPatternTests(unittest.TestCase):
    def setUp(self) -> None:
        self.publisher = Publisher()
        self.observers = [RecordingObserver() for _ in range(3)]
        for observer in self.observers:
            self.publisher.subscribe(observer)

    def test_all_observers_receive_first_event(self) -> None:
        self.publisher.publish(Event("STOCK_LOW"))
        self.assertEqual([len(observer.received_events) for observer in self.observers], [1, 1, 1])

    def test_unsubscribe_excludes_observer_from_second_event(self) -> None:
        self.publisher.publish(Event("STOCK_LOW"))
        self.publisher.unsubscribe(self.observers[1])
        self.publisher.publish(Event("STOCK_REPLENISHED"))
        self.assertEqual([len(observer.received_events) for observer in self.observers], [2, 1, 2])

    def test_event_values_and_object_are_preserved(self) -> None:
        low = Event("STOCK_LOW")
        replenished = Event("STOCK_REPLENISHED")
        self.publisher.publish(low)
        self.publisher.unsubscribe(self.observers[1])
        self.publisher.publish(replenished)
        self.assertEqual(
            [[event.type for event in observer.received_events] for observer in self.observers],
            [["STOCK_LOW", "STOCK_REPLENISHED"], ["STOCK_LOW"], ["STOCK_LOW", "STOCK_REPLENISHED"]],
        )
        self.assertIs(self.observers[0].received_events[0], low)


if __name__ == "__main__":
    unittest.main()
