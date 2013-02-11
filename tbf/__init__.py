from compiler import compileModuleDefs
from vm import RealtimeVM, SimulationVM

def compileSimple(source):
    return compileModuleDefs(source, {})

def compileModule(name, modules={}):

    namespace = {}    

    def compileM(moduleName, prefix=u""):
        moduleUses, moduleContents = modules[moduleName]
        for use_as, use_name in moduleUses:
           compileM(use_name, use_as)
        moduleDefs = compileModuleDefs(moduleContents, namespace)
        
        if prefix != u"":
            prefix = prefix + u"."
        for m_def, m_impl in moduleDefs.items():
            namespace[prefix+m_def] = m_impl
    
    compileM(name)
    
    return namespace 

def runRT(compiled):
    vm = RealtimeVM(compiled)
    vm.run()

def runSimul(compiled):
    vm = SimulationVM(compiled)
    vm.run()
