from pathlib import Path
import json

flows = {}

# 1. Ler todos os json
for file in Path("flows").glob("*.json"):
    with open(file, encoding="utf8") as f:
        flows[file.stem] = json.load(f)

# 2. Criar nós
nodes = []

for flow_name, flow in flows.items():

    nodes.append({
        "type": "flow",
        "id": flow_name,
        "label": flow_name
    })

    for i, step in enumerate(flow["steps"]):

        nodes.append({
            "type": step["action"],
            "id": f"{flow_name}_{i}",
            "label": step["action"]
        })

# 3. Criar conexões
edges = []

for flow_name, flow in flows.items():

    previous = flow_name

    for i, step in enumerate(flow["steps"]):

        current = f"{flow_name}_{i}"

        edges.append((previous, current))

        previous = current

        if step["action"] == "flow":

            edges.append(
                (
                    current,
                    step["flow"]
                )
            )

print(nodes)
print(edges)