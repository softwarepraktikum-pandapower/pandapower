import pandapower as pp
from pandapower.control import Controller

class overvoltage_protection_controller(Controller):
    def __init__(self, net, sgen_idx, max_vm_pu):
        self.net = net
        self.sgen_idx = sgen_idx
        self.max_vm_pu = max_vm_pu
        self.sgen_bus = net.sgen.bus.loc[sgen_idx]

    def initialize_control(self):
        # enable the controlled sgen at the beginning of each timestep
        self.net.sgen.in_service.loc[self.sgen_idx] = True

    def is_converged(self):
        # Check whether the bus voltage of the specified sgen exceeds the maximum voltage limit
        if self.net.res_bus.vm_pu.loc[self.sgen_bus] > self.max_vm_pu:
            return False
        else:
            return True

    def control_step(self):
        # Disable the sgen
        self.net.sgen.in_service.loc[self.sgen_idx] = False

