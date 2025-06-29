import importlib
import pkgutil
from typing import Dict, List, Any

class PluginManager:
    """
    PluginManager for CML – scans modules in cml/ package (excluding CML_A and CML_B)
    and categorizes them by PLUGIN_CATEGORY: A, B, C, Q, M.
    """
    def __init__(self, package=None):
        if package is None:
            import cml
            self.package = cml
        else:
            self.package = package

        self.plugins: Dict[str, Dict[str, Any]] = {}
        self.categories: Dict[str, List[Dict[str, Any]]] = {c: [] for c in ['A','B','C','Q','M']}
        self.index_plugins()

    def index_plugins(self):
        """
        Discover all modules in the self.package path, skipping CML_A and CML_B,
        and register those defining PLUGIN_CATEGORY in valid categories.
        """
        for finder, module_name, ispkg in pkgutil.iter_modules(self.package.__path__):
            if module_name in ('CML_A', 'CML_B'):
                continue
            full_name = f"{self.package.__name__}.{module_name}"
            try:
                mod = importlib.import_module(full_name)
                cat = getattr(mod, 'PLUGIN_CATEGORY', None)
                if cat in self.categories:
                    pname = getattr(mod, 'PLUGIN_NAME', module_name)
                    tags  = getattr(mod, 'PLUGIN_TAGS', [])
                    funcs = [attr for attr in dir(mod) if callable(getattr(mod, attr)) and not attr.startswith('_')]
                    info = {
                        'module': mod,
                        'name': pname,
                        'category': cat,
                        'tags': tags,
                        'functions': funcs,
                    }
                    self.plugins[pname] = info
                    self.categories[cat].append(info)
            except Exception as e:
                print(f"[PluginManager] Chyba pri nacitani {full_name}: {e}")

    def search_by_name(self, name: str) -> Dict[str, Any]:
        """Return plugin info by exact name."""
        return self.plugins.get(name)

    def search_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Return list of plugins in a given category."""
        return self.categories.get(category, [])

    def search_by_tag(self, tag: str) -> List[Dict[str, Any]]:
        """Return plugins matching a specific tag."""
        return [info for info in self.plugins.values() if tag in info['tags']]

    def search_by_function(self, func: str) -> List[Dict[str, Any]]:
        """Return plugins exposing a given function name."""
        return [info for info in self.plugins.values() if func in info['functions']]
