from bootstrap import *

from engine import TransmissionMedium
from protocols import LPDQNode, LPDQBaseStation
import simpy
from random_mock import RandomMock

def test(env, nodes, bs):
    # using the example in paper
    # http://ieeexplore.ieee.org/xpls/icp.jsp?arnumber=7457611
    # setting up the random seeds
    nodes[0].random = RandomMock([0, 0, 0])
    nodes[1].random = RandomMock([0, 0, 2])
    nodes[2].random = RandomMock([0, 1, 1])
    nodes[3].random = RandomMock([0, 1, 0])
    nodes[4].random = RandomMock([1])
    nodes[5].random = RandomMock([2, 0])
    nodes[6].random = RandomMock([2, 2])

    for i in range(7):
        nodes[i].send("", nodes[i].MTU)

    def on_receive(packet):
        payload = packet.payload
        id = packet.id 
        if type(payload) == str:
            if id == 5:
                assert abs(env.now - 1.8) < 0.1
            elif id == 6:
                assert abs(env.now - 3.8) < 0.1
            elif id == 7:
                assert abs(env.now - 4.8) < 0.1
            elif id == 1:
                assert abs(env.now - 5.8) < 0.1
            elif id == 2:
                assert abs(env.now - 6.8) < 0.1
            elif id == 4:
                assert abs(env.now - 7.8) < 0.1
            elif id == 3:
                assert abs(env.now - 8.8) < 0.1

    bs.on_receive += on_receive

    yield env.timeout(10)

def main():
    env = simpy.Environment()
    rates = [30]
    slot_t = 0.1
    feedback_t = 0.1

    random_list = range(10)

    t = TransmissionMedium(env)
    bs = LPDQBaseStation(0, env, 0, 3, rates=rates, jitter_range = 0.0001, feedback_t = feedback_t, slot_t = slot_t)
    t.add_device(bs)
    nodes = []
    TOTAL = 10
    for i in range(1, TOTAL + 1):
        node = LPDQNode(i, env, feedback_t = feedback_t, slot_t = slot_t, m=3, rates = rates, guard = 0.01, seed = i, jitter_range = 0.001)
        t.add_device(node)
        nodes.append(node)
    env.process(test(env, nodes, bs))
    
    env.run(until=20)

if __name__ == "__main__":
    main()
