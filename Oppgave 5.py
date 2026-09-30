from random import randrange as rnd
import uuid

class Dart():
    def __init__(self):
        self._spillere = {}
        self._kast_pr_spiller = 3
        self._poeng_range = [0,60]


    def _kast(self):
        poeng = [0,[]]
        for k in range(self._kast_pr_spiller):
            poeng[1].append(rnd(self._poeng_range[0],self._poeng_range[1]))
        poeng[0] = sum(poeng[1])
        return poeng

    def endre_kast_pr_runde(self): #veldig unødvendig, men i tilfelle man skulle få lyst å endre
        while True:
            try:
                antall_kast = int(input("Hvor mange kast skal hver spiller ha per runde?\n"))
                break
            except ValueError:
                print("Ugyldig input! Oppgi antall kast i heltall!")
        self._kast_pr_spiller = antall_kast

#2 Denne biten burde være nok for deloppgave 2:
    def definer_spillere(self):
        while True:
            try:
                antall_spillere = int(input("Hvor mange skal spille?\n"))
                break
            except ValueError:
                print("Ugyldig input! Oppgi antall personer i tall (HELE personer!)!")

        if antall_spillere > 10:
            print("Det er bare plass til ti personer i dartavdelingen i dette establisementet!\nDe andre får komme tilbake senere. :)")
            antall_spillere = 10

        for s in range(antall_spillere):
            _uuid = uuid.uuid4().hex[:8]  #la til uuid så ikke samme navn flere ganger skaper problemer
            navn = input(f"Navn på spiller {s+1}?\n")
            spiller_data = {"navn":navn,
                            "score":0,
                            "runder":[]  #lagrer data for hver pil i hver runde, sånn i tilfelle man vil gjøre noe gøy med den daten
                                  }
            self._spillere[_uuid] = spiller_data

    def spill_en_runde(self):
        for s in self._spillere:
            spiller = self._spillere[s]
            kast = self._kast()
            spiller["score"] += kast[0]
            spiller["runder"].append(kast[1])

    def spill_n_runder(self, n):
        for runde in range(n):
            self.spill_en_runde()

    def vis_score_enkelt(self, spiller): #denne er ikke veldig brukbar uten en meny for å velge spiller fra en liste
        print(f"{spiller} har en score på {self._spillere[spiller]["score"]}!")

    def vis_score_samlet(self):
        rangering = []
        for s in self._spillere:
            spiller = self._spillere[s]
            spiller_res = (spiller["score"], spiller["navn"])
            rangering.append(spiller_res)
            print(f"Spiller: {spiller["navn"]} scoret {spiller["score"]} poeng!")

        for p, s in enumerate(sorted(rangering,reverse=True)[:3]):
            print(f"{p+1}. plass: {s[1]} med {s[0]} poeng!")


game1 = Dart()
#game1.endre_kast_pr_runde() #om man skulle få lyst til å endre kast, er det mulig
game1.definer_spillere()
game1.spill_en_runde()
#game1.spill_n_runder(3)
#game1.vis_score_enkelt("Jan") #denne metoden er litt suspekt, den krever at du vet alias for brukeren på forhånd. Lager en spillerseleksjon hvis jeg får tid.
game1.vis_score_samlet()

#jeg burde strukturere dataene anderledes, eller legge inn en metode for å wipe score i objektet, hvis man vil kalle flere separate set med runder på samme objekt

"""
================================================
Kjøreeksempel 1:
================================================

Hvor mange skal spille?
5
Navn på spiller 1?
Perigrin "för dålig för att kasta sten" Took
Navn på spiller 2?
Gandalf Grå
Navn på spiller 3?
Sauroman
Navn på spiller 4?
Tom Bombadil
Navn på spiller 5?
Barliman Butterbur
Spiller: Perigrin "för dålig för att kasta sten" Took scoret 60 poeng!
Spiller: Gandalf Grå scoret 131 poeng!
Spiller: Sauroman scoret 87 poeng!
Spiller: Tom Bombadil scoret 102 poeng!
Spiller: Barliman Butterbur scoret 145 poeng!
1. plass: Barliman Butterbur med 145 poeng!
2. plass: Gandalf Grå med 131 poeng!
3. plass: Tom Bombadil med 102 poeng!

Process finished with exit code 0

================================================
Kjøreeksempel 2:
================================================

Hvor mange skal spille?
Gollum
Ugyldig input! Oppgi antall personer i tall (HELE personer!)!
Hvor mange skal spille?
3
Navn på spiller 1?
Gandalf
Navn på spiller 2?
Gollum
Navn på spiller 3?
Gollum
Spiller: Gandalf scoret 35 poeng!
Spiller: Gollum scoret 67 poeng!
Spiller: Gollum scoret 107 poeng!
1. plass: Gollum med 107 poeng!
2. plass: Gollum med 67 poeng!
3. plass: Gandalf med 35 poeng!

Process finished with exit code 0
"""