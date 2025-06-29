# test_plugins.py
from cml.CML_B import PluginManager
import cml

mgr = PluginManager(cml)

print("=== Všechny načtené pluginy podle názvu ===")
for name in mgr.plugins:
    print(f"• {name} (kat. {mgr.plugins[name]['category']})")

print("\n=== Pluginy v kategorii M ===")
for info in mgr.search_by_category('M'):
    print(f"• {info['name']} → funkce: {info['functions']}")

print("\n=== Pluginy v kategorii Q ===")
for info in mgr.search_by_category('Q'):
    print(f"• {info['name']} → funkce: {info['functions']}")
