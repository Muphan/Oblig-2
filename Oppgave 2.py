


class ODDER_FODDER:
    def __init__(self, odd_0=9, odd_n=101):
        self.odd_0 = odd_0
        self.odd_n = odd_n

        self.odd_list = [["For loop:"],["While loop:"]]

        self.populate_list(self.odd_0, self.odd_n)
        self.print_list()

    def for_write_odds(self, o_0, o_n):
        for odd in range(o_0, o_n+1, 2):
            self.odd_list[0].append(odd)

    def while_write_odds(self, o_0, o_n):
        teller = o_0
        while teller <= o_n:
            self.odd_list[1].append(teller)
            teller += 2

    def populate_list(self, o_0, o_n):
        self.for_write_odds(o_0, o_n)
        self.while_write_odds(o_0, o_n)

    def print_list(self):
        w = 12
        header = f"{self.odd_list[0][0]:^{w}} | {self.odd_list[1][0]:^{w}}"
        line = "="*len(header)
        print(header)
        print(line)
        for fo, wh in zip(self.odd_list[0][1:], self.odd_list[1][1:]):
            print(f"{fo:^{w}} | {wh:^{w}}")


#kunne bakt inn en prompt-funksjon så den kunne spurt bruker om min-max verdier, men valgte å
#ikke bruke tid på dette, har du lyst kan du fôre andre verdier rett i ODDER_FOODER(x, y) :3


ODDER_FODDER()

"""
================================================
Kjøreeksempel:
================================================

 For loop:   | While loop: 
===========================
     9       |      9      
     11      |      11     
     13      |      13     
     15      |      15     
     17      |      17     
     19      |      19     
     21      |      21     
     23      |      23     
     25      |      25     
     27      |      27     
     29      |      29     
     31      |      31     
     33      |      33     
     35      |      35     
     37      |      37     
     39      |      39     
     41      |      41     
     43      |      43     
     45      |      45     
     47      |      47     
     49      |      49     
     51      |      51     
     53      |      53     
     55      |      55     
     57      |      57     
     59      |      59     
     61      |      61     
     63      |      63     
     65      |      65     
     67      |      67     
     69      |      69     
     71      |      71     
     73      |      73     
     75      |      75     
     77      |      77     
     79      |      79     
     81      |      81     
     83      |      83     
     85      |      85     
     87      |      87     
     89      |      89     
     91      |      91     
     93      |      93     
     95      |      95     
     97      |      97     
     99      |      99     
    101      |     101     

Process finished with exit code 0
==================================================


"""