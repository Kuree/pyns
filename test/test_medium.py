if __name__ == '__main__' and __package__ is None:
   from os import sys, path
   sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


from engine import TransmissionMedium
import simpy
from engine import Device

if __name__ == "__main__":
    TEST_MESSAGE1 = "TEST1"
    TEST_MESSAGE2 = "TEST2"
    def listen(packet):
        assert packet.payload == TEST_MESSAGE1

    env = simpy.Environment()

    def test():
        t = TransmissionMedium(env)
        d1 = Device(1)
        d2 = Device(2)
        d1.on_receive = listen
        t.add_device(d1)
        t.add_device(d2)
        d1._send(TEST_MESSAGE1, 1)
        yield env.timeout(1)
        assert env.now == 1
        assert t.is_busy() == False
        d1.sleep()
        d1._send(TEST_MESSAGE2, 2)
        yield env.timeout(1)
        assert env.now == 2
        assert t.is_busy() == True
        yield env.timeout(1)
        assert env.now == 3
        assert t.is_busy() == False
        d1._send(TEST_MESSAGE1, 2)
        yield env.timeout(1)
        d2.wake_up()
        d2._send(TEST_MESSAGE1, 2)
        yield env.timeout(1)
        assert env.now == 5
        assert t.is_busy() == True
        yield env.timeout(1)
        assert t.is_busy() == False
    env.process(test())
    env.run(until=10)

