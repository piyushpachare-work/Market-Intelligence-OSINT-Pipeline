from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import io
import os

app = FastAPI()

CSV_PATH = "section_FCSV/KPI2.csv"

def load_clean_data():
    df = pd.read_csv(CSV_PATH, encoding='utf-8')
    df.columns = df.columns.str.replace('\ufeff', '', regex=False).str.strip()
    df.rename(columns={
        'Sub-category': 'Sub_Category',
        'Search Volume': 'Search_Volume',
        'Keyword Difficulty': 'Keyword_Difficulty',
        'Related Terms': 'Related_Terms',
        'Question-based Searches': 'Question_Based_Searches'
    }, inplace=True)

    df['Sub_Category'] = df['Sub_Category'].fillna(df['Category'] + ' (General)')
    df['Sub_Category'] = df['Sub_Category'].str.strip()
    df['Category'] = df['Category'].str.strip()
    df['Keyword'] = df['Keyword'].str.strip()

    df['Node_Size'] = np.log1p(df['Search_Volume']) * 50
    df['Node_Size'] = df['Node_Size'].apply(lambda x: max(x, 10))
    return df

@app.get("/F/KPI2")
def generate_ecosystem_chart():
    if not os.path.exists(CSV_PATH):
        return JSONResponse(status_code=404, content={"error": "KPI2.csv not found."})

    try:
        df = load_clean_data()
        G = nx.Graph()

        for _, row in df.iterrows():
            cat_node = f"Cat: {row['Category']}"
            sub_node = f"Sub: {row['Sub_Category']}"
            key_node = row['Keyword']

            G.add_node(cat_node, type='category', color='skyblue', size=300)
            G.add_node(sub_node, type='sub_category', color='lightgreen', size=200)
            G.add_node(key_node, type='keyword', color='salmon', size=row['Node_Size'])

            G.add_edge(cat_node, sub_node)
            G.add_edge(sub_node, key_node)

        pos = nx.spring_layout(G, seed=42, k=0.35, iterations=50)
        node_colors = [data['color'] for _, data in G.nodes(data=True)]
        node_sizes = [data['size'] for _, data in G.nodes(data=True)]

        plt.figure(figsize=(20, 18))
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, alpha=0.9)
        nx.draw_networkx_edges(G, pos, alpha=0.3, edge_color='gray')
        labels = {node: node for node, data in G.nodes(data=True)}
        nx.draw_networkx_labels(G, pos, labels=labels, font_size=8)

        plt.title("Keyword Ecosystem Map", fontsize=18)
        plt.axis('off')
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        return Response(content=buf.read(), media_type="image/png")

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
