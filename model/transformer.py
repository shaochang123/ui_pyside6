import torch.nn as nn
import torch
class TransformerClassifier(torch.nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim, num_heads, num_layers, dropout=0.2):
        super(TransformerClassifier, self).__init__()

        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.output_dim = output_dim
        self.num_heads = num_heads
        self.num_layers = num_layers

        # Transformer Encoder
        self.encoder_layer = nn.TransformerEncoderLayer(d_model=hidden_dim, nhead=num_heads, dropout=dropout)
        self.transformer_encoder = nn.TransformerEncoder(self.encoder_layer, num_layers=num_layers)

        # Input projection layer
        self.input_proj = nn.Linear(input_dim, hidden_dim)

        # Output layer
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        # Input projection
        x = self.input_proj(x)

        # Transformer Encoder
        x = x.permute(1, 0, 2)  # (seq_length, batch_size, hidden_dim)
        x = self.transformer_encoder(x)
        x = x.permute(1, 0, 2)  # (batch_size, seq_length, hidden_dim)

        # Take the last time step's output for classification
        x = x[:, -1, :]

        # Output layer
        out = self.fc(x)
        return out