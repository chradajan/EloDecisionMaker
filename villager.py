class Villager:
    name = ''
    photoPath = ''
    personality = ''
    species = ''
    birthday = ''
    catchphrase = ''

    def __init__(self, n, pp, p, s, b, c):
        self.name = n
        self.photoPath = pp
        self.personality = p
        self.species = s
        self.birthday = b
        self.catchphrase = c

    def __str__(self):
        return "{}\n{}\n{}\n{}\n{}".format(self.name, self.personality, self.species, self.birthday, self.catchphrase)
