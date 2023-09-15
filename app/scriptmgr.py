import ioutils, os
class ScriptManager:
    def loadScript(self, key:str):
        fp = f'..\\scripts\\{key}.py'
        if os.path.exists(fp):
            return ioutils.loadText(fp)
        return None
    
    def saveScript(self, key:str, script:str):
        fp = f'..\\scripts\\{key}.py'
        ioutils.writeText(fp, script)

    def getScriptList(self):
        files = os.listdir('..\\scripts')    
        ls = []
        for f in files:
            if f.endswith('.py'):
                id = f[:-3]
                fp = os.path.join('..\\scripts', f)
                method = 'get'
                requireBody = False
                endpoint = id 
                if f.startswith('postBody'):
                    method = 'post'
                    requireBody = True
                    endpoint = endpoint[9:].replace('_', '/')
                else:
                    endpoint = endpoint[4:].replace('_', '/')
                ls += [{'id': id, 'path': fp, 'method': method, 'requireBody': requireBody, 'endpoint': endpoint}]
        return ls