from pandapower.control import Controller

class Central_PV_Controller(Controller):
    def __init__(self, net, max_loading_percent=100):
        self.net = net
        self.max_loading_percent = max_loading_percent

    def initialize_control(self):
        # enable all sgens at the beginning of each timestep
        self.net.sgen.in_service = True

    def is_converged(self):
        # Check whether the maximum loading of any line is exceeded
        overloaded_lines = self.net.line.index[self.net.res_line.loading_percent > self.max_loading_percent]
        if len(overloaded_lines) > 0:
            return False
        else:
            return True

    def control_step(self):
        # Disable the sgen with the hightest feed in which is in service
        in_service_sgens = self.net.sgen[self.net.sgen.in_service]
        sgen_with_highest_feed_in = in_service_sgens.p_kw.sort_values().index[0]
        self.net.sgen.in_service.loc[sgen_with_highest_feed_in] = False

