# tests/test_api_endpoints.py
import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_protein_secondary_structure():
    """Test the CNN+BiLSTM secondary structure prediction endpoint"""
    test_data = {
        "sequence": "MLPGLALLLLAAWTARALEVPTDGNAGLLAEPQIAMFCGRLNMHMNVQNGKWDSDPSGTKTCIDTKEGILQYCQEVYPELQITNVVEANQPVTIQNWCKRGRKQCKTHPHFVIPYRCLVGEFVSDALLVPDKCKFLHQERMDVCETHLHWHTVAKETCSEKSTNLHDYGMLLPCGIDKFRGVEFVCCPLAEESDNVDSADAEEDDSDVWWGGADTDYADGSEDKVVEVAEEEEVAEVEEEEADDDEDDEDGDEVEEEAEEPYEEATERTTSIATTTTTTTESVEEVVREVCSEQAETGPCRAMISRWYFDVTEGKCAPFFYGGCGGNRNNFDTEEYCMAVCGSAMSQSLLKTTQEPLARDPVKLPTTAASTPDAVDKYLETPGDENEHAHFQKAKERLEAKHRERMSQVMREWEEAERQAKNLPKADKKAVIQHFQEKVESLEQEAANERQQLVETHMARVEAMLNDRRRLALENYITALQAVPPRPRHVFNMLKKYVRAEQKDRQHTLKHFEHVRMVDPKKAAQIRSQVMTHLRVIYERMNQSLSLLYNVPAVAEEIQDEVDELLQKEQNYSDDVLANMISEPRISYGNDALMPSLTETKTTVELLPVNGEFSLDDLQPWHSFGADSVPANTENEVEPVDARPAADRGLTTRPGSGLTNIKTEEISEVKMDAEFRHDSGYEVHHQKLVFFAEDVGSNKGAIIGLMVGGVVIATVIVITLVMLKKKQYTSIHHGVVEVDAAVTPEERHLSKMQQNGYENPTYKFFEQMQN",
        "confidence_threshold": 0.8
    }

    response = client.post("/api/bio/secondary-structure", json=test_data)
    assert response.status_code == 200
    assert "predictions" in response.json()
    assert "confidence_scores" in response.json()

def test_protein_tertiary_structure():
    """Test the VAE+Diffusion tertiary structure prediction endpoint"""
    test_data = {
        "sequence": "MLPGLALLLL",
        "num_samples": 1
    }

    response = client.post("/api/bio/tertiary-structure", json=test_data)
    assert response.status_code == 200
    assert "structure_predictions" in response.json()
    assert "ranking_scores" in response.json()

def test_materials_dft():
    """Test the NexaMat DFT calculations endpoint"""
    test_data = {
        "structure": {
            "lattice": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
            "species": ["Si", "Si"],
            "positions": [[0.0, 0.0, 0.0], [0.25, 0.25, 0.25]]
        },
        "calculation_type": "band_structure"
    }

    response = client.post("/api/materials/dft", json=test_data)
    assert response.status_code == 200
    assert "energy" in response.json()
    assert "band_structure" in response.json()

def test_qst_fidelity():
    """Test the QST fidelity calculation endpoint"""
    test_data = {
        "quantum_state": {
            "type": "pure",
            "vector": [0.707, 0, 0, 0.707]
        },
        "measurement_basis": "pauli"
    }

    response = client.post("/api/quantum/fidelity", json=test_data)
    assert response.status_code == 200
    assert "fidelity" in response.json()
    assert "confidence_interval" in response.json()
    assert "error" in response.json()

def test_qst_quantum_state():
    """Test the QST quantum state preparation endpoint"""
    test_data = {
        "target_state": {
            "type": "mixed",
            "density_matrix": [[0.5, 0], [0, 0.5]]
        },
        "preparation_method": "adiabatic"
    }

    response = client.post("/api/quantum/state-preparation", json=test_data)
    assert response.status_code == 200
    assert "prepared_state" in response.json()
    assert "success" in response.json()

def test_qst_quantum_error_correction():
    """Test the QST quantum error correction endpoint"""
    test_data = {
        "quantum_state": {
            "type": "mixed",
            "density_matrix": [[0.5, 0], [0, 0.5]]
        },
        "error_correction_method": "surface_code"
    }

    response = client.post("/api/quantum/error-correction", json=test_data)
    assert response.status_code == 200
    assert "corrected_state" in response.json()
    assert "success" in response.json()