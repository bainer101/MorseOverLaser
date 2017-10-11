import morse
ml = morse.MorseConverter()

ml.setup_laser(4, 3)
ml.send("k")
