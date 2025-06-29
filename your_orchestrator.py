# your_orchestrator.py (nebude to CML_A.py, ten zůstává beze změny)

from cml.CML_B import PluginManager

def main():
    mgr = PluginManager()
    # načti pluginy jednotlivých kategorií
    plugins_A = mgr.search_by_category('A')
    plugins_B = mgr.search_by_category('B')
    plugins_C = mgr.search_by_category('C')
    plugins_Q = mgr.search_by_category('Q')
    plugins_M = mgr.search_by_category('M')

    print("Kategorie A:", [p['name'] for p in plugins_A])
    print("Kategorie B:", [p['name'] for p in plugins_B])
    print("Kategorie C:", [p['name'] for p in plugins_C])
    print("Kategorie Q:", [p['name'] for p in plugins_Q])
    print("Kategorie M:", [p['name'] for p in plugins_M])

    # dále s nimi můžete pracovat, třeba instanciovat CloudMemoryManager:
    # cm_info = plugins_M[0]
    # CM = cm_info['module'].CloudMemoryManager(...)
    # ...

if __name__ == "__main__":
    main()
