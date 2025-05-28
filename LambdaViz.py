import streamlit as st
import json
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_example_data():
    # Create sample example with two proteins (one with tertiary coordinates)
    coords = []
    for i in range(16):
        coords.append([
            4 * np.cos(i * 2 * np.pi / 16),
            4 * np.sin(i * 2 * np.pi / 16),
            0.5 * i
        ])
    return [
        {
            "model": "NexaBio_1",
            "sequence": "TTWPREGFMGYLALFR",
            "secondary_structure": "HECHECHECHECHECH",
            "confidence": 92,
            "timestamp": "2025-05-27T19:02:27.742372"
        },
        {
            "model": "NexaBio_2",
            "sequence": "GVIGSGRNWEGCNDMT",
            "tertiary_coordinates": coords,
            "confidence": 89,
            "timestamp": "2025-05-27T18:58:47.497334"
        }
    ]

def generate_3d_scatter(coordinates, title):
    # Create a 3D scatter trace for the provided coordinates
    x = [pt[0] for pt in coordinates]
    y = [pt[1] for pt in coordinates]
    z = [pt[2] for pt in coordinates]
    trace = go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode='markers+lines',
        marker=dict(
            size=5,
            color=z,
            colorscale='Viridis',
            opacity=0.8
        ),
        line=dict(width=4),
        name=title
    )
    return trace

def lambda_viz_dashboard():
    st.title("LambdaViz: Advanced Protein Viewer")
    st.markdown("Multi-panel 3D structure visualization")

    # Load data (try upload JSON, otherwise use example)
    uploaded_file = st.file_uploader("Upload Protein JSON", type="json", key="lambdaviz")
    if uploaded_file:
        try:
            data = json.load(uploaded_file)
        except Exception as e:
            st.error("Invalid JSON file.")
            data = create_example_data()
    else:
        data = create_example_data()

    # Filter proteins with tertiary coordinates
    proteins = [p for p in data if 'tertiary_coordinates' in p]
    if not proteins:
        st.info("No proteins with tertiary coordinates found.")
        return

    # Define grid dimensions (2 per row)
    n = len(proteins)
    cols = 2
    rows = (n + 1) // cols

    # Create subplot grid with separate 3D scenes
    specs = [[{'type': 'scene'} for _ in range(cols)] for _ in range(rows)]
    fig = make_subplots(rows=rows, cols=cols, specs=specs, subplot_titles=[p["model"] for p in proteins])

    # Add each protein structure into its panel
    for idx, protein in enumerate(proteins):
        row = idx // cols + 1
        col = idx % cols + 1
        trace = generate_3d_scatter(protein["tertiary_coordinates"], protein["model"])
        fig.add_trace(trace, row=row, col=col)
        # Adjust scene parameters if needed
        scene_id = f'scene{"" if idx == 0 else idx+1}'
        fig.layout[scene_id].update(aspectmode='data')

    fig.update_layout(
        height=600*rows,
        title_text="3D Protein Structures",
        showlegend=False,
        margin=dict(l=0, r=0, t=50, b=0)
    )
    st.plotly_chart(fig, use_container_width=True)

def main():
    st.set_page_config(page_title="LambdaViz", layout="wide")
    lambda_viz_dashboard()

if __name__ == "__main__":
    main()