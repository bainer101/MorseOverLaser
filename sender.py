import morse
ml = morse.MorseConverter()

ml.setup_laser(4)
ml.send("k", 3)
