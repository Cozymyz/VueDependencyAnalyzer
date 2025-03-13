from typing import Dict, List

class DependencyGraph:
    def __init__(self, data: dict):
        self.components: Dict[str, List[str]] = data["components"]
        self.modules: Dict[str, List[str]] = data["modules"]

    def find_unused_modules(self) -> List[str]:
        """find unused modules"""
        used_modules = set()
        for deps in self.components.values():
            used_modules.update(deps)
        return [m for m in self.modules if m not in used_modules]

    def detect_circular_deps(self) -> List[List[str]]:
        """detect_circular_dependencies"""
        graph = {**self.modules, **self.components}
        visited = set()
        rec_stack = set()
        cycles = []

        def dfs(node, path):
            if node in rec_stack:
                cycles.append(path[path.index(node):] + [node])
                return
            if node in visited:
                return
            visited.add(node)
            rec_stack.add(node)
            for neighbor in graph.get(node, []):
                dfs(neighbor, path + [node])
            rec_stack.remove(node)

        for node in graph:
            dfs(node, [])

        return cycles