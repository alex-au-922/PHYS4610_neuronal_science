import yaml
class NeuronNetwork:
    def __init__(self):
        with open('constants.yaml') as stream:
            self.arg = yaml.safe_load(stream)[self.__class__.__name__]
        print(self.arg)
        
if __name__ == "__main__":
    obj = NeuronNetwork()