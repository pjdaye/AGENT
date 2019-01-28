

class QualifierList:
    def __init__(self, qualifiers):
        self.qualifiers = qualifiers

    def insert_qualifier(self, qualifier):
        self.qualifiers.insert(0, qualifier)

    def __len__(self):
        return len(self.qualifiers)

    def __iter__(self):
        return self.qualifiers

    def __str__(self):
        return " ".join([str(obs) for obs in self.qualifiers])
