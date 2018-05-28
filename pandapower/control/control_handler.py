import pandapower as pp
import pandas as pd
import copy
import matplotlib.pyplot as plt


class ControlHandler(object):
    """
    The control handler is responsible to manage all steps
    which are needed to perform the controlling of network elements
    """

    def __init__(self, net, timeseries, max_iterations=100):
        """
        Initialize all relevant variables
        """
        self.net = net
        self.controller_list = []
        self.timeseries = timeseries
        self.initial_load_p_kw = copy.deepcopy(net.load.p_kw.values)
        self.initial_sgen_p_kw = copy.deepcopy(net.sgen.p_kw.values)
        self.max_iterations = max_iterations
        self.logged_values = pd.DataFrame(0,
                                       columns=["max_voltage_pu", "min_voltage_pu",
                                                "max_loading_percent"],
                                       index=timeseries.index)

    def add_controller(self, controller):
        """
        Adds a controller to the control handler list
        """
        self.controller_list.append(controller)

    def run_timeseries(self):
        """
        Run the actual timeseries simulation
        """

        # If no controller preset: stop simulation
        if not self.controller_list:
            print("No controller specified!")
            return

        # If no time series present: stop simulation
        if self.timeseries is None:
            print("No timeseries specified!")
            return

        # Simulate each time step in the time series
        for timestep in self.timeseries.index:
            print("timestep: ", timestep)

            # Get the active power scalings for the current time step and initialize all
            # sgens and loads
            load_scaling = self.timeseries["P_load"].loc[timestep]
            sgen_scaling = self.timeseries["P_sgen"].loc[timestep]
            self.net.load.p_kw = self.initial_load_p_kw * load_scaling
            self.net.sgen.p_kw = self.initial_sgen_p_kw * sgen_scaling

            # Initialize the control of all controllers
            for controller in self.controller_list:
                controller.initialize_control()

            # Iterate through all controllers in the controller list and stop if all controller
            # have converged or the iteration count reached its maximum
            iterations = 0
            all_converged = False
            while not all_converged:
                if iterations > self.max_iterations:
                    print("Maximum iterations exceeded, stopping control loop!")
                    self.stopped += 1
                    break

                pp.runpp(self.net)
                all_converged = True
                for controller in self.controller_list:
                    if not controller.is_converged():
                        controller.control_step()
                        all_converged = False
                iterations += 1
            self.log_values(timestep)

    def log_values(self, timestep):
        """
        Log the extremums of line loadings and bus voltages
        """
        max_loading_percent = self.net.res_line.loading_percent.max()
        max_voltage_pu = self.net.res_bus.vm_pu.max()
        min_voltage_pu = self.net.res_bus.vm_pu.min()
        self.logged_values.loc[timestep, ["max_loading_percent", "max_voltage_pu", "min_voltage_pu"]] = \
                                (max_loading_percent, max_voltage_pu, min_voltage_pu)

    def plot_results(self):
        """
        Plot the logged results
        """
        x_axis = self.timeseries.index
        max_loading_results = self.logged_values.max_loading_percent
        max_voltage_results = self.logged_values.max_voltage_pu
        min_voltage_results = self.logged_values.min_voltage_pu

        plt.close("all")
        plt.figure(1)
        plt.plot(x_axis, max_loading_results)
        plt.xlabel("Timestep")
        plt.ylabel("Maximum line loading [%]")
        plt.figure(2)
        plt.plot(x_axis, max_voltage_results)
        plt.xlabel("Timestep")
        plt.ylabel("Maximum bus voltage [pu]")
        plt.figure(3)
        plt.plot(x_axis, min_voltage_results)
        plt.xlabel("Timestep")
        plt.ylabel("Minimum bus voltage [pu]")





