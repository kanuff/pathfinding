class Space:
    def __init__(self, x, y):

        # I wanted this class to be as minimal as possible to make it easier to adapt to different algorithms
        # For this project which uses A*, initializing each space with the appropriate attributes and scores
        # happens when we construct the simulator

        self.pos = [x, y]

    def show(self):         #  This method used for debugging to inspect what was defined on each Space instance
        for attr in vars(self):
            print("Space.{0} = {1}".format(attr, getattr(self, attr)))