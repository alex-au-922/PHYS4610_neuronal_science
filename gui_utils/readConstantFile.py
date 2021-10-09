import yaml

def readConstants():
    fileName = 'constants.yaml'
    with open(fileName) as stream:
        args = yaml.safe_load(stream)
    args = removeDuplicateConstants(args)
    return flattenConstants(args)

def removeDuplicateConstants(args):
    paramList = {}
    for key, dictionary in args.items():
        paramList.update(dictionary)
    return paramList

def flattenConstants(args):
    inhibitDict = args['INHIBIT']
    excitedDict = args['EXCITED']
    del args['INHIBIT']
    del args['EXCITED']
    newInhibitDict = {}
    for key, value in inhibitDict.items():
        newKey = 'INHIBIT_'+key
        newInhibitDict[newKey] = value
    newExcitedDict = {} 
    for key,value in excitedDict.items():
        newKey = 'EXCITED_'+key
        newExcitedDict[newKey] = value
    args.update(newInhibitDict)
    args.update(newExcitedDict)
    return args

if __name__ == "__main__":
    readConstants()
