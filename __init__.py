from compiler import compileModuleDefs
from vm import RealtimeVM

def runSimpleRT(source):
    compiled = compileModuleDefs(source, {})
    vm = RealtimeVM(compiled)
    vm.run()

def runModule(name, modules={}):

    namespace = {}    

    def compileModule(moduleName, prefix=""):
        moduleUses, moduleContents = modules[moduleName]
        for use_name, use_as in moduleUses:
           compileModule(use_name, use_as)
        moduleDefs = compileModuleDefs(moduleContents, namespace)
        
        if prefix != "":
            prefix = prefix + "."
        for m_def, m_impl in moduleDefs.items():
    
