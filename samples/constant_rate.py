from pyns.protocols import create_basestation, create_node, ProtocolType
from pyns.engine import Simulator, SimArg, TraceFormatter, TransmissionMedium
import logging
import numpy
import sys
import random
import os

class ConstantSimulator(Simulator):
    def __init__(self, total_time, use_seed, num_nodes, protocol_type, log_prefix):
        super().__init__(total_time)
        self.use_seed = use_seed
        self.num_nodes = num_nodes
        self.protocol_type = protocol_type
        self.log_prefix = log_prefix


    def _run(self, env, pr):
        if self.use_seed:
            seeds = [i for i in range(self.num_nodes + 1)]
            numpy.random.seed(0)
            random.seed(0)
        else:
            seeds = [random.randint(0, self.num_nodes * 1000) for i in range(self.num_nodes + 1)]
        special_args = {"seed": seeds[0]}
        name = self.log_prefix + str(pr)
        t = TransmissionMedium(env, name)
        t.add_logger(name)
        bs = create_basestation(self.protocol_type, 0, env, "default.json", special_args)
        t.add_device(bs)
        
        nodes = []
        
        for i in range(self.num_nodes):
            special_arg = {"total": self.num_nodes, "scheduled_time": i, "seed": seeds[i]}
            n = create_node(self.protocol_type, i, env, "default.json", special_arg)
            nodes.append(n)
            t.add_device(n)


        rate = pr * len(nodes)
        dummy_payload = "Test"
        while True:
            num_of_trans = numpy.random.poisson(rate)
            nodes_to_trans = random.sample(nodes, num_of_trans)
            for n in nodes_to_trans:
                n.send(dummy_payload, n.MTU)
            sleep_time = numpy.random.uniform(0.5, 1.5)
            yield env.timeout(sleep_time)

def main():
    parser = SimArg("Simulation with constant packet rate")
    args = parser.parse_args()

    
    # setting up logger    
    total_time = args.sim_time
    use_seed = args.use_seed
    num_nodes = args.num_nodes
    #pr = args.packet_rate
    protocol_type = args.type

    log_prefix = "rate-"
    if args.test:
        rates = [1 / num_nodes]
        use_seed = True
    else:
        rates = [0.1 / num_nodes * i for i in range(1, 21)]

    sim = ConstantSimulator(total_time, use_seed, num_nodes, protocol_type, log_prefix)
        
    for rate in rates:
        name = log_prefix + str(rate)
        logger = logging.getLogger(name)
        if args.stdout or args.test:
            ch = logging.StreamHandler(sys.stdout)
        else:
            ch = logging.FileHandler(os.path.join("rate_log", str(protocol_type) + "-" + name))
        ch.setFormatter(TraceFormatter())
        ch.setLevel(logging.INFO)
        logger.addHandler(ch)
        
 
    sim.start(rates)
   



if __name__ == "__main__":
    main()
