class THE_MEANING:
    def __init__(self):
        self.THE_ANSWER = 42
        self.translations = ["førtito", "toogførti", "fortytwo", "forty-two"]
        #Vurderte å legge inn en sjekk for å se om input er ett matematisk uttrykk som gir 42,
        #men bestemte meg for å spare tid x3

        self.check_if_valid()

    def prompt_user(self): #Som ble påpekt ved oblig 1, holder user prompts utenfor __init__ :)
        answer = input("Hva er svaret på det ultimate spørsmålet om livet, universet og alle ting?\nHINT: Det er ett tall.\n")
        return answer

    def type_check(self):
        a = self.prompt_user()
        try:
            a_int = int(a)
            return [a_int]
        except (ValueError, TypeError):
            pass
        if isinstance(a, str):
            parsed_input = a.lower().replace(" ", "")
            if parsed_input in self.translations:
                return [42, a.lower()]
        return [False, "FEIL!"]

    def check_if_valid(self):
        a = self.type_check()
        if a[0] == 42:
            print(f"Det stemmer! Meningen med livet er {a[-1]}!")
            # Her blir det litt rar visning hvis input f.eks er "før ti     to"
            # siden jeg ikke fjerner mellomrommene i printen.
            # Mest pga tilfeller som "To og førti", mulig løsning hadde vært å bruke "-"
            # Men det kan også gi litt rare svar, eks "Før ti to" -> "før-ti-to"
            # Så nøyer meg med dette da jeg føler oppgaven er besvart! :3
        elif a[0] > 30 or a[0] < 50: # Oppgave 1.2
            print("Nærme, men feil.")
        else:
            print(f"{a[-1]} So long, and thanks for all the fish!")


THE_MEANING()


"""
===================================================
Kjøreeksempler:
*path strings removed
===================================================
Eksempel 1:
---------------------------------------------------
Hva er svaret på det ultimate spørsmålet om livet, universet og alle ting?
HINT: Det er ett tall.
eple
FEIL! So long, and thanks for all the fish!

Process finished with exit code 0
---------------------------------------------------
Eksempel 2:
---------------------------------------------------
Hva er svaret på det ultimate spørsmålet om livet, universet og alle ting?
HINT: Det er ett tall.
Førti to
Det stemmer! Meningen med livet er førti to!

Process finished with exit code 0
---------------------------------------------------
Eksempel 3:
---------------------------------------------------
Hva er svaret på det ultimate spørsmålet om livet, universet og alle ting?
HINT: Det er ett tall.
42
Det stemmer! Meningen med livet er 42!

Process finished with exit code 0

---------------------------------------------------
Eksempel 4:
---------------------------------------------------
Hva er svaret på det ultimate spørsmålet om livet, universet og alle ting?
HINT: Det er ett tall.
32
Nærme, men feil.

Process finished with exit code 0

===================================================
"""
