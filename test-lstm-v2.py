# Small LSTM Network to Generate Text for Alice in Wonderland
import numpy
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils

from src.read_midi import TunaMidiReader

import numpy as np

from miditoolkit.midi import parser as mid_parser  
from miditoolkit.midi import containers as ct


tuna_obj = TunaMidiReader()
tuna_obj.read_midi_file(filepath="static/input-midi-files/testfile.mid")
vector_list = tuna_obj.return_vector_list_of_notes()

# transform MIDI file
temp_vector_list = [[x[0]/20000, x[1]/20000, x[2]/128, x[3]/128] for x in vector_list]

vector_list = np.asarray(vector_list)

dataX = []
dataY = []

window_size = 3

for i in range(len(vector_list)-window_size-1):
	dataX.append(vector_list[i:i+window_size])
	dataY.append(vector_list[window_size+1])


dataX = np.asarray(dataX)
dataY = np.asarray(dataY)

# define the LSTM model
model = Sequential()
model.add(LSTM(8, input_shape=(dataX.shape[1], dataX.shape[2])))
model.add(Dropout(0.2))
model.add(Dense(dataY.shape[1], activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam')
# define the checkpoint
filepath="weights-improvement-{epoch:02d}-{loss:.4f}.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
callbacks_list = [checkpoint]
# fit the model
model.fit(dataX, dataY, epochs=20, batch_size=2, callbacks=callbacks_list)

init_data = dataX[0]
current_data = init_data.tolist()

results = []

print(dataX.shape)
print(dataY.shape)

for i in range(200):

	print(np.asarray([current_data]).shape)

	prediction = model.predict(np.asarray([current_data]))
	# current_data = current_data.tolist()
	current_data.append(prediction[0])
	current_data = current_data[1:]
	results.append(current_data[-1])


for x in results:
	print(x)



# create an empty file
mido_obj = mid_parser.MidiFile()
beat_resol = mido_obj.ticks_per_beat

# create an  instrument
track = ct.Instrument(program=0, is_drum=False, name='example track')
mido_obj.instruments = [track]

for note in results:
    note = ct.Note(start=round(note[0]*20000), end=round(note[1]*20000), pitch=round(note[2]*128), velocity=round(note[3]*128))
    mido_obj.instruments[0].notes.append(note)


# create makers
marker_hi = ct.Marker(time=0, text='HI')
mido_obj.markers.append(marker_hi)

# write to file
mido_obj.dump('final-predicted-ringtone.midi')