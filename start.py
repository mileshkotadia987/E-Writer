import serial, os, signals, sys, suggestions
from sklearn.externals import joblib

def print_sentence_with_pointer(sentence, position):
	print(sentence)
	print(" "*position + "^")

test_sentence = "pack my box with five dozen liquor jugs"

TRY_TO_PREDICT = False
SAVE_NEW_SAMPLES = False
FULL_CYCLE = False
ENABLE_WRITE = True
TARGET_ALL_MODE = False
AUTOCORRECT = True
DELETE_ALL_ENABLED = False

SERIAL_PORT = "COM10"
BAUD_RATE = 9600
TIMEOUT = 100

target_sign = "a"
current_batch = "0"
target_directory = "data"

current_test_index = 0
arguments = {}

for i in sys.argv[1:]:
	if "=" in i:
		sub_args = i.split("=")
		arguments[sub_args[0]]=sub_args[1]
	else:
		arguments[i]=None

if len(sys.argv)>1:
	if arguments.__contains__("target"):
		target_sign = arguments["target"].split(":")[0]
		current_batch = arguments["target"].split(":")[1]
		print("TARGET SIGN: '{sign}' USING BATCH: {batch}".format(sign=target_sign, batch = current_batch))
		SAVE_NEW_SAMPLES = True
	if arguments.__contains__("predict"):
		TRY_TO_PREDICT = True
	if arguments.__contains__("write"):
		TRY_TO_PREDICT = True
		ENABLE_WRITE = True
	if arguments.__contains__("test"):
		current_batch = arguments["test"]
		TARGET_ALL_MODE = True
		SAVE_NEW_SAMPLES = True
	if arguments.__contains__("noautocorrect"):
		AUTOCORRECT=False
	if arguments.__contains__("port"):
		SERIAL_PORT = arguments["port"]

clf = None
classes = None
sentence = ""
hinter = suggestions.Hinter.load_english_dict()

if TRY_TO_PREDICT:
	print("Loading model...")
	clf = joblib.load('model.pkl')
	classes = joblib.load('classes.pkl')


print("OPENING SERIAL_PORT '{port}' WITH BAUDRATE {baud}...".format(port = SERIAL_PORT, baud = BAUD_RATE))
print("IMPORTANT!")
print("To end the program hold Ctrl+C and send some data over serial")

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout = TIMEOUT)
output = []
in_loop = True
is_recording = False

current_sample = 0
output_file = open("output.txt","w")
output_file.write("")
output_file.close()

if TARGET_ALL_MODE:
	print_sentence_with_pointer(test_sentence, 0)
try:
	while in_loop:
		line = ser.readline().replace("\r\n","")
		if line=="STARTING BATCH":
			is_recording = True
			output = []
			print("RECORDING...",)
		elif line=="CLOSING BATCH":
			is_recording = False
			if len(output)>1:
				print("DONE, SAVING...",)
				if TARGET_ALL_MODE:
					if current_test_index<len(test_sentence):
						target_sign = test_sentence[current_test_index]
					else:
						print("Target All Ended!")
						quit()

				filename = "{sign}_sample_{batch}_{number}.txt".format(sign = target_sign, batch = current_batch, number = current_sample)
				path = target_directory + os.sep + filename
				if SAVE_NEW_SAMPLES == False:
					path = "tmp.txt"
					filename = "tmp.txt"

				f = open(path, "w")
				f.write('\n'.join(output))
				f.close()
				print("SAVED IN {filename}".format(filename = filename))

				current_sample += 1

				if TRY_TO_PREDICT:
					print("PREDICTING...")
					sample_test = signals.Sample.load_from_file(path)

					linearized_sample = sample_test.get_linearized(reshape=True)
					number = clf.predict(linearized_sample)
					char = chr(ord('a')+number[0])
					last_word = sentence.split(" ")[-1:][0]

					if AUTOCORRECT and char.islower():
						predicted_char = hinter.most_probable_letter(clf, classes, linearized_sample, last_word)
						if predicted_char is not None:
							print("CURRENT WORD: {word}, PREDICTED {old}, CROSS_CALCULATED {new}".format(word = last_word, old = char, new = predicted_char))
							char = predicted_char

					if ENABLE_WRITE:
						if char == '-':
							sentence = sentence+" "
						elif char == '~':
							#sentence[-1]=""
							sentence = sentence[:-1]

						elif char == '.':
							sentence = sentence+". "
							#if DELETE_ALL_ENABLED:
								#sentence = ""
							#else:
								#print("DELETE_ALL_ENABLED = FALSE")

						else:

							sentence += char
							print("[{char}] -> {sentence}".format(char = char, sentence = sentence))
							output_file = open("output.txt","w")
							output_file.write(sentence)
							output_file.close()
					else:
						print(char)
			else:
				print("ERROR...")
				current_test_index -= 1

			if TARGET_ALL_MODE:
				current_test_index += 1
				print_sentence_with_pointer(test_sentence, current_test_index)
		else:
			output.append(line)
except KeyboardInterrupt:
	print('CLOSED LOOP!')

ser.close()
