class Controller(object):
    def __init__(self):
        """
        This init method is used to initialize all needed properties of the controller.
        It is called once when the controller is created.
        """
        pass

    def initialize_control(self):
        """
        This method is called once at the beginning of each timestep and can be used to set or
        reset relevant values before the control starts.
        """
        pass

    def control_step(self):
        """
        This is the actual control step. It is used to adapt values of the controlled elements.
        """
        pass

    def is_converged(self):
        """
        This method is used to determine if the controller is converged or not.
        """
        print("Method is_converged() has not been overwritten and will always return True!")
        return True
