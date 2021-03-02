def buildTopology(COMPONENTS, topologyPath) -> None:
    TOPOLOGIES = {
        componentName: findTopology(component)
        for componentName, component in COMPONENTS.items()
    }
    with open(topologyPath, 'wb') as file:
        dump(TOPOLOGIES, file)

def buildCorner(COMPONENTS, cornerPath) -> None:
    CORNERS = {
        componentName: findCorner(component)
        for componentName, component in COMPONENTS.items()
    }
    with open(cornerPath, 'wb') as file:
        dump(CORNERS, file)
