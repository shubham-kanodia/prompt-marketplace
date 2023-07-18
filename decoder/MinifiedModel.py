import torch.nn as nn


class MinifiedModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv_out = nn.Conv2d(128, 3, 3, padding=1)

    def forward(self, x):
        sample = self.conv_out(x)
        return sample
