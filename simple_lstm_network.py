import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint

"""
1. load true MIDI training data here

X = <Feed one hot of desired ringtone qualities>

Ringtone qualities:
1. length
2. uplifting
3. complexity
4. urgency

y = <Load preprocessed MIDI sounds as truth data in (n, 4) format>
"""

note_length = 100

X = numpy.random.random(5, )
y = numpy.random.random(note_length, 4)

print(X)
print(y)

# define the LSTM model
model = Sequential()
model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2])))
model.add(Dropout(0.2))
model.add(Dense(4, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam')

# define the checkpoint
filepath = "weights-improvement-{epoch:02d}-{loss:.4f}.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
callbacks_list = [checkpoint]
# fit the model
model.fit(X, y, epochs=20, batch_size=128, callbacks=callbacks_list)

'''
Now let's generate some ringtones using our model!
'''

# load the network weights
filename = "weights-improvement-19-1.9435.hdf5"
model.load_weights(filename)
model.compile(loss='categorical_crossentropy', optimizer='adam')

# Choose qualities for the desired ringtone
length = 1.0
uplifting = 1.0
complexity = 1.0
urgency = 1.0

random_note = numpy.random.random(4, )

justin_note = numpy.array([length, uplifting, complexity, urgency])
output_notes = [numpy.concatenate([justin_note, random_note])]

# generate notes
for i in range(1000):
    prediction = model.predict(output_notes, verbose=0)
    output_notes.append(numpy.concatenate([justin_note, prediction]))

print("\nDone.")
print(numpy.array(output_notes).shape)
