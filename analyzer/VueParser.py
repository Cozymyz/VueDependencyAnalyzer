import os
import ast
import re
from typing import Dict, Set

class VueParser:
    def __init__(self, project_path: str):
        self.project_path = project_path
        self.component_deps: Dict[str, Set[str]] = {}
        self.module_deps: Dict[str, Set[str]] = {}

    def analyz(self):
        """Entry Method: Start analysis process"""
        self._analyze_components()
        self._analyze_modules()
        return {
            "components": {k: list(v) for k, v in self.component_deps.items()},
            "modules": {k: list(v) for k, v in self.module_deps.items()}
        }

    def _analyze_components(self):
        """Analyze component directory"""
        components_dir = os.path.join(self.project_path, "src/View")
        for root, _, files in os.walk(components_dir):
            for file in files:
                if not file.endswith(".vue"):
                    continue
                file_path = os.path.join(root, file)
                component_name = os.path.splitext(file)[0]
                self.component_deps[component_name] = self._parse_vue_file(file_path)

    def _analyze_modules(self):
        """Analyze vuex module directory"""
        modules_dir = os.path.join(self.project_path, "src/store/modules")
        for root, _, files in os.walk(modules_dir):
            for file in files:
                if not file.endswith(".js"):
                    continue
                file_path = os.path.join(root, file)
                modules_name = os.path.splitext(file)[0]
                self.module_deps[modules_name] = self._parse_js_file(file_path)

    def _parse_vue_file(self, file_path: str) -> Set[str]:
        """Analyze single vue file"""
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        dependencies = set()

        # import stm
        import_pattern = re.compile(r"import\s+.+\s+from\s+['\"](.+?store/modules/(.+?))['\"]")
        matches = import_pattern.findall(content)
        for _, module_path in matches:
            module_name = module_path.split("/")[-1].replace(".js", "")
            dependencies.add(module_name)
        # tree = ast.parse(content)
        # for node in ast.walk(tree):
        #     if isinstance(node, ast.ImportFrom) and "store/modules" in node.module:
        #         module_name = node.module.split(".")[-1]
        #         dependencies.add(module_name)

        # store stm
        store_pattern = re.compile(r"this\.\$store\.state\.(\w+)")
        matches = store_pattern.findall(content)
        dependencies.update(matches)

        # lines = content.split("\n")
        # for line in lines:
        #     if "this.$store.state." in line:
        #         parts = line.split(".")
        #         if len(parts) >= 4:
        #             dependencies.add(parts[3])

        return dependencies

    def _parse_js_file(self, file_path: str) -> Set[str]:
        """Analyze single js file"""
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        dependencies = set()
        # tree = ast.parse(content)
        #
        # for node in ast.walk(tree):
        #     if isinstance(node, ast.ImportFrom) and "store/modules" in node.module:
        #         module_name = node.module.split(".")[-1]
        #         dependencies.add(module_name)

        import_pattern = re.compile(r"import\s+.+\s+from\s+['\"](.+?store/modules/(.+?))['\"]")
        matches = import_pattern.findall(content)
        for _, module_path in matches:
            module_name = module_path.split("/")[-1].replace(".js", "")
            dependencies.add(module_name)

        return dependencies