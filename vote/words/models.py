from django.db import models


class WordManager(models.Manager):
    def xkcd_pw(self, n):
        return "".join([x.data for x in self.order_by('?')[:n]])


class Word(models.Model):
    data = models.CharField(max_length=20, primary_key=True)
    objects = WordManager()


def load_words(filename):
    i = 0
    with open(filename, 'r') as f:
        for line in f.readlines():
            word = line.strip().replace("'", "").replace("-", "").title()
            if len(word) > 3 and len(word) < 10:
                try:
                    w = Word(data=word)
                    w.save()
                    i += 1
                except:
                    pass
    print i, "words loaded"
