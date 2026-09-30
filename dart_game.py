import math
import random
import matplotlib.pyplot as plt
import numpy as np
from cmath import sqrt
from random import randrange as rnd
import uuid

# Okei.. jeg vet det ble spurt om 2 separate filer her.. og beklager hvis det blir ille gæli
# at jeg leverer bonusoppgavene som én, men jeg tenkte det ikke gjorde noe..
# Jeg kan splitte opp og gjøre den om så den inneholder minimum/kun starter én av oppgavene.
# Men var derfor jeg lagde Besvarelser() klassen, så du kan kjøre de om hverandre (samt en liste med ferdige navn.. fytti jeg ble lei av å skrive navn på slutten xD)

class Dart():
    def __init__(self):
        self._players = {}
        self._darts_pr_round = 3
        self._point_range_simple = [0, 60]
        self._n_rounds = 1
        self._board_radius = 200 #pixels, default verdi
        self._wall_radius = 400  #placeholder, er for evt bergning av treff utenfor skiven


    def one_turn(self):
        points = [0,[]]
        throws = []
        for _ in range(self._darts_pr_round):
            throws.append(self.polar_coords(self.random_hit()))

        for t in throws:
            score = self.real_scoring(t)
            points[1].append(score[1])

        points[0] = sum(points[1])
        return points

    def darts_pr_round(self): #veldig unødvendig, men i tilfelle man skulle få lyst å endre (ser den dukka opp i bonus oppgaven! :3)
        while True:
            try:
                n_darts = int(input("Hvor mange kast skal hver spiller ha per runde?\n"))
                break
            except ValueError:
                print("Ugyldig input! Oppgi antall kast i heltall!")
        print(f"Hver spiller kaster {n_darts} piler per runde.\n")
        self._darts_pr_round = n_darts

#2 Denne biten burde være nok for deloppgave 2:
    def definer_spillere(self, spiller_liste = None):
        # la til metode for å ta imot spiller liste.. ble lei av å skrive inn navn under testing xD
        if isinstance(spiller_liste, list):
            for navn in spiller_liste:
                _uuid = uuid.uuid4().hex[:8]
                self._players[_uuid] = {
                    "navn": navn,
                    "score": 0,
                    "runder": []
                }
            return

        else:
            while True:
                try:
                    antall_spillere = int(input("Hvor mange skal spille?\n"))
                    break
                except ValueError:
                    print("Ugyldig input! Oppgi antall personer i tall (HELE personer!)!")

            if antall_spillere > 10:
                print(
                    "Det er bare plass til ti personer i dartavdelingen i dette establisementet!\nDe andre får komme tilbake senere. :)")
                antall_spillere = 10

            for s in range(antall_spillere):
                _uuid = uuid.uuid4().hex[:8]  # la til uuid så ikke samme navn flere ganger skaper problemer
                navn = input(f"Navn på spiller {s + 1}?\n")
                spiller_data = {"navn": navn,
                                "score": 0,
                                "runder": []
                                # lagrer data for hver pil i hver runde, sånn i tilfelle man vil gjøre noe gøy med den daten
                                }
                self._players[_uuid] = spiller_data


    def one_round(self):
        for s in self._players:
            player = self._players[s]
            kast = self.one_turn()
            player["score"] += kast[0]
            player["runder"].append(kast[1])

    def rounds_to_play(self):
        #for runde in range(n):
        #    self.spill_en_runde()
        while True:
            try:
                n_rounds = int(input("Hvor mange runder skal hver spiller spille?\n"))
                break
            except ValueError:
                print("Ugyldig input! Oppgi antall runder i heltall!")
        print(f"Hver spiller spiller {n_rounds} runder.\n")
        self._n_rounds = n_rounds

    def vis_score_enkelt(self, spiller): #denne er ikke veldig brukbar uten en meny for å velge spiller fra en liste
        print(f"{spiller} har en score på {self._players[spiller]['score']}!")

    def vis_score_samlet(self):
        rangering = []
        for s in self._players:
            spiller = self._players[s]
            spiller_res = (spiller["score"], spiller["navn"])
            rangering.append(spiller_res)
            print(f"Spiller: {spiller["navn"]} scoret {spiller['score']} poeng!")

        for p, s in enumerate(sorted(rangering,reverse=True)[:3]):
            print(f"{p+1}. plass: {s[1]} med {s[0]} poeng!")

    def real_scoring(self, polar_list):
        r = polar_list[0]
        theta = polar_list[1]
        sector_map = [6, 13, 4, 18, 1, 20, 5, 12, 9, 14,
                      11, 8, 16, 7, 19, 3, 17, 2, 15, 10]

        #Radius ratioer:
        R_BULL_INNER = 0.0374 # max, indre bullseye
        R_BULL_OUTER = 0.0935 # max, yttre bullseye
        R_TRIPLE_0 = 0.5606   # min, trippel
        R_TRIPLE_1 = 0.6294   # max, trippel
        R_DOUBLE_0 = 0.9529   # min, dobbel
        R_DOUBLE_1 = 1.0000   # max, dobbel

        if r < R_BULL_INNER: return "Inner Bull!!", 50
        if r < R_BULL_OUTER: return "Outer Bul!", 25
        if r > R_DOUBLE_1:   return "Miss!", 0

        segment = ((theta + 9) // 18) % 20 #skal gi 0-19
        board_value = sector_map[segment]

        if R_TRIPLE_0 <= r <= R_TRIPLE_1:
            return ["Triple", board_value * 3]
        elif R_DOUBLE_0 <= r <= R_DOUBLE_1:
            return ["Double", board_value * 2]
        else:
            return ["Single", board_value * 1]

    def polar_coords(self, xy):
        x = xy[0]
        y = xy[1]
        theta_rad = math.atan2(y, x)
        theta_deg = round(math.degrees(theta_rad) % 360) #runder til nærmeste hele grad
        radius = math.sqrt(x ** 2 + y ** 2)
        r_ratio = radius / self._board_radius  #regner ut r ratioen. {r fra center}/{r til ytterkant}: <=1 er ett treff, >1 bom.

        return r_ratio, theta_deg

    def faulty_random_hit(self): # tilfeldig x og y, basert på dartskivens radius #denne fikk en forferdelig fordeling med opphoping rundt min og maks x
        rand_x = random.uniform(-self._board_radius, self._board_radius) #lager en tilfeldig x i def{dart tavle}
        max_y = math.sqrt(self._board_radius**2 - rand_x**2)             #finner max y i tavla basert på x
        rand_y = random.uniform(-max_y, max_y)                           #lager en tilfeldig y basert på max y
        return rand_x, rand_y

    def random_hit(self):
        r = self._board_radius * math.sqrt(random.random())
        theta_rad = random.uniform(0, 2 * math.pi)

        rand_x = r * math.cos(theta_rad)
        rand_y = r * math.sin(theta_rad)

        return rand_x, rand_y

    def play_simple(self, spiller_liste):
        self.definer_spillere(spiller_liste)
        self.darts_pr_round()
        self.rounds_to_play()

        for r in range(self._n_rounds):
            self.one_round()

        self.vis_score_samlet()

    def play_301(self, spiller_liste):
        self.definer_spillere(spiller_liste)
        self.darts_pr_round()

        players_301 = {}
        for uuid_key, player in self._players.items():
            players_301[uuid_key] = {
                "navn" : player["navn"],
                "score": 301,
                "has_doubled_in": False,
                "round_hist": [],
                "total_rounds":0,
                "total_kast":0
            }
        winner = ""
        game_over = False
        while not game_over:

            for uuid_key, player in players_301.items():
                start_of_turn_score = player["score"]

                round_score = [301,[]]
                for _ in range(self._darts_pr_round):
                    kast = self.polar_coords(self.random_hit())
                    score = self.real_scoring(kast)

                    new_score = (player["score"] - score[1])
                    if not player["has_doubled_in"]:
                        if score[0] == "Double":
                            player["has_doubled_in"] = True
                            player["score"] = new_score
                            round_score[1].append(score)
                        else:
                            round_score[1].append(["No Double",0])
                    elif new_score == 1 or new_score < 0:
                        round_score[1].append(["BUST",0])
                        player["score"] = start_of_turn_score
                        round_score[0] = start_of_turn_score
                        break
                    elif new_score ==0:
                        if not score[0] == "Double":
                            round_score[1].append(["BUST", 0])
                            player["score"] = start_of_turn_score
                            round_score[0] = start_of_turn_score
                            break
                        else:
                            round_score[1].append(score)
                            game_over = True
                            winner = uuid_key
                            print(f"Spiller {player['navn']} har vunnet!")
                    else:
                        round_score[1].append(score)
                        player["score"] = new_score
                    player["total_kast"] += 1
                    if game_over: break

                round_score[0] = player["score"]
                player["total_rounds"] +=1
                player["round_hist"].append(round_score)
                if game_over: break

        #victory_stats = f"De vant på runde {players_301[winner]['total_rounds']}, med {players_301[winner]['total_kast']} kast!\n"
        #congrats = f"GRATULERER {players_301[winner]['navn'].upper()} ! ! !"
        #print(victory_stats)
        #print(f"\n\n{congrats:^{len(victory_stats)}}")

        #brukte ai til å generere en seiers oppsummering med litt mer futt i.
        self.print_vinner_fanfare(players_301[winner]['navn'],players_301[winner]['total_rounds'],players_301[winner]['total_kast'])

        show_score = False
        while True:
            name_choice = input("Vil du se detaljert runde info for vinneren? (y/n)").lower()
            try:
                if name_choice == "n": break
                elif name_choice == "y" or name_choice == "j": show_score = True; break
            except ValueError:
                print("Du kan ikke sitte på gjerdet, (j)a eller (n)ei, takk!")
        if show_score:
            for round in players_301[winner]['round_hist']:  # ta vekk kommentaren på denne løkka for å få utskrift av rundehistorikk
                print(round)

    def print_vinner_fanfare(self, spiller_navn, runder, totalt_kast): #denne genererte jeg med gemini
        bredde = 45
        print("\n" + "=" * bredde)
        print("🎉 " * ((bredde - 2) // 4))
        print(f"Spiller {spiller_navn} har vunnet!".center(bredde))
        print(f"De vant på runde {runder}, med {totalt_kast} kast!".center(bredde))
        print("-" * bredde)
        print(f"GRATULERER {spiller_navn.upper()} ! ! !".center(bredde))
        print("🏆 " * ((bredde - 2) // 4))
        print("=" * bredde + "\n")



# Angående randomisering, valgte å lage en litt mer "realistisk" metode ved å lage en random x,y og gå via polar koordinater
# istedenfor f.eks. sector = randrange(0,20) og f.eks rand_seg = rand(1, 5), segments = [1,2,3,25,50],
# for så å kjøre noen if sjekker eller kalle på resultat i ett dict, f.eks results = {"50": 50, "1": lambda x: x*1, ...} (ikke riktig struktur der, men er for å illustrere tankegang)
# Tanken er også at jeg kan lage et ui som tar x og y koordinater fra klikk. derfor lagde jeg likegodt metoder for å håndtere
# dette fra starten av
#
# Brukte ai til å lage denne ploteren (det er lenge siden jeg har brukt pyplot x) ),
# det ble stilt spørsmål ved de opprinnelige rng modellen jeg hadde
# så jeg la inn dette for å gjøre en sjekk, og sant nok, metoden min hadde clustering rundt min og max x.

    def plot_hits(self, n, model):
        xs = []
        ys = []
        for _ in range(n):
            random = model()
            xs.append(random[0])
            ys.append(random[1])

        plt.scatter(xs,ys, alpha=0.5, s=10)
        plt.title("Spredning av kast")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.axis("equal")
        plt.xlim(-200, 200)
        plt.ylim(-200, 200)
        vinkel = np.linspace(0, 2 * np.pi, 200)
        sirkel_x = 200 * np.cos(vinkel)
        sirkel_y = 200 * np.sin(vinkel)
        plt.plot(sirkel_x, sirkel_y, color='red', linewidth=2, label="Skivekant (R=200)")
        plt.gca().set_aspect('equal', adjustable='box')
        plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
        plt.axvline(0, color='black', linewidth=0.8, linestyle='--')
        plt.grid(True, linestyle=':', alpha=0.6)
        plt.show()

        plt.hist(xs, bins=30)
        plt.title("fordeling av x-verdier")
        plt.show()


#testing av randomisering, fjern kommentarene hvis du vil sjekke forskjellene
#rand_test = Dart()
#rand_test.plot_hits(10000, rand_test.faulty_random_hit)
#rand_test.plot_hits(10000, rand_test.random_hit)


class Besvarelser(): # vibe-code'a bare sammen denne
    def __init__(self):
        spiller_liste = ["Brannmann Sam", "Kaptein Sabeltann", "Pelle Propell", "alle bompi bjørnene", "Postman Pat",
                         "Toget Thomas", "Skeletor"]
        egendefinerte_navn = True
        while True:
            name_choice = input("Vil du bruke pregenerete spillere? (y/n)").lower()
            try:
                if name_choice == "n":
                    egendefinerte_navn = False; break
                elif name_choice == "y" or name_choice == "j":
                    break
            except ValueError:
                print("Du kan ikke sitte på gjerdet, (j)a eller (n)ei, takk!")

        #dart = Dart()

        self.oppgaver = {
            "Bonusoppgave 1": lambda: self.dart.play_simple(spiller_liste if egendefinerte_navn else None),
            "Bonusoppgave 2": lambda: self.dart.play_301(spiller_liste if egendefinerte_navn else None),
            "Avslutt program": exit
        }
    def gen_dart_instance(self):
        new_instance = self.dart_instance = Dart()
        return new_instance

    def besvar(self):

        header_width = 50
        line = "="*header_width
        header = f"{line}\n{'BONUSOPPGAVER':^{header_width}}\n{line}"
        space = f"||{' ' * (header_width - 4)}||"
        innhold = []

        for idx, (tittel, funksjon) in enumerate(self.oppgaver.items(), start=1):
            valg = f"{idx}. {tittel}"
            rendering = f"||{valg:^{header_width - 4}}||"
            innhold.append(rendering)
        menu = [header, space]
        for e in innhold:
            menu.append(e)
        menu.extend([space, line])

        while True:
            self.dart = self.gen_dart_instance()
            print("\n".join(menu))
            try:
                valg_idx = int(input("\nVelg menyvalg: ")) - 1
            except ValueError:
                print("Velg ett tall fra menyen er du snill :3")

            valgt_tittel = list(self.oppgaver.keys())[valg_idx]

            self.oppgaver[valgt_tittel]()
            self.dart = None



#Dart().play_simple()

#Dart().play_301()
Besvarelser().besvar()