import os, shutil
import config
import sys
import threading
import time

class Observer():

	def __init__(self):

		self.modes = {
			"default_mode": self.default_mode,
			"remove_mode": self.remove_mode
		}

		self.before = os.listdir(config.paths["work"])
		self.after = None
		self.source_file = None # Begins with the 2nd if 1st input is not on workpath aor unspecified on config

		self.file_index = 0
		self.old_file = None
		self.new_file = None


	def define_newer_file(self):		
		"""Define the newer file to decide its destination directory"""
		f0 = os.path.getctime((config.paths["work"] + "\\" + self.after[0]))
		f1 = os.path.getctime((config.paths["work"] + "\\" + self.after[1]))

		if f0 > f1:
			self.new_file = self.after[0]
			self.old_file = self.after[1]
		else:
			self.new_file = self.after[1]
			self.old_file = self.after[0]


	def wait_for_file_release(self):
		"""Once a new file is created it waits for posible use for another process"""
		free = False

		while not free:
			time.sleep(0.5) # Wait to reduce resources compsumption...
			try:
				# The newer file is moved and renamed, the old file is deleted on the work path.
				shutil.move(
					src=config.paths["work"] + "\\" + self.new_file, 
					dst=config.paths["destination"] + "\\" + self.new_file)
				shutil.move(
					src=config.paths["destination"] + "\\" + self.new_file, 
					dst=config.paths["destination"] + "\\" + self.old_file)
				os.remove(config.paths["work"] + "\\" + self.old_file)
				free =  True

			except:
				free = False
				print( "Esperando liberacion del archivo...")


	def run(self, mode):



		while True:

			self.after = os.listdir(config.paths["work"])
			if self.after != self.before and len(self.after) == 2:

				self.define_newer_file()
				self.wait_for_file_release()

				self.modes[mode]()

				self.copy_source_to_workpath()

			elif len(self.after) == 0 and self.source_file is None:
				self.source_file = config.replacements[0] + config.file["ext"]
				self.copy_source_to_workpath()


			self.before = self.after


	def copy_source_to_workpath(self):
		try:
			shutil.copyfile(
			src=config.paths["source"] + "\\" + self.source_file, 
			dst=config.paths["work"] + "\\" + self.source_file)	
		except Exception as e:
			print(f"Archivo inexistente - {e}")
			print("Finalizado")


	def default_mode(self):
		"""Next file to process on lineal mode"""
		self.source_file = self.plus_one(self.old_file[:-4]) + config.file["ext"]


	def remove_mode(self):
		"""Next file to process on specific mode"""
		self.file_index += 1
		self.source_file = config.replacements[self.file_index] + config.file["ext"]
		

	def plus_one(self, number):
		next_number = str(int(number) + 1)
		zeros = (len(number) - len(next_number)) * "0"
		return zeros + next_number