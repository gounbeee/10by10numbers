
# POLYMORPHISM AND DUCK TYPING
# https://opensource.com/article/20/5/duck-typing-python

# ABOUT TYPE
# : A dynamically typed language like Python works differently.
#   Here you can think of the variable name, not like a box but
#   rather analogous to a "tag" (somewhat like a price tag in a store).
#   So, the tag does not have a type. Rather, if you ask the tag what
#   its type is, it would probably pick the object it is tagged to at
#   that moment. Why I say "at that moment" is because, just like in the
#   real world, a tag attached to a shoe could also be attached to some
#   other item at a different time. So the Python interpreter does not
#   assign any type to a variable name, per se. But if you ask a variable
#   name its type, then it will give you the type of the object it is
#   currently tied to. This is dynamic typing.
#
# ABOUT DUCK-TYPING
# : Python is clever, though, and it uses the "duck test": if a variable
#   walks like a duck and talks like a duck, then it is a duck. In other
#   words, Applied to computer science, that means Python examines data
#   to determine its type. Python knows that integers are used for math
#   and words are used in communication, so the programmer doesn't have
#   to explain to Python how to use the data it finds in variables. Python
#   uses duck typing to figure it out on its own, and does not attempt to
#   do math on strings or print the contents of arrays (without iteration),
#   and so on.
#
#
#
class AudioFile:

    def __init__(self, filename):
        if not filename.endswith(self.ext):
            raise Exception("Invalid file format")
        self.filename = filename



class MP3File(AudioFile):
    ext = "mp3"
    def play(self):
        #####print(("playing {} as mp3".format(self.filename))
        pass

class WavFile(AudioFile):
    ext = "wav"
    def play(self):
        #####print(("playing {} as wav".format(self.filename))
        pass

class OggFile(AudioFile):
    ext = "ogg"

    def play(self):
        #####print(("playing {} as ogg".format(self.filename))
        pass

# BELOW IS THE PRACTICE OF 'DUCK-TYPING'
# SO THIS CLASS DOES NOT INHERIT THE AudioFile CLASS
class FlacFile:
    def __init__(self, filename):
        if not filename.endswith(".flac"):
            raise Exception("Invalid file format")

        self.filename = filename

    def play(self):
        #####print(("playing {} as flac".format(self.filename))
        pass





ogg = OggFile("myfile.ogg")
ogg.play()


flac = FlacFile("file.flac")
flac.play()