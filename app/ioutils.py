import yaml, os

def loadYaml(fp):
    with open(fp, encoding='utf8') as f:
        text = f.read()
        return yaml.load(text, yaml.SafeLoader)
    
def saveYaml(fp, model):
    ymlStr = yaml.dump(model, default_flow_style = False, allow_unicode = True, encoding = None)
    with open(fp, 'w', encoding='utf8') as f:
        f.write( ymlStr )

def loadText(fp):
    with open(fp, encoding='utf8') as f:
        return f.read()
        

def writeText(fp, text):
    with open(fp, 'w', encoding='utf8') as f:
        f.write(text)
        f.close()
        
def serialize(obj):
    if obj == None:
        return None
        
    if isinstance(obj, list) or isinstance(obj, tuple):
        result = []
        for x in obj:
            result += [serialize(x)]
        return result
    
    if isinstance(obj, dict):
        result = {}
        for key in obj.keys():
            result[key] = serialize(obj[key])
        return result
    
    if isinstance(obj, str) or isinstance(obj, int) or isinstance(obj, float):
        return obj

    return serialize(obj.__dict__)