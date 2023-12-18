class NominalEncoder:
    def __init__(self):
        self.table = None

    def fit(self, values):
        self.table = self.createProbTable(values)

    def createProbTable(self, values) -> dict:
        values = list(values)
        # get element set
        element_set = list(set(values))
        element_set = sorted(element_set)
        # create table
        table = dict()
        for element in element_set:
            table[element] = values.count(element) / len(values)
        return table

    def encode(self, values):
        results = [self.table[element] for element in values]
        return results
    

if __name__=="__main__":
    values = ["A", "A", "B", "A", "B"]
    y_true = [10, 50, 60, 40, 1000]
    encoder = NominalEncoder()
    encoder.fit(values)
    result = encoder.encode(values)
    print(result)