import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.distributions.categorical import Categorical


def layer_init(layer, std=np.sqrt(2), bias_const=0.0):
    torch.nn.init.orthogonal_(layer.weight, std)
    torch.nn.init.constant_(layer.bias, bias_const)
    return layer

# class AgentRL(nn.Module):
#     def __init__(self, dim_obs, dim_action):
#         super(AgentRL, self).__init__()
#         self.q_network = nn.Sequential(
#             layer_init(nn.Linear(dim_obs, 64)),
#             nn.Tanh(),
#             layer_init(nn.Linear(64, 64)),
#             nn.Tanh(),
#             layer_init(nn.Linear(64, dim_action), std=1.0)
#         )

#     def forward(self, x):
#         return self.q_network(x)


class AgentRL(nn.Module):
    def __init__(self, dim_obs, dim_action):
        super(AgentRL, self).__init__()
        self.critic = nn.Sequential(
            layer_init(nn.Linear(dim_obs, 64)),
            nn.Tanh(),
            layer_init(nn.Linear(64, 64)),
            nn.Tanh(),
            layer_init(nn.Linear(64, 1), std=1.0),
        )
        self.actor = nn.Sequential(
            layer_init(nn.Linear(dim_obs, 64)),
            nn.Tanh(),
            layer_init(nn.Linear(64, 64)),
            nn.Tanh(),
            layer_init(nn.Linear(64, dim_action), std=0.01),
        )

    def get_value(self, x):
        return self.critic(x)

    def get_action_and_value(self, x, action=None):
        logits = self.actor(x)
        if torch.isnan(logits).sum().item() > 0:
            print('he')
        probs = Categorical(logits=logits)
        if action is None:
            action = probs.sample()
        return action, probs.log_prob(action), probs.entropy(), self.critic(x)



