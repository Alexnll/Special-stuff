from mxnet import nd, init, autograd
from mxnet.gluon import data as gdata, nn, loss as gloss
from mxnet import gluon
import matplotlib.pyplot as plt

'''
p1 = nd.array([0.96, 2.89, 6.04, 10.57, 16.49, 26.66, 40.12, 54.78, 75.51, 100.4, 125.4])
q1 = nd.array([0.621, 1.12, 1.62, 2.09, 2.55, 3.14, 3.63, 4.06, 4.5, 4.92, 5.29])
p2 = nd.array([0.68, 2.14, 5.76, 11.05, 18.13, 26.74, 40.96, 57.75, 74.99, 97.59, 124.3])
q2 = nd.array([0.275, 0.592, 1.06, 1.49, 1.92, 2.31, 2.8, 3.22, 3.6, 4.01, 4.4])
p3 = nd.array([0.786, 1.81, 5.07, 12, 20.83, 31.4, 43.45, 62.09, 82.59, 102.9, 128.3])
q3 = nd.array([0.124, 0.249, 0.524, 0.916, 1.28, 1.62, 1.93, 2.34, 2.72, 3.03, 3.38])
'''
p1 = nd.array([0.213,0.64,1.39,3.03,5.67,12.66,31.99,44.79,62.45,81.41,106.1,126.4])
q1 = nd.array([1.13,1.74,2.28,2.89,3.37,3.96,4.58,4.8,5.05,5.27,5.51,5.68])
p2 = nd.array([0.6,1.71,3.55,7.13,12.08,22.57,45.85,59.77,78.28,98.03,123.5])
q2 = nd.array([1.12,1.71,2.23,2.79,3.22,3.72,4.26,4.48,4.71,4.92,5.15])
p3 = nd.array([2.03, 5.16, 9.69, 17.02, 25.74, 39.89, 67.07, 82.17, 102, 122.5])
q3 = nd.array([1.09, 1.63, 2.09, 2.56, 2.91, 3.33, 3.8, 4, 4.22, 4.44])




plt.figure(figsize=(15, 5))


def training1(features, labels, position, fire_point, title, batch_size=11):
    dataset = gdata.ArrayDataset(features, labels)
    data_iter = gdata.DataLoader(dataset, batch_size, shuffle=True)
    net = nn.Sequential()
    net.add(nn.Dense(1))
    net.initialize()
    loss = gloss.L2Loss()
    trainer = gluon.Trainer(net.collect_params(), 'sgd', {'learning_rate': 0.01})
    epoch = 0
    m = 100
    m1 = -100
    m2 = 100
    while (m2 - m1)**2 > 0.000000000000001:
        if epoch != 0:
            m1 = m2
        epoch += 1
        for X, y in data_iter:
            with autograd.record():
                l = loss(net(X), y)
            l.backward()
            trainer.step(batch_size)
        l = loss(net(features), labels)
        if epoch % 100 == 0 or epoch == 1:
            print('epcoh: %d  loss: %s' % (epoch, l.mean().asscalar()))
        m2 = l.mean().asscalar()
        m = l.mean().asscalar()

    print("epoch:" + str(epoch))
    print("m: " + str(m))
    print("w: " + str(net[0].weight.data().asnumpy()))
    print("b: " + str(net[0].bias.data().asnumpy()))
    print("error square: " + str(((net(features).reshape(batch_size, 1) - labels.reshape(batch_size, 1)) ** 2).sum().asscalar()))

    p_test = nd.arange(0, 1/fire_point, 0.1)
    q_test = net(p_test)
    plt.subplot(1, 3, position)
    plt.scatter(features.asnumpy(), labels.asnumpy(), color='#FF4700')
    plt.plot(p_test.asnumpy(), q_test.asnumpy(), color='b')
    plt.xlabel("1/p (1/kPa)")
    plt.ylabel("1/q (g carbon/mmol)")
    plt.title(title)


def training2(features, labels, position, fire_point, title, batch_size=11):
    dataset = gdata.ArrayDataset(features, labels)
    data_iter = gdata.DataLoader(dataset, batch_size, shuffle=True)
    net = nn.Sequential()
    net.add(nn.Dense(1))
    net.initialize()
    loss = gloss.L2Loss()
    trainer = gluon.Trainer(net.collect_params(), 'sgd', {'learning_rate': 0.01})
    epoch = 0
    m = 100
    while epoch < 1000:
        epoch += 1
        for X, y in data_iter:
            with autograd.record():
                l = loss(net(X), y)
            l.backward()
            trainer.step(batch_size)
        l = loss(net(features), labels)
        if epoch % 100 == 0 or epoch == 1:
            print('epcoh: %d  loss: %s' % (epoch, l.mean().asscalar()))
        m = l.mean().asscalar()

    print("epoch:" + str(epoch))
    print("m: " + str(m))
    print("w: " + str(net[0].weight.data().asnumpy()))
    print("b: " + str(net[0].bias.data().asnumpy()))
    print("error square: " + str(((net(features).reshape(batch_size, 1) - labels.reshape(batch_size, 1)) ** 2).sum().asscalar()))

    p_test = nd.arange(0, 1/fire_point, 0.1)
    q_test = net(p_test)
    plt.subplot(1, 3, position)
    plt.scatter(features.asnumpy(), labels.asnumpy(), color='#FF4700')
    plt.plot(p_test.asnumpy(), q_test.asnumpy(), color='b')
    plt.xlabel("1/p (1/kPa)")
    plt.ylabel("1/q (g carbon/mmol)")
    plt.title(title)


training1(1/p1, 1/q1, 1, 0.213, "Ethane on AC (10℃)")
training1(1/p2, 1/q2, 2, 0.6, "Ethane on AC (30℃)")
training1(1/p3, 1/q3, 3, 2.03, "Ethane on AC (60℃)", 10)
plt.show()
