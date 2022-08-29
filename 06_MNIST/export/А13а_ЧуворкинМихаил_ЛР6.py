# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'

# %%
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np


# %%
pathToData = '.\\emnist\\'
img_rows = img_cols = 28

def loadBinData(pathToData, img_rows, img_cols): 
    print('Загрузка данных из двоичных файлов...') 
    with open(pathToData + 'imagesTrain.bin', 'rb') as read_binary: 
        x_train = np.fromfile(read_binary, dtype = np.uint8) 
    with open(pathToData + 'labelsTrain.bin', 'rb') as read_binary: 
        y_train = np.fromfile(read_binary, dtype = np.uint8) 
    with open(pathToData + 'imagesTest.bin', 'rb') as read_binary: 
        x_test = np.fromfile(read_binary, dtype = np.uint8) 
    with open(pathToData + 'labelsTest.bin', 'rb') as read_binary: 
        y_test = np.fromfile(read_binary, dtype = np.uint8) 

    x_train = np.array(x_train[16:], dtype = 'float32') / 255 
    x_test = np.array(x_test[16:], dtype = 'float32') / 255
    if flatten or reshape:
        x_train = x_train.reshape(-1, img_rows, img_cols)
        x_test = x_test.reshape(-1, img_rows, img_cols) 
    y_train = y_train[8:]
    y_test = y_test[8:] 
    return x_train, y_train, x_test, y_test 


# %%
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()


x_train = tf.keras.utils.normalize(x_train, axis=1)
x_test = tf.keras.utils.normalize(x_test, axis=1)

y_train_cat = tf.keras.utils.to_categorical(y_train, 10)
y_test_cat = tf.keras.utils.to_categorical(y_test, 10)

model = tf.keras.Sequential()
#model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Reshape((784,)))
model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(10, activation=tf.nn.softmax))

model.compile(	optimizer='adam', 
				loss='categorical_crossentropy', 
				metrics=['accuracy']
				)


history = model.fit(x_train, y_train_cat, epochs=10, batch_size=512)


# %%
fig, axs = plt.subplots(nrows=1, ncols=len(history.history.keys()), constrained_layout=True, figsize=(10, 5))

for ax, key in zip(axs.flat, history.history.keys()):	
	ax.plot(history.history[key])
	ax.set_title(key)
	#ax.set_ylabel(key)
	ax.set_xlabel('epoch')
	ax.legend(['train', 'test'], loc='upper left')
plt.show()

print(model.summary())


# %%
val_loss, val_acc = model.evaluate(x_test, y_test_cat)
print(val_loss, val_acc)


# %%

predictions = model.predict(x_test)
predictions = np.argmax(predictions, axis=1)
print(predictions[0])

plt.imshow(x_test[0], cmap=plt.cm.binary)
plt.show()


# %%
# Выделение неверных вариантов
mask = predictions == y_test

x_false = x_test[~mask]
pred_false = predictions[~mask]
y_false = y_test[~mask]

print("Predicted:", pred_false[:25])
print("From Test:", y_false[:25])

# Вывод первых 25 неверных результатов
fig, axs = plt.subplots(nrows=5, ncols=5, figsize=(10, 10),
                        subplot_kw={'xticks': [], 'yticks': []})

for i, ax in enumerate(axs.flat):
    ax.imshow(x_false[i], cmap=plt.cm.binary)
    ax.set_title(str(pred_false[i]))
plt.tight_layout()
plt.show()


# %%
num_classes = 26
flatten = True
reshape = False

x_train, y_train, x_test, y_test = loadBinData(pathToData, img_rows, img_cols)

y_train -= 1
y_test -= 1

if flatten or reshape:
	x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols).transpose(0,2,1)
	x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols).transpose(0,2,1)
else:
	x_train = x_train.reshape(-1, 784)
	x_test = x_test.reshape(-1, 784)

y_train_cat = tf.keras.utils.to_categorical(y_train, num_classes)
y_test_cat = tf.keras.utils.to_categorical(y_test, num_classes)


# %%
fig, axs = plt.subplots(nrows=1, ncols=10, figsize=(15, 10),
                        subplot_kw={'xticks': [], 'yticks': []})

for i, ax in enumerate(axs.flat):
	sample = x_train[i].reshape(img_rows, img_cols).transpose(1, 0) if not (flatten or reshape) else x_train[i]
	ax.imshow(sample, cmap=plt.cm.binary)
	ax.set_title(chr(y_train[i] + 65))
plt.tight_layout()
plt.show()


# %%
model = tf.keras.Sequential()
if reshape: model.add(tf.keras.layers.Reshape((784,)))
if flatten: model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dropout(0.3))
model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(num_classes, activation=tf.nn.softmax))

model.compile(	optimizer=tf.keras.optimizers.Adam(learning_rate=0.01), 
				loss='categorical_crossentropy', 
				metrics=['accuracy']
				)

history = model.fit(x_train, y_train_cat, epochs=10, batch_size=4096)


# %%
val_loss, val_acc = model.evaluate(x_test, y_test_cat)
print(val_loss, val_acc)


# %%
fig, axs = plt.subplots(nrows=1, ncols=len(history.history.keys()), constrained_layout=True, figsize=(10, 5))

for ax, key in zip(axs.flat, history.history.keys()):	
	ax.plot(history.history[key])
	ax.set_title(key)
	#ax.set_ylabel(key)
	ax.set_xlabel('epoch')
	ax.legend(['train', 'test'], loc='upper left')

plt.show()


# %%
predictions = model.predict(x_test)
predictions = np.argmax(predictions, axis=1)
print(chr(predictions[5] + 65))
sample = x_test[5].reshape(img_rows, img_cols).transpose(1, 0) if not (flatten or reshape) else x_test[5]
plt.imshow(sample, cmap=plt.cm.binary)
plt.show()


# %%
# Выделение неверных вариантов
mask = predictions == y_test

x_false = x_test[~mask]
pred_false = predictions[~mask]
y_false = y_test[~mask]

rs = np.random.randint(0, len(pred_false), 25)

# Вывод первых 25 неверных результатов
fig, axs = plt.subplots(nrows=5, ncols=5, figsize=(10, 10),
                        subplot_kw={'xticks': [], 'yticks': []})

for i, ax in enumerate(axs.flat):
    idx = rs[i]
    sample = x_false[idx].reshape(img_rows, img_cols).transpose(1, 0) if not (flatten or reshape) else x_false[idx]
    ax.imshow(sample, cmap=plt.cm.binary)
    ax.set_title('Pred: ' + chr(pred_false[idx] + 65) + '  Test: ' + chr(y_false[idx] + 65))
plt.tight_layout()
plt.show()


# %%
flatten = True
reshape = False
x_train_emnist, y_train_emnist, x_test_emnist, y_test_emnist = loadBinData(pathToData, img_rows, img_cols)
y_train_emnist += 9
y_test_emnist += 9

(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

x_train = np.concatenate((x_train, x_train_emnist), axis=0)
y_train = np.concatenate((y_train, y_train_emnist), axis=0)
x_test = np.concatenate((x_test, x_test_emnist), axis=0)
y_test = np.concatenate((y_test, y_test_emnist), axis=0)
num_classes = 26 + 10
print(x_train.shape)
print(x_test.shape)

x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
print(x_train.shape)
print(x_test.shape)
input_shape = (img_rows, img_cols, 1)

y_train_cat = tf.keras.utils.to_categorical(y_train, num_classes)
y_test_cat = tf.keras.utils.to_categorical(y_test, num_classes)


# %%
rs = np.random.randint(0, len(x_train), size=10)
fig, axs = plt.subplots(nrows=1, ncols=10, figsize=(15, 10),
                        subplot_kw={'xticks': [], 'yticks': []})

for i, ax in enumerate(axs.flat):
	idx = rs[i]
	sample = x_train[idx] if y_train[idx] < 10 else x_train[idx].transpose(1, 0, 2) 
	tch = chr(y_train[idx] + 48) if y_train[idx] < 10 else chr(y_train[idx] + 55)
	ax.imshow(sample, cmap=plt.cm.binary)  
	ax.set_title(tch)
plt.tight_layout()
plt.show()


# %%
model = tf.keras.Sequential()

model.add(tf.keras.layers.Conv2D(32, kernel_size = (5, 5), strides = (1, 1), padding = 'same', activation = 'relu', input_shape = input_shape))
#model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.MaxPooling2D(pool_size = (2, 2), strides = (2, 2)))

model.add(tf.keras.layers.Conv2D(64, kernel_size = (5, 5), strides = (1, 1), activation = 'relu'))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.MaxPooling2D(pool_size = (2, 2), strides = (2, 2)))

model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(1024, activation = 'relu'))
model.add(tf.keras.layers.Dropout(0.3))
model.add(tf.keras.layers.Dense(16, activation = 'linear'))

model.add(tf.keras.layers.Dense(num_classes, activation = 'softmax'))

model.compile(	optimizer=tf.keras.optimizers.Adam(learning_rate=0.01), 
				loss='categorical_crossentropy', 
				metrics=['accuracy'],
				)

history = model.fit(x_train, y_train_cat,validation_split=0.2, epochs=25, batch_size=2048)


# %%
val_loss, val_acc = model.evaluate(x_test, y_test_cat)
print(val_loss, val_acc)


# %%
fig, axs = plt.subplots(nrows=1, ncols=len(history.history.keys()), constrained_layout=True, figsize=(15, 5))

print(len(history.history.keys()))

for ax, key in zip(axs.flat, history.history.keys()):	
	ax.plot(history.history[key])
	ax.set_title(key)
	#ax.set_ylabel(key)
	ax.set_xlabel('epoch')
	ax.legend(['train', 'test'], loc='upper left')

plt.show()
print(model.summary())


# %%
val_acc_list = []
for i in range(36):
	mask = y_test == i
	val_loss, val_acc = model.evaluate(x_test[mask], y_test_cat[mask])
	ch = chr(i + 48) if i < 10 else chr(i + 55)
	val_acc_list.append(val_acc)
	#print(f'{ch}: ', val_acc)


# %%
for i in range(36):
	ch = chr(i + 48) if i < 10 else chr(i + 55)
	print(f'{ch}: ', val_acc_list[i])


# %%
# Выделение неверных вариантов
show_false = True

if show_false:
    mask = predictions == y_test
    x_false = x_test[~mask]
    pred_false = predictions[~mask]
    y_false = y_test[~mask]
    rs = np.random.randint(0, len(pred_false), 25)
else:
    rs = np.random.randint(0, len(predictions), 25)

# Вывод первых 25 неверных результатов
fig, axs = plt.subplots(nrows=5, ncols=5, figsize=(10, 10),
                        subplot_kw={'xticks': [], 'yticks': []})

for i, ax in enumerate(axs.flat):
    idx = rs[i]
    if show_false:
        sample = x_false[idx] if y_false[idx] < 10 else x_false[idx].transpose(1, 0, 2)   
        pch = chr(pred_false[idx] + 48) if pred_false[idx] < 10 else chr(pred_false[idx] + 55)
        tch = chr(y_false[idx] + 48) if y_false[idx] < 10 else chr(y_false[idx] + 55)
    else:
        sample = x_test[idx] if y_test[idx] < 10 else x_test[idx].transpose(1, 0, 2)   
        pch = chr(predictions[idx] + 48) if predictions[idx] < 10 else chr(predictions[idx] + 55)
        tch = chr(y_test[idx] + 48) if y_test[idx] < 10 else chr(y_test[idx] + 55)
    ax.imshow(sample, cmap=plt.cm.binary)
    ax.set_title('Pred: ' + pch + '  Test: ' + tch)
plt.tight_layout()
plt.show()


# %%
## на этой модели удалось получить точность в 94%
# model = tf.keras.Sequential()

# model.add(tf.keras.layers.Conv2D(32, kernel_size = (3, 3), strides = (1, 1), padding = 'same', activation = 'relu', input_shape = input_shape))
# model.add(tf.keras.layers.BatchNormalization())
# model.add(tf.keras.layers.MaxPooling2D(pool_size = (2, 2), strides = (2, 2), padding = 'same'))
# model.add(tf.keras.layers.Conv2D(32, kernel_size = (3, 3), strides = (1, 1), activation = 'relu'))
# model.add(tf.keras.layers.BatchNormalization())
# model.add(tf.keras.layers.MaxPooling2D(pool_size = (2, 2), strides = (2, 2)))

# model.add(tf.keras.layers.Conv2D(64, kernel_size = (5, 5), strides = (1, 1), activation = 'relu'))
# model.add(tf.keras.layers.BatchNormalization())
# model.add(tf.keras.layers.MaxPooling2D(pool_size = (2, 2), strides = (2, 2)))

# model.add(tf.keras.layers.Flatten())
# model.add(tf.keras.layers.Dense(1024, activation = 'relu'))
# model.add(tf.keras.layers.Dropout(0.5))
# model.add(tf.keras.layers.Dense(16, activation = 'linear'))

# model.add(tf.keras.layers.Dense(num_classes, activation = 'softmax'))

# model.compile(	optimizer=tf.keras.optimizers.Adam(learning_rate=0.01), 
# 				loss='categorical_crossentropy', 
# 				metrics=['accuracy'],
# 				)

# history = model.fit(x_train, y_train_cat,validation_split=0.2, epochs=50, batch_size=6000)


