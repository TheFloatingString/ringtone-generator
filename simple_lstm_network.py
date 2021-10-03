import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint

from src.read_midi import TunaMidiReader
import glob

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

list_of_files = glob.glob("static/input-midi-files/*.mid")

raw_ringtones = []

for filename in list_of_files:
    tuna_obj = TunaMidiReader()
    tuna_obj.read_midi_file(filename)
    raw_ringtones.append((tuna_obj.return_vector_list_of_notes()))

window_size = 5

X_data = []
y_data = []

ringtone = raw_ringtones[0]


for index, item in enumerate(ringtone):
    if index + window_size < len(ringtone):
        X_data.append(ringtone[index:index + window_size])
        y_data.append([ringtone[index + window_size]])

X_data = numpy.array(X_data)
X_data = numpy.reshape(X_data, (len(X_data), window_size, 4))

# note_length = 100

# X = numpy.random.random(5, )
# y = numpy.random.random(note_length, 4)

# print(X)
# print(y)

# define the LSTM model
model = Sequential()
model.add(LSTM(256, input_shape=(155, 5, 4)))
model.add(Dropout(0.2))
model.add(Dense(4, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam')

# define the checkpoint
filepath = "weights-improvement-{epoch:02d}-{loss:.4f}.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
callbacks_list = [checkpoint]
# fit the model
model.fit(X_data, y_data, epochs=20, batch_size=10, callbacks=callbacks_list)

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

justin_note = ([length, uplifting, complexity, urgency])
output_notes = [numpy.concatenate([justin_note, random_note])]

# generate notes
for i in range(1000):
    prediction = model.predict(output_notes, verbose=0)
    output_notes.append(numpy.concatenate([justin_note, prediction]))

print("\nDone.")
print((output_notes).shape)
