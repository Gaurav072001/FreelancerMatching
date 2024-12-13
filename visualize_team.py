import networkx as nx
import matplotlib.pyplot as plt

def visualize_team(team):
    G=nx.Graph()
    for freelancer in team:
        G.add_node(freelancer.name, clolor='blue')
        for skill in freelancer.skills:
            G.add_node(skill, color="green")
            G.add_edge(freelancer.name, skill)
    
    colors= [G.nodes[node].get('color','black') for node in G.nodes()]
    nx.draw(G, with_labels=True, node_color=colors, node_size=1500)
    plt.show()