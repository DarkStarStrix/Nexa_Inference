import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Provided tertiary structure data
data = {
    "model": "NexaBio_2",
    "sequence": "GVIGSGRNWEGCNDMT",
    "tertiary_coordinates": [
        [0, 0, 0],
        [1.1, 1.2, 1.3],
        [2.2, 2.4, 2.6],
        [3.3, 3.6, 3.9],
        [4.4, 4.8, 5.2],
        [5.5, 6, 6.5],
        [6.6, 7.2, 7.8],
        [7.7, 8.4, 9.1],
        [8.8, 9.6, 10.4],
        [9.9, 10.8, 11.7],
        [11, 12, 13],
        [12.1, 13.2, 14.3],
        [13.2, 14.4, 15.6],
        [14.3, 15.6, 16.9],
        [15.4, 16.8, 18.2],
        [16.5, 18, 19.5]
    ],
    "confidence": 89,
    "timestamp": "2025-05-27T18:58:47.497334"
}

def fold_protein(coordinates):
    """
    Simulate protein folding by transforming the coordinates.
    This basic transformation uses sine and cosine functions
    to fold the linear structure.
    """
    folded = []
    for coord in coordinates:
        x, y, z = coord
        # Use the x coordinate for folding simulation.
        new_x = x
        new_y = 4 * np.sin(x)
        new_z = 4 * np.cos(x)
        folded.append([new_x, new_y, new_z])
    return folded

def main():
    st.set_page_config(layout="wide", page_title="3D Protein Structure Viewer")
    st.title("3D Protein Structure Viewer with Folding Simulation")

    # Get original coordinates
    coordinates = data["tertiary_coordinates"]

    # Button to apply protein folding transformation
    if st.button("Fold Protein"):
        coordinates = fold_protein(coordinates)

    # Extract coordinates for plotting
    x = [coord[0] for coord in coordinates]
    y = [coord[1] for coord in coordinates]
    z = [coord[2] for coord in coordinates]

    # Create Plotly 3D scatter plot with connecting lines
    fig = go.Figure(data=[
        go.Scatter3d(
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
            line=dict(width=4)
        )
    ])
    fig.update_layout(
        title="Tertiary Structure - 3D Scatter Plot",
        scene=dict(aspectmode='data'),
        margin=dict(l=0, r=0, b=0, t=30)
    )

    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
