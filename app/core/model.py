import logging
import os
from datetime import datetime
from typing import List, Tuple

import numpy as np
import pandas as pd
import torch
import yaml
from Bio import SeqIO
from torch import nn
from tqdm import tqdm

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class HelixSynthMini (nn.Module):
    def __init__(self, embedding_dim=20, hidden_dim=64, num_layers=2, dropout=0.2):
        super ().__init__ ()
        self.embedding = nn.Embedding (21, embedding_dim)

        self.cnn = nn.Sequential (
            nn.Conv1d (embedding_dim, hidden_dim, 3, padding=1),  # cnn.0
            nn.ReLU (),
            nn.BatchNorm1d (hidden_dim)
        )

        self.lstm = nn.LSTM (
            hidden_dim,
            hidden_dim,
            num_layers,
            bidirectional=True,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0
        )

        self.fc = nn.Linear (hidden_dim * 2, 3)
        self.dropout = nn.Dropout (dropout)

    def forward(self, x):
        x = self.embedding (x)
        x = x.permute (0, 2, 1)

        x = self.cnn (x)

        x = x.permute (0, 2, 1)
        x, _ = self.lstm (x)

        x = self.dropout (x)
        x = self.fc (x)
        return x

    def load_state_dict(self, state_dict, strict=False):
        """Custom state dict loading to handle key mismatches"""
        new_state_dict = {}
        for k, v in state_dict.items ():
            if k == 'embedding.weight':
                new_state_dict ['embedding.weight'] = v
            else:
                new_state_dict [k] = v

        super ().load_state_dict (new_state_dict, strict=False)


class ProteinDataGenerator:
    def __init__(self, config_path: str = "config.yml"):
        """Initialize the ProteinDataGenerator with configuration."""
        self.config = self._load_config (config_path)
        self.device = torch.device ('cuda' if torch.cuda.is_available () else 'cpu')

        self.aa_map = {
            'A': 0, 'C': 1, 'D': 2, 'E': 3, 'F': 4,
            'G': 5, 'H': 6, 'I': 7, 'K': 8, 'L': 9,
            'M': 10, 'N': 11, 'P': 12, 'Q': 13, 'R': 14,
            'S': 15, 'T': 16, 'V': 17, 'W': 18, 'Y': 19,
            'X': 20
        }

        self.model = self._initialize_model ()
        logger.info (f"Initialized ProteinDataGenerator on device: {self.device}")

    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file."""
        try:
            with open (config_path, 'r') as f:
                config = yaml.safe_load (f)
                logger.info ("Configuration loaded successfully")
                return config
        except Exception as e:
            logger.error (f"Error loading config: {e}")
            raise

    def _initialize_model(self) -> HelixSynthMini:
        """Initialize and load the model."""
        try:
            model = HelixSynthMini (
                embedding_dim=20,
                hidden_dim=self.config ['model'] ['architecture'] ['hidden_dim'],
                num_layers=self.config ['model'] ['architecture'] ['num_layers'],
                dropout=self.config ['model'] ['architecture'] ['dropout']
            )

            from torch.serialization import add_safe_globals
            import numpy as np
            add_safe_globals ([np._core.multiarray.scalar])

            checkpoint_path = self.config ['model'] ['weights'] ['path']
            logger.info (f"Loading checkpoint from: {checkpoint_path}")

            checkpoint = torch.load (
                checkpoint_path,
                map_location=self.device,
                weights_only=False
            )

            logger.info ("Model architecture:")
            logger.info (model)

            if isinstance (checkpoint, dict):
                if 'model_state_dict' in checkpoint:
                    state_dict = checkpoint ['model_state_dict']
                else:
                    state_dict = checkpoint

                logger.info ("State dict keys:")
                logger.info (state_dict.keys ())

                model.load_state_dict (state_dict)
                logger.info ("Model loaded successfully")
            else:
                raise ValueError ("Invalid checkpoint format")

            model.to (self.device)
            model.eval ()
            return model

        except Exception as e:
            logger.error (f"Error initializing model: {e}")
            raise

    def encode_sequence(self, seq: str, max_len: int) -> List [int]:
        """Encode a protein sequence to indices."""
        try:
            seq = seq.upper ()
            encoded = []

            for aa in seq [:max_len]:
                if aa in self.aa_map:
                    encoded.append (self.aa_map [aa])
                else:
                    encoded.append (self.aa_map ['X'])

            if len (encoded) < max_len:
                encoded.extend ([self.aa_map ['X']] * (max_len - len (encoded)))

            return encoded [:max_len]

        except Exception as e:
            logger.error (f"Error encoding sequence: {e}")
            return [self.aa_map ['X']] * max_len

    def process_batch(self, sequences: List [str], max_len: int) -> List [dict]:
        """Process a batch of sequences."""
        try:
            encoded = [self.encode_sequence (seq, max_len) for seq in sequences]
            x = torch.tensor (encoded, dtype=torch.long).to (self.device)

            with torch.no_grad ():
                output = self.model (x)
                preds = output.argmax (dim=-1)
                confs = torch.softmax (output, dim=-1).max (dim=-1) [0].mean (dim=-1)

            results = []
            for seq, pred, conf in zip (sequences, preds, confs):
                structure = ''.join (['HEC' [i] for i in pred.cpu ()]) [:len (seq)]
                results.append ({
                    'sequence': seq,
                    'structure': structure,
                    'confidence': conf.item (),
                    'length': len (seq),
                })
            return results

        except Exception as e:
            logger.error (f"Error processing batch: {e}")
            return []

    def predict_and_generate(self, num_samples: int = 1000) -> Tuple [pd.DataFrame, pd.DataFrame]:
        """Main prediction and generation pipeline."""
        try:
            sequences = []
            for record in SeqIO.parse (self.config ['data'] ['input'] ['fasta_path'], 'fasta'):
                if len (record.seq) > 0:
                    sequences.append (str (record.seq))

            real_results = []
            batch_size = self.config ['runtime'] ['batch_size']
            max_len = self.config ['model'] ['architecture'] ['max_sequence_length']

            for i in tqdm (range (0, len (sequences), batch_size), desc="Processing real sequences"):
                batch = sequences [i:i + batch_size]
                batch_results = self.process_batch (batch, max_len)
                for result in batch_results:
                    result ['type'] = 'real'
                real_results.extend (batch_results)

            synthetic_results = []
            valid_aas = list (self.aa_map.keys ()) [:-1]  # Exclude 'X'

            for _ in tqdm (range (num_samples), desc="Generating synthetic data"):
                seq_len = np.random.randint (50, 200)
                seq = ''.join (np.random.choice (valid_aas) for _ in range (seq_len))
                batch_results = self.process_batch ([seq], max_len)
                if batch_results:
                    batch_results [0] ['type'] = 'synthetic'
                    synthetic_results.extend (batch_results)

            return pd.DataFrame (real_results), pd.DataFrame (synthetic_results)

        except Exception as e:
            logger.error (f"Error in prediction pipeline: {e}")
            return pd.DataFrame (), pd.DataFrame ()

def main():
    try:
        logger.info("Initializing protein data generator...")
        generator = ProteinDataGenerator()

        logger.info("Starting prediction and generation pipeline...")
        real_data, synthetic_data = generator.predict_and_generate(num_samples=5000)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir = os.path.join('predictions', timestamp)
        os.makedirs(output_dir, exist_ok=True)

        real_data.to_csv(os.path.join(output_dir, 'real_predictions.csv'), index=False)
        synthetic_data.to_csv(os.path.join(output_dir, 'synthetic_data.csv'), index=False)

        combined_data = pd.concat([real_data, synthetic_data])
        combined_data.to_csv(os.path.join(output_dir, 'combined_data.csv'), index=False)

        logger.info(f"Pipeline completed. Results saved to {output_dir}")
        logger.info(f"Total sequences processed: {len(combined_data)}")

    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")

if __name__ == "__main__":
    main()
