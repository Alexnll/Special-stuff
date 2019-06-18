'''
Minimal character-level Vanilla RNN model implementation based on numpy
https://gist.github.com/karpathy/d4dee566867f8291f086
'''
import numpy as np

# data I/O
data = open('input.txt', 'r').read() # should be plain text file
print("data: " + data)
chars = list(set(data))
print(chars)
data_size, vocab_size = len(data), len(chars)
print("data has %d characters, %d unique." % (data_size, vocab_size))
char_to_ix = { ch:i for i,ch in enumerate(chars) }
ix_to_char = { i:ch for i,ch in enumerate(chars) }

# hyperparameters
learning_rate = 0.01
hidden_size = 10          # size of vector h - hidden layer of neurons
seq_length = 25           # number of steps to unroll the RNN for

# model parameters
Wxh = np.random.randn(hidden_size, vocab_size) * 0.01
Whh = np.random.randn(hidden_size, hidden_size) *0.01
Wyh = np.random.randn(vocab_size, hidden_size) * 0.01
bh = np.zeros((hidden_size, 1))    # hidden bias
by = np.zeros((vocab_size, 1))     # output bias

# model construction
def lossFun(inputs, targets, hprev):
    # xs: input in different time steps
    # hs: hidden layer in different time steps
    # ys: output probabilities for next chars in different time steps
    # ps: normalized ys
    xs, hs, ys, ps = {}, {}, {}, {} 
    hs[-1] = np.copy(hprev)
    loss = 0
    # forward pass
    for t in range(len(inputs)):
        xs[t] = np.zeros((vocab_size, 1))  # encode in 1-of-k representation
        xs[t][inputs[t]] = 1
        hs[t] = np.tanh(np.dot(Wxh, xs[t]) + np.dot(Whh, hs[t-1] + bh))  # compute the next hidden state
        ys[t] = np.dot(Wyh, hs[t]) + by # compute the probabilities for next chars
        ps[t] = np.exp(ys[t]) / np.sum(np.exp(ys[t]))  # normalized log
        loss += np.log(ps[t][targets[t], 0]) # softmax (cross-entropy loss)
    
    # backward pass (compute the gradients going backwards)
    dWxh, dWhh, dWyh = np.zeros_like(Wxh), np.zeros_like(Whh), np.zeros_like(Wyh)
    dbh, dby = np.zeros_like(bh), np.zeros_like(by)
    dhnext = np.zeros_like(hs[0])
    for t in reversed(range(len(inputs))):
        dy = np.copy(ps[t])

        dy[targets[t]] -= 1 # backprop into y
        dWyh += np.dot(dy, hs[t].T)
        dby += dy
        
        dh = np.dot(Wyh.T, dy) +dhnext   # backprop into h
        dhraw = (1 - hs[t] * hs[t]) * dh # backprop through tanh nonlinearity
        dWhh += np.dot(dhraw, hs[t-1].T)
        dbh += dhraw
        
        dWxh += np.dot(dhraw, xs[t].T)
        dnext = np.dot(Whh.T, dhraw)

    for dparam in [dWxh, dWhh, dWyh, dbh, dby]:
        np.clip(dparam, -5, 5, out=dparam) # clip to mitigate exploding gradients
    
    return loss, dWxh, dWhh, dWyh, dbh, dby, hs[len(inputs)-1]

# sample a sequence of integers from the model
# h is memory state, seed_ix is seed letter for first time step
def sample(h, seed_ix, n):
    x = np.zeros((vocab_size, 1))
    x[seed_ix] = 1
    ixes = []
    for t in range(n):
        h = np.tanh(np.dot(Wxh, x) + np.dot(Whh, h) + bh)
        y = np.dot(Wyh, h) + by
        p = np.exp(y) / np.sum(np.exp(y))
        ix = np.random.choice(range(vocab_size), p=p.ravel())
        x = np.zeros((vocab_size, 1))
        x[ix] = 1
        ixes.append(ix)
    return ixes

n, p = 0 ,0
mWxh, mWhh, mWyh = np.zeros_like(Wxh), np.zeros_like(Whh), np.zeros_like(Wyh)
mbh, mby = np.zeros_like(bh), np.zeros_like(by)
smooth_loss = -np.log(1.0/vocab_size)*seq_length # loss at iteration 0
while True:
    # prepare inputs (we're sweeping from left to right in steps seq_length long)
    if p+seq_length+1 >= len(data) or n == 0: 
        hprev = np.zeros((hidden_size,1)) # reset RNN memory
        p = 0 # go from start of data
    inputs = [char_to_ix[ch] for ch in data[p:p+seq_length]]
    targets = [char_to_ix[ch] for ch in data[p+1:p+seq_length+1]]

    # sample from the model now and then
    if n % 100 == 0:
        sample_ix = sample(hprev, inputs[0], 200)
        txt = ''.join(ix_to_char[ix] for ix in sample_ix)
        print("----\n %s \n----" % txt)

    # forward seq_length characters through the net and fetch gradient
    loss, dWxh, dWhh, dWhy, dbh, dby, hprev = lossFun(inputs, targets, hprev)
    smooth_loss = smooth_loss * 0.999 + loss * 0.001
    if (n % 100 == 0): 
        print("iter %d, loss: %f" % (n, smooth_loss)) # print progress
  
    # perform parameter update with Adagrad
    for param, dparam, mem in zip([Wxh, Whh, Wyh, bh, by], 
                                [dWxh, dWhh, dWhy, dbh, dby], 
                                [mWxh, mWhh, mWyh, mbh, mby]):
        mem += dparam * dparam
        param += -learning_rate * dparam / np.sqrt(mem + 1e-8) # adagrad update

    p += seq_length # move data pointer
    n += 1 # iteration counter 