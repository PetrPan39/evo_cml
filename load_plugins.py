"""
load_plugins.py

Standalone orchestrator to dynamically discover, import, and assign plugin classes
from the cml package without modifying CML_A.py.
"""
import importlib
from cml.CML_B import PluginManager


def load_plugins():
    """Discover plugin classes by category."""
    mgr = PluginManager()
    plugin_classes = {}
    for category in ['A', 'B', 'C', 'Q', 'M']:
        plugin_classes[category] = {}
        for info in mgr.search_by_category(category):
            module_name = info['module_name']
            cls_name = info['name']
            # Dynamically import the plugin module
            module = importlib.import_module(f"cml.{module_name}")
            # Retrieve the class by friendly name
            cls = getattr(module, cls_name)
            plugin_classes[category][cls_name] = cls
    return plugin_classes


if __name__ == '__main__':
    plugins = load_plugins()
    for cat, classes in plugins.items():
        print(f"Category {cat}:")
        if classes:
            for name, cls in classes.items():
                print(f"  {name}: {cls}")
        else:
            print("  (none)")
