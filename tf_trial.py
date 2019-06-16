import numpy as np
import tensorflow as tf

N, D, H = 64, 1000, 100

x = tf.placeholder(tf.float32, shape=(N, D))  # will change in different iteratiom, so we dont want them in the graph
y = tf.placeholder(tf.float32, shape=(N, D))  # placeholder is outside the graph
#0 w1 = tf.placeholder(tf.float32, shape=(D, H))
#1 w1 = tf.Variable(tf.float32, shape=(D, H)) # Variables live inside the graph, neew init
#0 w2 = tf.placeholder(tf.float32, shape=(H, D))
#1 w2 = tf.Variable(tf.float32, shape=(H, D))

init = tf.contrib.layers.xavier_initializer()
h = tf.layers.dense(inputs=x, units=H, activation=tf.nn.relu, kernel_initializer=init)
y_pred = tf.layers.dense(inputs=h, units=D, kernel_initializer=init)

#1 h = tf.maximum(tf.matmul(x, w1), 0)
#1 y_pred = tf.maximum(tf.matmul(h, w2), 0)
#1 diff = y_pred - y
#1 loss = tf.reduce_mean(tf.reduce_sum(diff**2, axis=1))
#1 grad_w1, grad_w2 = tf.gradients(loss, [w1, w2])
loss = tf.loss.mean_squared_error(y_pred, y) # predefined in


#1 Learning_rate = 1e-5
#1 new_w1 = w1.assign(w1 - Learning_rate*grad_w1) # add assign operations to update w1 and w2 as part of the graph
#1 new_w2 = w2.assign(w2 - Learning_rate*grad_w2) # the assign operation live into the graph
#1 updates = tf.group(new_w1, new_w2) # important

optimizer = tf.train.GradientDescentOptimizer(1e-5)
updates = optimizer.minimize(loss) # mark w1 and w2 as tranable by default

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer()) # run graph once to initialize w1 and w2
    values = {x: np.random.randn(N, D),  # now only feed the x and y to the graph
    y: np.random.randn(D, H), 
#0    w1: np.random.randn(H, N),
#0    w2: np.random.randn(N, D),
    }

#    Learning_rate = 1e-5
    for t in range(50):
        loss_val, = sess.run([loss, updates], feed_dict=values)
#0       out = sess.run([loss, grad_w1, grad_w2], feed_dict=values)
#0       loss_val, grad_w1_val, grad_w2_val = out # every time will give the grade to the numpy array, may be expensive
#0       value[w1] -= Learning_rate*grad_w1_val
#0       value[w2] -= Learning_rate*grad_w2_val