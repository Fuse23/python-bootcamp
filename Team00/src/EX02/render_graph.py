import json
import os
from typing import Mapping

import matplotlib.pyplot as plt
import networkx as nx
import altair as alt
import pandas as pd
from dotenv import load_dotenv


def get_graph() -> nx.DiGraph:
    path: str | None = os.environ.get('WIKI_FILE')
    if not path:
        print('Database not found')
        exit(-1)
    path = os.path.dirname(__file__) + path
    if not os.path.exists(path):
        print('Database not found', path)
        exit(-1)
    graph: dict = {}
    with open(path, 'r') as file:
        graph = json.load(file)
    return nx.DiGraph(graph, directed=True)


def get_nodes_html(nodes: pd.DataFrame,
                   graph: nx.DiGraph,
                   node_sizes: dict) -> alt.Chart:
    nodes['size'] = nodes['id'].map(node_sizes)
    return alt.Chart(nodes).mark_circle().encode(
        x='x',
        y='y',
        size=alt.Size(
            'size',
            scale=alt.Scale(range=[min(node_sizes), max(node_sizes)]),
        ),
        tooltip=['id']
    ).properties(width=800, height=800, title='GRAPH')


def get_text_html(nodes: pd.DataFrame) -> alt.Chart:
    return alt.Chart(nodes).mark_text(
        align='left',
        baseline='middle',
        dx=7,
        size=14,
    ).encode(
        x='x:Q',
        y='y:Q',
        text='id'
    )


def get_chart(graph: nx.DiGraph, positions: Mapping) -> alt.Chart:
    arrows: list = []
    for source, target in graph.edges:
        arrows.append((
            positions[source][0], positions[source][1],
            positions[target][0], positions[target][1],
        ))
    arrows_data: pd.DataFrame = pd.DataFrame(
        arrows,
        columns=['x', 'y', 'xx', 'yy'],
    )
    return alt.Chart(arrows_data).mark_text(
        align='left',
        baseline='middle',
        dx=7,
        size=10,
    ).encode(
        x='x:Q',
        y='y:Q',
        opacity=alt.value(0),
        text='arrow:N',
    ) + alt.Chart(arrows_data).mark_line(opacity=0.5).encode(
        x='x:Q',
        y='y:Q',
        x2='xx:Q',
        y2='yy:Q'
    ).interactive()


def generate_html(graph: nx.DiGraph,
                  positions: Mapping,
                  node_sizes: dict) -> None:
    nodes: pd.DataFrame = pd.DataFrame(
        positions, index=['x', 'y']
    ).T.reset_index().rename(columns={'index': 'id'})
    html_graph: alt.Chart = \
        get_nodes_html(nodes, graph, node_sizes) \
        + get_text_html(nodes) \
        + get_chart(graph, positions)
    html_graph.save(os.path.dirname(__file__) + '/../wiki_graph.html')


def graph_render() -> None:
    Graph: nx.DiGraph = get_graph()
    node_sizes: dict = dict(Graph.degree())
    positions: Mapping = nx.kamada_kawai_layout(Graph)
    fig, ax = plt.subplots(figsize=(80, 80))
    nx.draw(
        G=Graph,
        pos=positions,
        with_labels=False,
        node_size=[node_sizes[node] for node in Graph.nodes()],
        ax=ax,
    )
    title_postitions: dict = {
        node: (x, y + 0.01) for node, (x, y) in positions.items()
    }
    nx.draw_networkx_labels(
        G=Graph,
        pos=title_postitions,
        font_color='red',
        ax=ax,
    )
    plt.savefig(os.path.dirname(__file__) + '/../wiki_graph.png', format='png')
    if input('Create wiki_graph.html file (y/N)? ').lower() == 'y':
        generate_html(Graph, positions, node_sizes)


def load_env() -> None:
    env_path: str = os.path.join(os.path.dirname(__file__), '../.env')
    if not os.path.exists(env_path):
        print(
            '.env file not found\n'
            + 'Check README_src.md file for more information'
        )
        exit(-1)
    load_dotenv(env_path)


if __name__ == '__main__':
    load_env()
    graph_render()
