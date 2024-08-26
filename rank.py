import pickle
import os


class Rank:
    def __init__(self):
        self.directory = './data'
        self.filepath = os.path.join(self.directory, 'ranking_list')

        # Check if the directory exists, create it if not
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

        # Check if the file exists, create it with an empty list if not
        if not os.path.exists(self.filepath):
            file = open(self.filepath, 'wb')
            file.write(pickle.dumps([]))
            file.close()

    def add(self, score):
        with open(self.filepath, 'rb') as f:
            ranking = pickle.loads(f.read())
        ranking.append(score)
        ranking.sort(reverse=True)

        with open(self.filepath, 'wb') as f:
            f.write(pickle.dumps(ranking))

    def get_list(self):
        with open(self.filepath, 'rb') as f:
            ranking = pickle.loads(f.read())
        return ranking