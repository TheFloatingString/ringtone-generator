import numpy as np 

from miditoolkit.midi import parser as mid_parser
from miditoolkit.midi import containers as ct

class TunaMidiReader:

	def __init__(self):

		self.list_of_notes = []
		self.vector_list_of_notes = []
		self.tuna_mido_obj = None

	def read_midi_file(self, filepath):
		tuna_mido_obj = mid_parser.MidiFile(filepath)

		for i in tuna_mido_obj.instruments:
			for note in i.notes:
				self.list_of_notes.append(note)

		self.vector_list_of_notes = [[Note.start, Note.end, Note.pitch, Note.velocity] for Note in self.list_of_notes]

		self.vector_list_of_notes = sorted(self.vector_list_of_notes, key=lambda x: x[0])

	def return_list_of_notes(self):
		return self.list_of_notes

	def return_vector_list_of_notes(self):
		return self.vector_list_of_notes

if __name__ == '__main__':
	tuna_obj = TunaMidiReader()
	tuna_obj.read_midi_file(filepath="static/input-midi-files/testfile.mid")
	vector_list = tuna_obj.return_vector_list_of_notes()
	print(vector_list)