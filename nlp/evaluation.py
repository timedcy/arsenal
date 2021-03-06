from __future__ import division

from collections import defaultdict
class F1:

    def __init__(self, confusion_matrix=False):
        if confusion_matrix:
            self.confusion_matrix = defaultdict(lambda : defaultdict(int))
        else:
            self.confusion_matrix = None
        self.n_examples = 0
        self.relevant  = defaultdict(set)
        self.retrieved = defaultdict(set)

    def report(self, instance, prediction, target):
        if self.confusion_matrix is not None:
            self.confusion_matrix[target][prediction] += 1
        self.n_examples += 1
        self.add_relevant(target, instance)
        self.add_retrieved(prediction, instance)

    def add_relevant(self, label, instance):
        self.relevant[label].add(instance)

    def add_retrieved(self, label, instance):
        self.retrieved[label].add(instance)
        return instance in self.relevant[label]

    def scores(self, verbose=True):
        relevant  = self.relevant
        retrieved = self.retrieved
        if verbose:
            #from prettytable import PrettyTable
            #t = PrettyTable(["","P","R","F"])
            #x.set_field_align("City name", "l") # Left align city names        
            print ' ============================================'
            print ' |          |   C   |   P   |   R   |   F   |'
            print ' |==========================================|'
        tbl = []
        labels = self.relevant.keys()
        labels.sort()
        for label in labels:
            R = P = F = 0
            count = len(relevant[label])
            top = relevant[label] & retrieved[label]
            if len(relevant[label]) != 0:
                R = len(top) / len(relevant[label])
            if len(retrieved[label]) != 0:
                P = len(top) / len(retrieved[label])
            if P + R != 0:
                F = 2*P*R / (P + R)
            if verbose:
                print ' | %8s | %5d | %5.1f | %5.1f | %5.1f |' % (label[:8], count, P*100, R*100, F*100)
                #t.add_row([label, P*100, R*100, F*100])
            tbl.append((label,count,P,R,F))
        if verbose:
            print ' ============================================'
            #print t
        return tbl

    def confusion(self):
        assert self.confusion_matrix is not None
        for t, predictions in self.confusion_matrix.iteritems():
            incorrect = sum(cnt for p,cnt in predictions.items() if t != p)
            print '%s [correct: %s; incorrect: %s]' % (t, predictions[t], incorrect)
            for predicted, cnt in predictions.iteritems():
                if t != predicted:
                    incorrect += cnt
                    print '      %6s -> %s' % (predicted, cnt)
            print
