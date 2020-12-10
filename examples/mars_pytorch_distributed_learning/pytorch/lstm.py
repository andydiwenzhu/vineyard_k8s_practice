import os
import sys
import torch

import vineyard

import torch.distributed as dist
import torch.nn as nn
import torch.optim as optim

from torch.nn.parallel import DistributedDataParallelCPU as DDP

class LSTMPredictor(nn.Module):

    def __init__(self, embedding_dim, hidden_dim):
        super(LSTMTagger, self).__init__()
        self.hidden_dim = hidden_dim
        self.lstm = nn.LSTM(embedding_dim, hidden_dim)
        self.hidden = nn.Linear(hidden_dim, 1)

    def forward(self, vec):
        lstm_out, _ = self.lstm(vec)
        return self.hidden(lstm_out)


def train(dist, vineyard_ipc_socket, input_id):
    rank = dist.rank()
    client = vineyard.connect(vineyard_ipc_socket)
    training_data = client.get(input_id).fetch_partition(rank, allow_migration=True)

    model = LSTMPredictor(EMBEDDING_DIM, HIDDEN_DIM)
    loss_function = nn.NLLLoss()
    optimizer = optim.SGD(model.parameters(), lr=0.1)

    for epoch in range(100):
        for x, y in training_data:
            model.zero_grad()
            y_ = model(x)
            loss = loss_function(y_, y)
            loss.backward()
            optimizer.step()


if __name__ == '__main__':
    world_size = int(os.environ.get('WORLD_SIZE', 1))
    vineyard_ipc_socket = os.environ.get('VINEYARD_IPC_SOCKET')
    input_id = os.environ.get('INPUT_ID')

    dist.init_process_group("gloo", world_size=world_size)

    train(dist, vineyard_ipc_socket, input_id)

    dist.destroy_process_group()