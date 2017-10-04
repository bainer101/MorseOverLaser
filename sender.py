import morse
ml = morse.MorseConverter()

ml.setup(4)
ml.send("k", multiplier=3)
