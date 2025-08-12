import streamlit as st
import json
import numpy as np
import plotly.graph_objects as go
from Bio.PDB import PDBIO, StructureBuilder
from io import StringIO

# ----- Helper Functions -----
def calculate_metrics(sequence, confidence):
    amino_acids = {
        'hydrophobic': set('AVILMFYW'),
        'polar': set('STNQRHKDE'),
        'special': set('CGP')
    }
    total_len = len(sequence)
    hydrophobic = sum(aa in amino_acids['hydrophobic'] for aa in sequence) / total_len * 100
    polar = sum(aa in amino_acids['polar'] for aa in sequence) / total_len * 100
    stability = (confidence * 0.7 + hydrophobic * 0.3)
    return hydrophobic, polar, stability

def create_example_data(domain="bio"):
    if domain == "bio":
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
    elif domain == "materials":
        return {
            "model": "NexaMat_1",
            "input_structure": "Si2",
            "predicted_properties": {
                "band_gap": 1.12,
                "formation_energy": -5.4,
                "confidence_score": 98.5
            },
            "explanation": "Prediction based on GNN model."
        }
    return {}


def secondary_structure_plot(sec_str):
    counts = {}
    for char in sec_str:
        counts[char] = counts.get(char, 0) + 1
    fig = go.Figure([go.Bar(x=list(counts.keys()),
                            y=list(counts.values()),
                            marker_color='blue')])
    fig.update_traces(texttemplate='%{y}', textposition='outside')
    fig.update_layout(title="Secondary Structure Element Frequencies",
                      xaxis_title="Structure Element",
                      yaxis_title="Count")
    return fig

def fold_protein(coordinates):
    folded = []
    for coord in coordinates:
        x, y, z = coord
        new_x = x
        new_y = 4 * np.sin(x)
        new_z = 4 * np.cos(x)
        folded.append([new_x, new_y, new_z])
    return folded

def extend_sequence(sequence, extension_length=10):
    return sequence + sequence[:extension_length]

def estimate_binding_affinity(sequence):
    hydrophobic_aas = set('AVILMFYW')
    hydrophobic_count = sum(aa in hydrophobic_aas for aa in sequence)
    affinity = 5.0 + 0.1 * hydrophobic_count
    return round(affinity, 2)

def generate_pdb_from_sequence(sequence):
    builder = StructureBuilder.StructureBuilder()
    builder.init_structure("X")
    builder.init_model(0)
    builder.init_chain("A")
    for i, aa in enumerate(sequence):
        builder.init_seg("    ")
        builder.init_residue(aa, " ", i+1, " ")
        builder.init_atom("CA", np.array([i*3.8, 0.0, 0.0]), 1.0, 1.0, " ", "CA", i+1, "C")
    structure = builder.get_structure()
    io = PDBIO()
    io.set_structure(structure)
    pdb_buf = StringIO()
    io.save(pdb_buf)
    return pdb_buf.getvalue()

def coords_to_structure(seq, coordinates, fmt="pdb"):
    if fmt == "pdb":
        io = PDBIO()
        builder = StructureBuilder.StructureBuilder()
        builder.init_structure("X")
        builder.init_model(0)
        builder.init_chain("A")
        for i, coord in enumerate(coordinates):
            builder.init_residue(seq[i], " ", i+1, " ")
            builder.init_atom("CA", np.array(coord), 1.0, 1.0, " ", "CA", i+1, "C")
        structure = builder.get_structure()
        pdb_buf = StringIO()
        io.set_structure(structure)
        io.save(pdb_buf)
        return pdb_buf.getvalue()
    elif fmt == "mol2":
        mol2_str = "@\\<TRIPOS>MOLECULE\n" + seq + "\n" + str(len(coordinates)) + " 0 0 0 0\nSMALL\nNO_CHARGES\n@\\<TRIPOS>ATOM\n"
        for i, coord in enumerate(coordinates):
            mol2_str += f"{i+1:4d} CA {coord[0]:8.3f} {coord[1]:8.3f} {coord[2]:8.3f} C 1.00 0.00\n"
        mol2_str += "@\\<TRIPOS>BOND\n"
        return mol2_str
    return None

def plot_3d_structure(coordinates, title="Tertiary Structure - 3D Scatter Plot"):
    x = [coord[0] for coord in coordinates]
    y = [coord[1] for coord in coordinates]
    z = [coord[2] for coord in coordinates]
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
        title=title,
        scene=dict(aspectmode='data'),
        margin=dict(l=0, r=0, b=0, t=30)
    )
    return fig

# ----- Inference Integration -----
def perform_inference(sequence):
    # Replace this with actual backend call logic.
    # Here, we simulate a prediction score based on sequence length and affinity.
    affinity = estimate_binding_affinity(sequence)
    # Simple simulated metric: if affinity above 6, then the protein is promising.
    prediction_score = affinity / 10.0
    return prediction_score

# ----- UI Components for each Domain -----

def biology_page():
    st.header("Biology: Protein Analysis")
    with st.expander("User Instructions", expanded=True):
        st.markdown(r"""
1. **Upload** a protein JSON file or use the provided example.
2. **Select** a protein model from the drop‑down.
3. Click **Compute** to load metrics and visualizations.
4. For multi-protein 3D comparison, use the **Multi-Protein Viewer** tab.
        """)

    st.sidebar.header("Input Data")
    uploaded_file = st.sidebar.file_uploader("Upload Protein JSON", type="json", key="bio_upload")
    data = json.load(uploaded_file) if uploaded_file else create_example_data("bio")
    st.sidebar.download_button("Export Example Dataset", json.dumps(data, indent=2), file_name="protein_dataset.json")

    protein_names = [p.get("model", f"Protein {i+1}") for i, p in enumerate(data)]
    selected_idx = st.sidebar.selectbox("Select Protein Model", range(len(protein_names)), format_func=lambda i: protein_names[i])
    protein = data[selected_idx]

    if st.button("Compute"):
        st.subheader(f"Metrics for {protein.get('model')}")
        hydrophobic, polar, stability = calculate_metrics(protein['sequence'], protein['confidence'])
        affinity = estimate_binding_affinity(protein['sequence'])
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Confidence", f"{protein['confidence']}%")
        col2.metric("Stability", f"{stability:.1f}%")
        col3.metric("Hydrophobic", f"{hydrophobic:.1f}%")
        col4.metric("Binding Affinity", f"{affinity} kcal/mol")

        prediction = perform_inference(protein['sequence'])
        st.metric("Inference Prediction Score", f"{prediction:.2f}")
        if prediction > 0.6:
            st.success("Protein is promising.")
        else:
            st.info("Protein prediction suggests further review needed.")

        st.markdown("---")
        st.subheader("Sequence & Structure")

        tab1, tab2, tab3 = st.tabs(["Sequence", "Secondary Structure", "Tertiary Structure"])

        with tab1:
            st.code(protein['sequence'], language="text")
            st.caption(f"Length: {len(protein['sequence'])} residues")
            ext_seq = extend_sequence(protein['sequence'])
            st.code(ext_seq, language="text")
            st.caption(f"Extended Length: {len(ext_seq)} residues")
            pdb_data = generate_pdb_from_sequence(ext_seq)
            st.download_button("Download Extended PDB", pdb_data, file_name=f"{protein.get('model', 'protein')}_extended.pdb")

        with tab2:
            if 'secondary_structure' in protein:
                st.code(protein['secondary_structure'], language="text")
                fig_sec = secondary_structure_plot(protein['secondary_structure'])
                st.plotly_chart(fig_sec, use_container_width=True)
            else:
                st.info("No secondary structure available.")

        with tab3:
            if 'tertiary_coordinates' in protein:
                coordinates = protein['tertiary_coordinates']
                if st.button("Fold Protein", key=f"fold_{protein.get('model')}"):
                    coordinates = fold_protein(coordinates)
                fig_3d = plot_3d_structure(coordinates)
                st.plotly_chart(fig_3d, use_container_width=True)
                pdb_str = coords_to_structure(protein['sequence'], coordinates, "pdb")
                mol2_str = coords_to_structure(protein['sequence'], coordinates, "mol2")
                st.download_button("Download PDB", pdb_str, file_name=f"{protein.get('model')}.pdb")
                st.download_button("Download MOL2", mol2_str, file_name=f"{protein.get('model')}.mol2")
            else:
                st.info("No tertiary structure available.")

def materials_page():
    st.header("Materials Science: Property Prediction")
    st.sidebar.header("Input Data")
    uploaded_file = st.sidebar.file_uploader("Upload Materials JSON", type="json", key="mat_upload")
    data = json.load(uploaded_file) if uploaded_file else create_example_data("materials")

    st.subheader(f"Results for {data.get('model')}")
    st.json(data)

    if "predicted_properties" in data:
        props = data["predicted_properties"]
        cols = st.columns(len(props))
        for i, (key, value) in enumerate(props.items()):
            cols[i].metric(key.replace("_", " ").title(), f"{value:.3f}")

def llm_page():
    st.header("LLM Inference")
    st.text_area ("Enter your prompt:", height=150)
    if st.button("Generate Response"):
        # Mock API call
        st.subheader("LLM Response")
        st.info("This is a mock response. In a real application, this would call the backend API.")
        st.markdown("> The quick brown fox jumps over the lazy dog. This sentence contains all letters of the alphabet and is often used for testing typefaces.")
        st.json({
            "tokens_generated": 25,
            "metrics": {
                "total_latency_ms": 150.2,
                "time_to_first_token_ms": 50.1,
                "tokens_per_second": 166.4
            }
        })

def benchmark_page():
    st.header("Performance Benchmarking")
    model_type = st.selectbox("Select Model to Benchmark", ["bio", "materials", "llm"])
    duration = st.slider("Test Duration (seconds)", 5, 60, 10)

    if st.button("Run Benchmark"):
        # Mock API call
        st.info(f"Running benchmark for **{model_type}** model for **{duration}** seconds...")
        st.success("Benchmark complete!")
        st.json({
            "benchmark_model": f"{model_type}_1",
            "test_duration_seconds": duration,
            "total_requests": 50,
            "avg_latency_ms": 85.5,
            "throughput_req_per_sec": 5.0
        })

# ----- Main App -----
def main():
    st.set_page_config(layout="wide", page_title="Nexa_Inference Dashboard", initial_sidebar_state="expanded")
    st.sidebar.title("Nexa_Inference")

    page_options = {
        "Biology Analysis": biology_page,
        "Materials Science": materials_page,
        "LLM Inference": llm_page,
        "Benchmarking": benchmark_page
    }

    page_selection = st.sidebar.radio("Select a Domain", list(page_options.keys()))

    st.title("Nexa_Inference Dashboard")

    # Render the selected page
    page_options[page_selection]()

if __name__ == "__main__":
    main()
