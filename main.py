from analyzer.VueParser import VueParser
from analyzer.DependencyGraph import DependencyGraph

def main():
    project_path = "D:\日本の学習\VueDemo\Web"
    parser = VueParser(project_path)
    raw_data = parser.analyz()

    graph = DependencyGraph(raw_data)
    print("\n====Dependency====")
    print(raw_data)
    print("\n====Unused Modules====")
    print(graph.find_unused_modules())
    print("\n====Cycles Dependency====")
    print(graph.detect_circular_deps())

if __name__ == "__main__":
    main()