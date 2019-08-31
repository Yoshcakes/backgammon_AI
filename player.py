"""
Describes a player
"""

import numpy as np
from collections import deque


class Player:
    def __init__(self, color):
        self.player = player
        self.epsilon = 1.0
        self.epsilon_decay = 0.995
        self.memory = deque(maxlen=2000)

    def roll(self):
        roll = np.random.randint(1, 7, size=2)
        if roll[0] == roll[1]:
            return np.hstack([roll, roll])
        else:
            return roll
            
    def _build_model(self):
        return

    def act(self, board):
        legal_moves = board.legal_moves(self.player, self.roll)
        return np.random.choice(legal_moves, 1)

        # self.epsilon *= self.epsilon_decay
        # self.epsilon = max(self.epsilon_min, self.epsilon)
        # if np.random.random() < self.epsilon:
        #     return np.random.choice(legal_moves, 1)
        # return np.argmax(self.model.predict(board)[0])

    def remember(self, state, action, reward, new_state, done):
        self.memory.append([state, action, reward, new_state, done])

    def replay(self):
        batch_size = 32
        if len(self.memory) < batch_size: 
            return

        samples = np.random.choice(self.memory, batch_size)
        for sample in samples:
            state, action, reward, new_state, done = sample
            target = self.target_model.predict(state)
            if done:
                target[0][action] = reward
            else:
                Q_future = max(self.target_model.predict(new_state)[0])
                target[0][action] = reward + Q_future * self.gamma
            self.model.fit(state, target, epochs=1, verbose=0)




# class DQN:
#     def __init__(self, env):
#         self.env     = env
#         self.memory  = deque(maxlen=2000)
        
#         self.gamma = 0.85
#         self.epsilon = 1.0
#         self.epsilon_min = 0.01
#         self.epsilon_decay = 0.995
#         self.learning_rate = 0.005
#         self.tau = .125

#         self.model        = self.create_model()
#         self.target_model = self.create_model()

#     def create_model(self):
#         model   = Sequential()
#         state_shape  = self.env.observation_space.shape
#         model.add(Dense(24, input_dim=state_shape[0], activation="relu"))
#         model.add(Dense(48, activation="relu"))
#         model.add(Dense(24, activation="relu"))
#         model.add(Dense(self.env.action_space.n))
#         model.compile(loss="mean_squared_error",
#             optimizer=Adam(lr=self.learning_rate))
#         return model

#     def act(self, state):
#         self.epsilon *= self.epsilon_decay
#         self.epsilon = max(self.epsilon_min, self.epsilon)
#         if np.random.random() < self.epsilon:
#             return self.env.action_space.sample()
#         return np.argmax(self.model.predict(state)[0])

#     def remember(self, state, action, reward, new_state, done):
#         self.memory.append([state, action, reward, new_state, done])

#     def replay(self):
#         batch_size = 32
#         if len(self.memory) < batch_size: 
#             return

#         samples = random.sample(self.memory, batch_size)
#         for sample in samples:
#             state, action, reward, new_state, done = sample
#             target = self.target_model.predict(state)
#             if done:
#                 target[0][action] = reward
#             else:
#                 Q_future = max(self.target_model.predict(new_state)[0])
#                 target[0][action] = reward + Q_future * self.gamma
#             self.model.fit(state, target, epochs=1, verbose=0)

#     def target_train(self):
#         weights = self.model.get_weights()
#         target_weights = self.target_model.get_weights()
#         for i in range(len(target_weights)):
#             target_weights[i] = weights[i] * self.tau + target_weights[i] * (1 - self.tau)
#         self.target_model.set_weights(target_weights)

#     def save_model(self, fn):
#         self.model.save(fn)

#         class DQNAgent:
#             def __init__(self, state_size, action_size):
#                 self.state_size = state_size
#                 self.action_size = action_size
#                 self.memory = deque(maxlen=2000)
#                 self.gamma = 0.95    # discount rate
#                 self.epsilon = 1.0  # exploration rate
#                 self.epsilon_min = 0.01
#                 self.epsilon_decay = 0.995
#                 self.learning_rate = 0.001
#                 self.model = self._build_model()
#             def _build_model(self):
#                 # Neural Net for Deep-Q learning Model
#                 model = Sequential()
#                 model.add(Dense(24, input_dim=self.state_size, activation='relu'))
#                 model.add(Dense(24, activation='relu'))
#                 model.add(Dense(self.action_size, activation='linear'))
#                 model.compile(loss='mse',
#                               optimizer=Adam(lr=self.learning_rate))
#                 return model
#             def remember(self, state, action, reward, next_state, done):
#                 self.memory.append((state, action, reward, next_state, done))
#             def act(self, state):
#                 if np.random.rand() <= self.epsilon:
#                     return random.randrange(self.action_size)
#                 act_values = self.model.predict(state)
#                 return np.argmax(act_values[0])  # returns action
#             def replay(self, batch_size):
#                 minibatch = random.sample(self.memory, batch_size)
#                 for state, action, reward, next_state, done in minibatch:
#                     target = reward
#                     if not done:
#                       target = reward + self.gamma * \
#                                np.amax(self.model.predict(next_state)[0])
#                     target_f = self.model.predict(state)
#                     target_f[0][action] = target
#                     self.model.fit(state, target_f, epochs=1, verbose=0)
#                 if self.epsilon > self.epsilon_min:
#                     self.epsilon *= self.epsilon_decay
        