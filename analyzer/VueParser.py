import os
from typing import Dict, Set, List
from bs4 import BeautifulSoup
import esprima

class VueParser:
    def __init__(self, project_path: str):
        self.project_path = project_path
        self.component_deps: Dict[str, Set[str]] = {}
        self.module_deps: Dict[str, Set[str]] = {}
        self.module_aliases: Dict[str, str] = {}
        self.store_helpers: Dict[str, str] = {}

    def analyz(self):
        """Entry Method: Start analysis process"""
        self._parse_store_config()
        self._analyze_components()
        self._analyze_modules()
        return {
            "components": {
                comp: [self._resolve_alias(m) for m in mods]
                for comp, mods in self.component_deps.items()
            },
            "modules": {
                self._resolve_alias(m): deps
                for m, deps in self.module_deps.items()
            }
        }

    def _resolve_alias(self, module_name: str) -> str:
        """Resolving module aliases"""
        return self.module_aliases.get(module_name, module_name)

    def _parse_store_config(self):
        """Parsing Vuex Store configuration file"""
        store_index = os.path.join(self.project_path, "src/store/index.js")
        if not os.path.exists(store_index):
            return

        try:
            with open(store_index, "r", encoding="utf-8") as f:
                ast = esprima.parseScript(f.read(), {'tolerant': True})
        except Exception as e:
            print(f"Store config parse error: {store_index} - {e}")
            return

        # Building the import map
        import_map = {}
        for node in ast.body:
            if node.type == 'ImportDeclaration' and '/modules/' in node.source.value:
                for spec in node.specifiers:
                    alias = spec.local.name
                    module_path = node.source.value.split('/modules/')[-1].replace('.js', '')
                    import_map[alias] = module_path

        # Extract module registration information
        for node in ast.body:
            if node.type == 'VariableDeclaration':
                for decl in node.declarations:
                    if (decl.init and
                            decl.init.callee and
                            decl.init.callee.name == 'Vuex.Store'):
                        for prop in decl.init.arguments[0].properties:
                            if prop.key.name == 'modules':
                                for mod_prop in prop.value.properties:
                                    alias = mod_prop.key.name
                                    source = mod_prop.value.name
                                    if source in import_map:
                                        self.module_aliases[alias] = import_map[source]

    def _analyze_components(self):
        """Analyze component directory"""
        components_dir = os.path.join(self.project_path, "src/View")
        for root, _, files in os.walk(components_dir):
            for file in files:
                if file.endswith(".vue"):
                    file_path = os.path.join(root, file)
                    component_name = os.path.splitext(file)[0]
                    deps = self._parse_vue_file(file_path)
                    self.component_deps[component_name] = deps

    def _analyze_modules(self):
        """Analyze vuex module directory"""
        modules_dir = os.path.join(self.project_path, "src/store/modules")
        for root, _, files in os.walk(modules_dir):
            for file in files:
                if file.endswith(".js"):
                    file_path = os.path.join(root, file)
                    modules_name = os.path.splitext(file)[0]
                    self.module_deps[modules_name] = self._parse_js_file(file_path)

    def _parse_vue_file(self, file_path: str) -> Set[str]:
        """Analyze single vue file"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f.read(), "html.parser")
        except Exception as e:
            print(f"File read error: {file_path}: {e}")
            return set()

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        dependencies = set()

        # # import stm
        # import_pattern = re.compile(
        #     r"import\s+.*?from\s+['\"](.*?store/modules/(.+?))['\"]",
        #     re.DOTALL
        # )
        # # import_pattern = re.compile(r"import\s+.+\s+from\s+['\"](.+?store/modules/(.+?))['\"]")
        # matches = import_pattern.findall(content)
        # for _, module_path in matches:
        #     module_name = module_path.split("/")[-1].replace(".js", "")
        #     dependencies.add(module_name)
        # # tree = ast.parse(content)
        # # for node in ast.walk(tree):
        # #     if isinstance(node, ast.ImportFrom) and "store/modules" in node.module:
        # #         module_name = node.module.split(".")[-1]
        # #         dependencies.add(module_name)
        #
        # # store stm
        # store_pattern = re.compile(r"this\.\$store\.state\.(\w+)")
        # matches = store_pattern.findall(content)
        # dependencies.update(matches)
        #
        # # lines = content.split("\n")
        # # for line in lines:
        # #     if "this.$store.state." in line:
        # #         parts = line.split(".")
        # #         if len(parts) >= 4:
        # #             dependencies.add(parts[3])

        #useing libraries
        for script in soup.find_all("script"):
            if not script.string:
                continue

            try:
                # Parsing JavaScript code with esprima
                script_ast = esprima.parseScript(script.string, {
                    'jsx': True,
                    'tolerant': True
                })
            except Exception  as e:
                print(f"Script parsing error: {file_path} - {e}")
                continue

            # Multi-dimensional dependency detection
            dependencies.update(self._find_store_imports(script_ast))
            dependencies.update(self._find_store_references(script_ast))
            dependencies.update(self._detect_helper_usage(script_ast))


        return dependencies

    def _parse_js_file(self, file_path: str) -> Set[str]:
        """Analyze single js file"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                ast = esprima.parseScript(f.read(), {'tolerant': True})
        except Exception as e:
            print(f"JS parse error: {file_path}: {e}")
            return set()

        return self._find_store_imports(ast)

        # with open(file_path, "r", encoding="utf-8") as f:
        #     content = f.read()
        #
        # dependencies = set()
        # # tree = ast.parse(content)
        # #
        # # for node in ast.walk(tree):
        # #     if isinstance(node, ast.ImportFrom) and "store/modules" in node.module:
        # #         module_name = node.module.split(".")[-1]
        # #         dependencies.add(module_name)
        #
        # import_pattern = re.compile(
        #     r"import\s+.*?from\s+['\"](.*?store/modules/(.+?))['\"]",
        #     re.DOTALL
        # )
        # # import_pattern = re.compile(r"import\s+.+\s+from\s+['\"](.+?store/modules/(.+?))['\"]")
        # matches = import_pattern.findall(content)
        # for _, module_path in matches:
        #     module_name = module_path.split("/")[-1].replace(".js", "")
        #     dependencies.add(module_name)
        #
        # return dependencies

    def _find_store_imports(self, ast) -> Set[str]:
        """Locate all store module import statements"""
        imports = set()

        # AST traverser
        for node in ast.body:
            if node.type == 'ImportDeclaration' and '/modules/' in node.source.value:
                for spec in node.specifiers:
                    raw_name = node.source.value.split('/modules/')[-1].replace('.js', '')
                    imports.add(raw_name)

        return imports

    def _find_store_references(self, ast) -> Set[str]:
        """Accurately identify this.$store.state references"""
        modules = set()

        def traverse(node):
            if not node or not hasattr(node, 'type'):
                return

            # this.$store.state.moduleName
            if node.type == 'MemberExpression':
                try:
                    if (node.object.object.object.name == 'this' and
                        node.object.property.name == '$store' and
                        node.object.object.property.name == 'state'):
                        module_alias = node.property.name
                        modules.add(module_alias)
                except AttributeError:
                    pass

            # Handling auxiliary function arguments
            if node.type == 'CallExpression':
                try:
                    if node.callee.name in self.store_helpers.values():
                        for arg in node.arguments:
                            if arg.type == 'Literal' and isinstance(arg.value, str):
                                modules.add(arg.value)
                except AttributeError:
                    pass

            # Recursively traverse child nodes
            for child in self._get_children(node):
                traverse(child)

        traverse(ast)
        return modules

    def _detect_helper_usage(self, ast) -> Set[str]:
        """Detecting the use of Vuex auxiliary functions"""
        helpers = {}
        modules = set()

        # Identify helper function imports
        for node in ast.body:
            if node.type == 'ImportDeclaration' and 'vuex' in node.source.value:
                for spec in node.specifiers:
                    if spec.imported.name in ['mapState', 'mapGetters']:
                        helpers[spec.local.name] = spec.imported.name

        # Analysis of auxiliary function calls
        def traverse(node):
            if node.type == 'CallExpression':
                try:
                    if node.callee.name in helpers:
                        for arg in node.arguments:
                            if arg.type == 'ObjectExpression':
                                for prop in arg.properties:
                                    if prop.value.arguments:
                                        namespace = prop.value.arguments[0].value
                                        modules.add(namespace)
                except AttributeError:
                    pass
            for child in self._get_children(node):
                traverse(child)

        traverse(ast)
        return modules

    def _get_children(self, node) -> List:
        """Get AST Child Node"""
        children = []
        for attr in ['body', 'declarations', 'init', 'expression',
                     'arguments', 'properties', 'cases', 'consequent',
                     'alternate', 'block', 'handler', 'finalizer']:
            if hasattr(node, attr):
                child = getattr(node, attr)
                if isinstance(child, list):
                    children.extend(child)
                elif child is not None:
                    children.append(child)
        return children