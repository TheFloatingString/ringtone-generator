import numpy as np

from miditoolkit.midi import parser as mid_parser  
from miditoolkit.midi import containers as ct


# create an empty file
mido_obj = mid_parser.MidiFile()
beat_resol = mido_obj.ticks_per_beat

# create an  instrument
track = ct.Instrument(program=0, is_drum=False, name='example track')
mido_obj.instruments = [track]

# create eighth notes
duration = int(beat_resol * 0.5)
prev_end = 0
pitch = 60
for i in range(10):
    # create one note
    start = prev_end
    end = prev_end + duration
    pitch = pitch
    velocity = 50
    note = ct.Note(start=start, end=end, pitch=pitch, velocity=velocity)
    mido_obj.instruments[0].notes.append(note)
    note = ct.Note(start=start, end=end, pitch=pitch+5, velocity=velocity)
    mido_obj.instruments[0].notes.append(note)
    note = ct.Note(start=start, end=end, pitch=pitch+8, velocity=velocity)
    mido_obj.instruments[0].notes.append(note)
    
    # prepare next
    prev_end = end
    pitch += 1

# create makers
marker_hi = ct.Marker(time=0, text='HI')
mido_obj.markers.append(marker_hi)

# write to file
mido_obj.dump('result.midi')

# reload for check
mido_obj_re = mid_parser.MidiFile('result.midi')
for note in mido_obj_re.instruments[0].notes:
    print(note)

print('\nmarker:', mido_obj_re.markers)