import networkx as nx
from pyvis.network import Network


data = [
    {
        "microalgae": "Spirulina sp.",
        "heavy_metals": ["mercury", "cadmium"],
        "concentration_tested": {"cadmium": "3.82 mg/kg"},
        "outcome": {
            "metal_factor_concentration": "80–4250",
            "bioconcentration_capacity": {"cadmium": "0.40 µg/g biomass", "mercury": "1.34 µg/g biomass"}
        },
    },
    {
        "microalgae": "Chlamydomonas reinhardtii",
        "heavy_metals": ["mercury", "cadmium", "lead"],
        "concentration_tested": {"mercury": "0.76 mg/kg", "cadmium": "100 mg/kg"},
        "outcome": {
            "biosorption_capacity": {"mercury": "0.072 mg/kg", "cadmium": "0.043 mg/kg", "lead": "0.098 mg/kg"}
        },
    },
    {
        "microalgae": "Ulothrix zonata",
        "heavy_metals": ["copper"],
        "concentration_tested": {"range": "5 - 52 mg/L"},
        "outcome": {"adsorption_model": "langmuir", "removal_time": "1200s", "optimum_pH": "4.5s"},
    },
    {
        "microalgae": "Spirogyra sp.",
        "heavy_metals": ["lead"],
        "concentration_tested": {"range": "105 - 204 mg/L"},
        "outcome": {
            "max_adsorption_capacity": "140 mg/g biomass",
            "time_frame": "1.867 hours",
            "initial_concentration": "200 mg/L",
        },
    },
    {
        "microalgae": "Spirulina platensis",
        "heavy_metals": ["cadmium"],
        "concentration_tested": {"range": "40-200 mg/L"},
        "outcome": {
            "removal_efficiency": "87.69 %",
            "adsorption_model": "langmuir",
            "best_fit_model": "freundlich",
            "desired_removal_rate": "90 %",
        },
    },
    {
        "microalgae": "Parachlorella sp.",
        "heavy_metals": ["cadmium"],
        "concentration_tested": {"range": "18-180 mg/L"},
        "outcome": {"max_adsorption_capacity": "98.20 mg/g", "temperature": "35 °C"},
    },
    {
        "microalgae": "Scenedesmus obliquus",
        "heavy_metals": ["cadmium"],
        "concentration_tested": {"range": "2.8-7.7 mg/L"},
        "outcome": {
            "breakthrough_time": "930 mins",
            "adsorption_capacity": "0.038 mg/g",
            "flow_rate": "6 mL/min",
            "influent_concentration": "0.008 mg/L",
        },
    }
]

G = nx.Graph()

net = Network(height="700px", width="100%", notebook=True, directed=False)

custom_html = """
<html>
<head>
    <title>Microalgae Heavy Metal Interaction Network</title>
    <style>
        body {
            background-color: #f4f4f4;
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
        }
        h1 {
            background-color: #2c3e50;
            color: white;
            padding: 20px;
            margin: 0;
            font-size: 24px;
        }
        #network {
            width: 100%;
            height: 700px;
            margin: 20px auto;
            border-radius: 10px;
            background: white;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
        }
    </style>
</head>
<body>
    <h1>Microalgae Heavy Metal Interaction Network</h1>
    <div id="network"></div>
</body>
</html>
"""

# Set custom options for better appearance
net.set_options("""
var options = {
  "nodes": {
    "shape": "dot",
    "scaling": { "min": 10, "max": 30 },
    "font": { "size": 14, "color": "#34495e" }
  },
  "edges": {
    "color": { "inherit": true },
    "width": 1.5
  },
  "physics": {
    "barnesHut": {
      "gravitationalConstant": -3000,
      "springLength": 150,
      "springConstant": 0.05
    },
    "minVelocity": 0.75
  }
}
""")


for entry in data:
    microalgae = entry["microalgae"]
    heavy_metals = entry["heavy_metals"]
    concentration_tested = entry["concentration_tested"]
    outcome = entry["outcome"]

    G.add_node(microalgae)
    net.add_node(microalgae, label=microalgae, color="blue", size=20, title=f"Microalgae: {microalgae}")

    for metal in heavy_metals:
        G.add_node(metal)
        net.add_node(metal, label=metal, color="red", size=15, title=f"Heavy Metal: {metal}")
        net.add_edge(microalgae, metal, color="gray", title="Removes")

    adsorption_model = outcome.get("adsorption_model")
    if adsorption_model:
        G.add_node(adsorption_model)
        net.add_node(adsorption_model, label=adsorption_model, color="green", size=15, title="Adsorption Model")
        net.add_edge(microalgae, adsorption_model, color="black", title="Uses")

    for key, value in outcome.items():
        if isinstance(value, dict):  # Handle nested dictionary values
            for sub_key, sub_value in value.items():
                sub_node_label = f"{sub_key}: {sub_value}"
                G.add_node(sub_node_label)
                net.add_node(sub_node_label, label=sub_node_label, color="purple", size=12, title=f"{sub_key.replace('_', ' ').title()}: {sub_value}")
                net.add_edge(microalgae, sub_node_label, color="gray", title="Outcome")
        else:
            node_label = f"{key}: {value}"
            G.add_node(node_label)
            net.add_node(node_label, label=node_label, color="purple", size=12, title=f"{key.replace('_', ' ').title()}: {value}")
            net.add_edge(microalgae, node_label, color="gray", title="Outcome")

    # Add concentration values as nodes
    for key, value in concentration_tested.items():
        node_label = f"{key}: {value}"
        G.add_node(node_label)
        net.add_node(node_label, label=node_label, color="orange", size=12, title=f"Concentration {key.replace('_', ' ').title()}: {value}")
        net.add_edge(microalgae, node_label, color="gray", title="Concentration")



for entry in data:
    microalgae = entry["microalgae"]
    heavy_metals = entry["heavy_metals"]
    concentration_tested = entry["concentration_tested"]
    outcome = entry["outcome"]

    G.add_node(microalgae)
    net.add_node(microalgae, label=microalgae, color="blue", size=20, title=f"Microalgae: {microalgae}")

    for metal in heavy_metals:
        G.add_node(metal)
        net.add_node(metal, label=metal, color="red", size=15, title=f"Heavy Metal: {metal}")
        net.add_edge(microalgae, metal, color="gray", title="Removes")

    adsorption_model = outcome.get("adsorption_model")
    if adsorption_model:
        G.add_node(adsorption_model)
        net.add_node(adsorption_model, label=adsorption_model, color="green", size=15, title="Adsorption Model")
        net.add_edge(microalgae, adsorption_model, color="black", title="Uses")

    for key, value in outcome.items():
        if isinstance(value, dict):  # Handle nested dictionary values
            for sub_key, sub_value in value.items():
                sub_node_label = f"{sub_key}: {sub_value}"
                G.add_node(sub_node_label)
                net.add_node(sub_node_label, label=sub_node_label, color="purple", size=12, title=f"{sub_key.replace('_', ' ').title()}: {sub_value}")
                net.add_edge(microalgae, sub_node_label, color="gray", title="Outcome")
        else:
            node_label = f"{key}: {value}"
            G.add_node(node_label)
            net.add_node(node_label, label=node_label, color="purple", size=12, title=f"{key.replace('_', ' ').title()}: {value}")
            net.add_edge(microalgae, node_label, color="gray", title="Outcome")

    for key, value in concentration_tested.items():
        node_label = f"{key}: {value}"
        G.add_node(node_label)
        net.add_node(node_label, label=node_label, color="orange", size=12, title=f"Concentration {key.replace('_', ' ').title()}: {value}")
        net.add_edge(microalgae, node_label, color="gray", title="Concentration")


net.show("index.html")

