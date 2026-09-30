#Pakkeliste
#Noen kommentarer er lagt eller utfylt i bunn,
#hvis du ser [x{tall}] kan du gjøre ett ctrl+f søk for å lettere finne kommentaren.
import os #for å se etter om det finnes en liste
import json
from itertools import batched
import uuid
import sys


class PakkeListe:
    def __init__(self):
        self.pakkelister = self.init_list()
        self.active_list_name = "Default"
        self.active_uuid = None
        self.active_list = []

        self.menu: dict = {"ui_comp":{    # [menu: dict] googla meg frem til den der da pycharm ga warnings jeg ville bli kvitt
                        "double line":   "="*50,
                        "single line":   "-"*50,
                        "empty line":    " "*50,
                        "gui_1":[
                                r"_     ___ ____ _____ _____ ____  ",
                                r"| |   |_ _|  ___|_   _| ____|  _ \ ",
                                r"| |    | ||___ \  | | |  _| | |_) |",
                                r"| |___ | | ___) | | | | |___|  _ < ",
                                r"|_____|___|____/  |_| |_____|_| \_\\"]
                            #bruke gemini for å generere denne x)
                        },
                     "options":{
                         "Add stuff":      self.add_to_list,
                         "Remove stuff":   self.remove_from_list,
                         "Clear list":     self.clear_list,
                         "Save list":      self.save_list,
                         "Load list":      lambda: self.list_manager("load"),
                         "Delete list":    lambda: self.list_manager("delete"),
                         "Rename list":    lambda: self.list_manager("rename"),
                         "Print the list": self.show_list,
                         "Exit program":   self.exit_gracefully
                        }}

        #self.gui_elements = self.generate_gui_content()
        self.header = "\n".join(self.generate_gui_content("header"))
        self.m_content = "\n".join(self.generate_gui_content("content"))

    # -fant ut at det var bedre å lagre alt istedenfor å kalle på denne(header) metoden hver gang jeg ville skrive ut headeren.
    # -ekspanderte det senere til å ha en stor funksjon som tar seg av alt gui innhold,
    #  det være sagt, dette begynner å bli så stort at det kunne gjort seg med en egen klasse til å generere ui innhold.
    # -gjorde om på strukturen så funksjoner kan kalles ved behov, for å kunne håndtere både statiske og dynamiske elementer.
    def generate_gui_content(self, type, data=None):
        ui_comp = self.menu["ui_comp"]
        ui_options = self.menu["options"]
        double_line = ui_comp["double line"]
        inner_width = len(double_line) - 4
        space = f"||{" " * inner_width}||"

        def menu_content():
            gui_content = [space]
            gui_options = []

            for i, o in enumerate(ui_options):
                gui_options.append(f"[{i + 1}: {o}]")

            for b in batched(gui_options, 2): #har brukt denne, så den er litt robust i tilfelle jeg legger til flere valg
                e1 = b[0]
                e2 = b[1] if len(b) > 1 else ""
                gui_content.append(f"|| {e1:<20} | {e2:<21} ||")

            gui_content.extend([space, double_line])
            return gui_content

        def menu_header():
            # statisk gui element, dette er den første jeg lagde og fant ut at å lagre all terminalutskrift i lister,
            # gjorde alt mye renere å se på, istedenfor haugevis med print() linjer.
            signature = f"||{"MUPHAN'S":^{inner_width}}||"
            gui_header = [
                double_line,
                signature
            ]
            # pakker inn 'eye-candy' og legger til i listen
            for e in ui_comp["gui_1"]:
                element = e.replace('\xa0', ' ')  # brukte gemini til å finne løsning på Non-breaking space
                left_spacing = (inner_width - len(element)) // 2
                right_spacing = inner_width - left_spacing - len(element)
                gui_header.append(f"||{" " * left_spacing}{element}{" " * right_spacing}||")

            gui_header.extend([space, double_line])

            return gui_header
            # det kunne også fint gjort seg å lagre statiske elementer som dette i en program_data.json,
            # så alt bare trengs å genereres første gang programmet kjøres.

            #print("\n".join(menu_lines)) #relic of the past, lar den stå som et arkeologisk spor av hvordan det har utviklet seg

        def single_line_display(data): #data: forventer tuppel eller liste med lister [[int(index), "innhold"],...]
            display_list = [double_line, space]
            for e in data:
                element = f"{e[0]}: {e[1]}"
                display_list.append(f"||{element:^{inner_width}}||") #midtstiller teksten som gir litt wonky resultat [x3]
            display_list.extend([space, double_line])
            return display_list

        constructors = {
            "header": menu_header,
            "content": menu_content,
            "single_list": lambda: single_line_display(data)
        }
        if type in constructors:
            return constructors[type]()
        else:
            raise ValueError(f"Invalid menu type: {type}")


    def add_to_list(self):
        item = input("Add stuff (max 40 characters): ").strip()

        if not item:
            #print("Can't add empty element!")
            return "Can't add empty element!"

        if len(item) > 40:
            #print(f"String too long ({len(item)})! Maximum 40 characters allowed.")
            return f"String too long ({len(item)})! Maximum 40 characters allowed."
        #kunne lagd denne litt mer robust så den ikke starter om loopen før bruker velger å gå tilbake til menyen
        #eller oppgir gyldig element


        self.active_list.append(item)
        #print(f"Added {item} successfully!")
        return f"Added {item} successfully!"

    def remove_from_list(self): # skulle jeg brukt mer tid på dette ville jeg lagt til en måte å "remove all" [semiFIXED; har lagd en clear list]
        if not self.active_list:
            print("\n The active list is empty. Please put some stuff in it before we take it out!")
            return

        print(self.show_list())

        user_input = input("Choose a number from the list (or b/q): ").strip()

        if user_input.lower() == "b" or not user_input:
            #print("Cancelled removal.")
            return "Cancelled removal."

        target_item = None

        try:
            idx = int(user_input)
            if 1 <= idx <= len(self.active_list):
                target_item = self.active_list[idx - 1]
            else:
                #print(f"Invalid selection. Choose a number between 1 and {len(self.active_list)}")
                return f"Invalid selection. Choose a number between 1 and {len(self.active_list)}"
        except ValueError:
            if user_input in self.active_list:
                target_item = user_input
            else:
                #print(f"'{user_input}' is not an item in the list")
                return f"'{user_input}' is not an item in the list"

        confirm = input(f"Are you sure you want to remove '{target_item}' (it might come in handy!! D:)? (y/n): ").strip().lower()

        if confirm == "y":
            self.active_list.remove(target_item)
            #print(f"Removed {target_item} from the active list!")
            return f"Removed {target_item} from the active list!"
        else:
            #print("Cancelled removal.")
            return "Cancelled removal."

    def clear_list(self): #nullstiller den aktive listen i arbeidsminnet
        if not self.active_list:
            #print("\n The active list is empty. Please put some stuff in it before we take it out!")
            return "\n The active list is empty. Please put some stuff in it before we take it out!"

        current_name = self.active_list_name
        confirm = input(f"Are you sure you want to clear the active list '{current_name}' (y/n): ").strip().lower()

        if confirm =="y":
            self.active_list = []
            self.active_uuid = None
            #print(f"Cleared {current_name} list!")
            return f"Cleared {current_name} list!"
        else:
            #print("Cleansing cancelled.")
            return "Cleansing cancelled."

    def init_list(self): #sjekker om det finnes en json for lister, hvis ikke så oppretter den en.
        if os.path.exists("pakkeliste.json"):
            try:
                with open("pakkeliste.json", "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("Warning: JSON file corrupt or missing. Generating new..")
                return {}
        else:
            return {}

    def show_list(self):
        if not self.active_list:
            #print("\n The active list is empty. Please put some stuff in it first! UwU <3")
            return "\n The active list is empty. Please put some stuff in it first! UwU <3"

        data_to_render = [[i+1, item] for i, item in enumerate(self.active_list)]
        #rendered_list = "\n".join(self.generate_gui_content("single_list", data=data_to_render))
        #print(rendered_list)
        return "\n".join(self.generate_gui_content("single_list", data=data_to_render))


# Jeg endte med å samle metodene for liste-liste håndtering i én funksjon da det ble mye gjennbrukt kode,
# jeg hadde load og delete på plass før jeg omskrev, load funksjonen finnes i gravplassen på bunn.
    def list_manager(self, mode="load"): # her laster, sletter og endrer vi navn på lister i dict(json)
        if len(self.pakkelister) == 0:
            #print("\nNo saved lists yet exists, please, remedy that! <3\n")
            return "\nNo saved lists yet exists, please, remedy that! <3\n"

        uuid_keys = list(self.pakkelister.keys())
        saved_lists = []
        for i, uid in enumerate(uuid_keys):
            name = self.pakkelister[uid]["name"]
            saved_lists.append([i + 1, name])

        saved_lists.extend([["b", "Back"], ["q", "Quit"]])

        rendered_lists = "\n".join(self.generate_gui_content("single_list", data=saved_lists))

        modes_prompt = {
            "load": "Select a list to LOAD",
            "delete": "Select a list to DELETE",
            "rename": "Select a list to RENAME"
        }

        while True:
            print(rendered_lists)
            print(f"---{modes_prompt.get(mode, 'Select a list')}---")
            user_input = input("Choose a number from the menu (or b/q): ").strip().lower()

            if user_input == "q":
                print("Quitting...")
                exit()
            elif user_input == "b":
                #print("Returning to main menu...")
                return "Returning to main menu..."

            try:
                choice = int(user_input)

                if 1 <= choice <= len(uuid_keys):
                    selected_uuid = uuid_keys[choice - 1]
                    list_data = self.pakkelister[selected_uuid]
                    current_name = list_data["name"]

                    if mode == "load":
                        self.active_list = list_data["items"][:]
                        self.active_uuid = selected_uuid
                        #print(f"-> Loaded packing list : {current_name}\n")
                        return f"-> Loaded packing list : {current_name}\n"

                    elif mode == "delete":
                        confirm = input(f"Are you sure you want to DELETE '{current_name}' (y/n): ").strip().lower()
                        if confirm == "y":
                            del self.pakkelister[selected_uuid]

                            if self.active_uuid == selected_uuid:
                                self.active_list = []
                                self.active_uuid = None

                            #print(f"-> Deleted packing list : {selected_uuid}\n")
                            self.save_to_file()
                            return f"-> Deleted packing list : {current_name}\n"
                        else:
                            #print("Cancelled deletion.")
                            return "Cancelled deletion."

                    elif mode == "rename":
                        new_name = input(f"Enter new name for '{current_name}': ").strip()
                        if new_name:
                            self.pakkelister[selected_uuid]["name"] = new_name
                            #print(f"-> Changed name from '{current_name}' to '{new_name}'\n")
                            self.save_to_file()
                            return f"-> Changed name from '{current_name}' to '{new_name}'\n"
                        else:
                            #print("Invalid name. No new name for u!")
                            return "Invalid name. No new name for u!"

                    else:
                        #print("Invalid selection. Try again!")
                        return f"Invalid selection. Try again!"

            except ValueError:
                #print(f"\nInvalid input! Choose a number, 'b' for BACK or 'q' for QUIT!\n")
                return f"\nInvalid input! Choose a number, 'b' for BACK or 'q' for QUIT!\n"

    def save_list(self): # lagre aktiv liste til dict (json) (jeg burde egentlig få lagt denne til i list manager)
        if not self.active_list:
            #print("List is empty. We can't save nothing!\n")
            return "List is empty. We can't save nothing!\n"

        if self.active_uuid in self.pakkelister:
            self.pakkelister[self.active_uuid]["items"] = self.active_list[:]
            #print(f"Saved changes to {self.pakkelister[self.active_uuid]['name']}")
            self.save_to_file()
            return f"Saved changes to {self.pakkelister[self.active_uuid]['name']}"

        else:
            name = input("Enter a name for this list: ").strip()
            if not name:
                #print("Invalid name. Save cancelled")
                return "Invalid name. Save cancelled"

            new_uuid = str(uuid.uuid4().hex[:8]) #startet med plain uuid4, men 128bit streng var litt overkill, så reduserte til 32bit
            self.pakkelister[new_uuid] = {
                "name": name,
                "items": self.active_list[:]
            }
            self.active_uuid = new_uuid
            #print(f"Saved the new list as '{name}'")
            self.save_to_file()
            return f"Saved the new list as '{name}'"

        #self.save_to_file() #måtte flytte denne inn i sjekkene, siden jeg gå dem return's

    def save_to_file(self, filename="pakkeliste.json"): #denne metoden og save_list burde egentlig bakes inn i list_manager
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(self.pakkelister, f, indent=4, ensure_ascii=False)
            #print(f"\n-> Saved to {filename}")
            return f"\n-> Saved to {filename}"
        except Exception as e:
            #print(f"\nERROR! Could not save to file: {e}")
            return f"\nERROR! Could not save to file: {e}"

    def exit_gracefully(self, reason="Program terminated."): #[x1]
        print("\n")
        print("=" * 50)
        print(f"  {reason}".center(50))
        print("  Saving state & closing... Bye! <3".center(50))
        print("=" * 50)
        sys.exit(0) #la til sys så det kan håndtere exit ved kjøring utenfor en IDE


    def run_lister(self):
        header = self.header
        m_content = self.m_content
        options = self.menu["options"]
        option_keys = list(options.keys())

        pending_ui_element = None #[x2]: siden alle metodene som kjøres her enten gjør sine egne greier før return,
                                  # eller avslutter med en print, kan jeg bare sende innholdet av printen ut av løkka og holde på den
                                  # til etter header og content blir tegnet på nytt.
        while True:
            print(header)       #printen av ui elementene er litt klønete, i at den printer hele pakka hver gang [x2]
            print(m_content)

            if pending_ui_element:
                 print(pending_ui_element)
                 pending_ui_element = None

            user_input = input(f"Type the number of your choice, 1 to {len(options)}: ").strip()

            try:
                choice = int(user_input)
                if 1 <= choice <= len(option_keys):
                    option_choice = option_keys[choice-1]

                    result = options[option_choice]()
                    if isinstance(result, str):
                        pending_ui_element = result

                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Invalid choice. Please try again.")

    # Skulle jeg brukt mer tid på dette ville jeg lagt til/endret:
    # Kontekstuelle menyer; ex: (List manager -> [Save, Load, Rename, Delete])
    # Litt mer intelligent utskrift av ui elementer; ex: utskrift av liste etter header og content. [FIXED]




#PakkeListe().run_lister()

if __name__ == "__main__":  # [x1]
    app = PakkeListe()
    try:
        app.run_lister()
    except KeyboardInterrupt:
        app.exit_gracefully("Program interrupted by user (Ctrl+C).")
    except Exception as e:
        app.exit_gracefully(f"Unexpected error occurred: {e}")



# [x1]: Denne koden er tatt direkte fra gemini. Jeg ville ha en metode for å lukke programmet pent på,
#     og husket ikke nøyaktig hvordan det gjøres, så søkte opp.
#     Som jeg skjønner det er essensen å pakke alt inn i en try blokk så enhver feil kan fanges for så kalle på en exit funksjon

# Kommentarer til oppgaven:
# "Du skal lage et lite program som gjør det mulig å lage en pakkeliste for når du skal ut og reise."
# "... lage et lite program ..."
# " ... lite ... "
# -Okei.. Jeg feilet vel egentlig på det punktet.. x)
#  Det være sagt, jeg gjør som jeg gjør for å ha det morro, samt trene mer på bruk av klasser ^^'
# -Jeg kunne lagt inn metoder for litt mer intuitive kommandoer, som Exit alltid q, load = l, rename = r, etc
#  men det får bli hvis jeg kommer tilbake til dette programmet i fremtiden, siden det gjør hva det blir bedt om, pluss
#  litt til x)
#
# - Det er mye utkommenterte print() kommandoer, har latt disse stå som ett arkeologisk spor på hvordan det ble gjort
#   før jeg lagde en måte å sende ting fra metodene frem til neste loop.
# - Jeg burde legge til ett ui element som alltid viser den aktive listen.
#
# [x3]:  for å gjøre dette penere må jeg basere hver linje på det lengste elementet i listen, gi hvert element
#        den lengden og høyrestille det, så pakke det inn i en midstilling som tar width-len(longest element)


r"""
================================================
Kjøreeksempel:
================================================
==================================================
||                   MUPHAN'S                   ||
||      _     ___ ____ _____ _____ ____         ||
||     | |   |_ _|  ___|_   _| ____|  _ \       ||
||     | |    | ||___ \  | | |  _| | |_) |      ||
||     | |___ | | ___) | | | | |___|  _ <       ||
||     |_____|___|____/  |_| |_____|_| \_\\     ||
||                                              ||
==================================================
||                                              ||
|| [1: Add stuff]       | [2: Remove stuff]     ||
|| [3: Clear list]      | [4: Save list]        ||
|| [5: Load list]       | [6: Delete list]      ||
|| [7: Rename list]     | [8: Print the list]   ||
|| [9: Exit program]    |                       ||
||                                              ||
==================================================
Type the number of your choice, 1 to 9:1
Add stuff (max 40 characters): test_item1
==================================================
||                   MUPHAN'S                   ||
||      _     ___ ____ _____ _____ ____         ||
||     | |   |_ _|  ___|_   _| ____|  _ \       ||
||     | |    | ||___ \  | | |  _| | |_) |      ||
||     | |___ | | ___) | | | | |___|  _ <       ||
||     |_____|___|____/  |_| |_____|_| \_\\     ||
||                                              ||
==================================================
||                                              ||
|| [1: Add stuff]       | [2: Remove stuff]     ||
|| [3: Clear list]      | [4: Save list]        ||
|| [5: Load list]       | [6: Delete list]      ||
|| [7: Rename list]     | [8: Print the list]   ||
|| [9: Exit program]    |                       ||
||                                              ||
==================================================
Added test_item1 successfully!
Type the number of your choice, 1 to 9:1
Add stuff (max 40 characters): test_item2
==================================================
||                   MUPHAN'S                   ||
||      _     ___ ____ _____ _____ ____         ||
||     | |   |_ _|  ___|_   _| ____|  _ \       ||
||     | |    | ||___ \  | | |  _| | |_) |      ||
||     | |___ | | ___) | | | | |___|  _ <       ||
||     |_____|___|____/  |_| |_____|_| \_\\     ||
||                                              ||
==================================================
||                                              ||
|| [1: Add stuff]       | [2: Remove stuff]     ||
|| [3: Clear list]      | [4: Save list]        ||
|| [5: Load list]       | [6: Delete list]      ||
|| [7: Rename list]     | [8: Print the list]   ||
|| [9: Exit program]    |                       ||
||                                              ||
==================================================
Added test_item2 successfully!
Type the number of your choice, 1 to 9:2
==================================================
||                                              ||
||                1: test_item1                 ||
||                2: test_item2                 ||
||                                              ||
==================================================
Choose a number from the list (or b/q)2
Are you sure you want to remove 'test_item2' (it might come in handy!! D:)? (y/n): y
==================================================
||                   MUPHAN'S                   ||
||      _     ___ ____ _____ _____ ____         ||
||     | |   |_ _|  ___|_   _| ____|  _ \       ||
||     | |    | ||___ \  | | |  _| | |_) |      ||
||     | |___ | | ___) | | | | |___|  _ <       ||
||     |_____|___|____/  |_| |_____|_| \_\\     ||
||                                              ||
==================================================
||                                              ||
|| [1: Add stuff]       | [2: Remove stuff]     ||
|| [3: Clear list]      | [4: Save list]        ||
|| [5: Load list]       | [6: Delete list]      ||
|| [7: Rename list]     | [8: Print the list]   ||
|| [9: Exit program]    |                       ||
||                                              ||
==================================================
Removed test_item2 from the active list!
Type the number of your choice, 1 to 9:4
Enter a name for this list: test_list2
==================================================
||                   MUPHAN'S                   ||
||      _     ___ ____ _____ _____ ____         ||
||     | |   |_ _|  ___|_   _| ____|  _ \       ||
||     | |    | ||___ \  | | |  _| | |_) |      ||
||     | |___ | | ___) | | | | |___|  _ <       ||
||     |_____|___|____/  |_| |_____|_| \_\\     ||
||                                              ||
==================================================
||                                              ||
|| [1: Add stuff]       | [2: Remove stuff]     ||
|| [3: Clear list]      | [4: Save list]        ||
|| [5: Load list]       | [6: Delete list]      ||
|| [7: Rename list]     | [8: Print the list]   ||
|| [9: Exit program]    |                       ||
||                                              ||
==================================================
Saved the new list as 'test_list2'
Type the number of your choice, 1 to 9:5
==================================================
||                                              ||
||                 1: Grilltur                  ||
||       2: Ting jeg må ta med på skolen        ||
||                3: test_list1                 ||
||                4: test_list2                 ||
||                   b: Back                    ||
||                   q: Quit                    ||
||                                              ||
==================================================
---Select a list to LOAD---
Choose a number from the menu (or b/q)2
==================================================
||                   MUPHAN'S                   ||
||      _     ___ ____ _____ _____ ____         ||
||     | |   |_ _|  ___|_   _| ____|  _ \       ||
||     | |    | ||___ \  | | |  _| | |_) |      ||
||     | |___ | | ___) | | | | |___|  _ <       ||
||     |_____|___|____/  |_| |_____|_| \_\\     ||
||                                              ||
==================================================
||                                              ||
|| [1: Add stuff]       | [2: Remove stuff]     ||
|| [3: Clear list]      | [4: Save list]        ||
|| [5: Load list]       | [6: Delete list]      ||
|| [7: Rename list]     | [8: Print the list]   ||
|| [9: Exit program]    |                       ||
||                                              ||
==================================================
-> Loaded packing list : Ting jeg må ta med på skolen

Type the number of your choice, 1 to 9:8
==================================================
||                   MUPHAN'S                   ||
||      _     ___ ____ _____ _____ ____         ||
||     | |   |_ _|  ___|_   _| ____|  _ \       ||
||     | |    | ||___ \  | | |  _| | |_) |      ||
||     | |___ | | ___) | | | | |___|  _ <       ||
||     |_____|___|____/  |_| |_____|_| \_\\     ||
||                                              ||
==================================================
||                                              ||
|| [1: Add stuff]       | [2: Remove stuff]     ||
|| [3: Clear list]      | [4: Save list]        ||
|| [5: Load list]       | [6: Delete list]      ||
|| [7: Rename list]     | [8: Print the list]   ||
|| [9: Exit program]    |                       ||
||                                              ||
==================================================
==================================================
||                                              ||
||                1: skrivesaker                ||
||                 2: notatbok                  ||
||                 3: kaffekopp                 ||
||               4: energidrikke                ||
||                                              ||
==================================================
Type the number of your choice, 1 to 9:7
==================================================
||                                              ||
||                 1: Grilltur                  ||
||       2: Ting jeg må ta med på skolen        ||
||                3: test_list1                 ||
||                4: test_list2                 ||
||                   b: Back                    ||
||                   q: Quit                    ||
||                                              ||
==================================================
---Select a list to RENAME---
Choose a number from the menu (or b/q)4
Enter new name for 'test_list2': æddæbæddæ
==================================================
||                   MUPHAN'S                   ||
||      _     ___ ____ _____ _____ ____         ||
||     | |   |_ _|  ___|_   _| ____|  _ \       ||
||     | |    | ||___ \  | | |  _| | |_) |      ||
||     | |___ | | ___) | | | | |___|  _ <       ||
||     |_____|___|____/  |_| |_____|_| \_\\     ||
||                                              ||
==================================================
||                                              ||
|| [1: Add stuff]       | [2: Remove stuff]     ||
|| [3: Clear list]      | [4: Save list]        ||
|| [5: Load list]       | [6: Delete list]      ||
|| [7: Rename list]     | [8: Print the list]   ||
|| [9: Exit program]    |                       ||
||                                              ||
==================================================
-> Changed name from 'test_list2' to 'æddæbæddæ'

Type the number of your choice, 1 to 9:5
==================================================
||                                              ||
||                 1: Grilltur                  ||
||       2: Ting jeg må ta med på skolen        ||
||                3: test_list1                 ||
||                 4: æddæbæddæ                 ||
||                   b: Back                    ||
||                   q: Quit                    ||
||                                              ||
==================================================
---Select a list to LOAD---
Choose a number from the menu (or b/q)b
==================================================
||                   MUPHAN'S                   ||
||      _     ___ ____ _____ _____ ____         ||
||     | |   |_ _|  ___|_   _| ____|  _ \       ||
||     | |    | ||___ \  | | |  _| | |_) |      ||
||     | |___ | | ___) | | | | |___|  _ <       ||
||     |_____|___|____/  |_| |_____|_| \_\\     ||
||                                              ||
==================================================
||                                              ||
|| [1: Add stuff]       | [2: Remove stuff]     ||
|| [3: Clear list]      | [4: Save list]        ||
|| [5: Load list]       | [6: Delete list]      ||
|| [7: Rename list]     | [8: Print the list]   ||
|| [9: Exit program]    |                       ||
||                                              ||
==================================================
Returning to main menu...
Type the number of your choice, 1 to 9:6
==================================================
||                                              ||
||                 1: Grilltur                  ||
||       2: Ting jeg må ta med på skolen        ||
||                3: test_list1                 ||
||                 4: æddæbæddæ                 ||
||                   b: Back                    ||
||                   q: Quit                    ||
||                                              ||
==================================================
---Select a list to DELETE---
Choose a number from the menu (or b/q)4
Are you sure you want to DELETE 'æddæbæddæ' (y/n): y
==================================================
||                   MUPHAN'S                   ||
||      _     ___ ____ _____ _____ ____         ||
||     | |   |_ _|  ___|_   _| ____|  _ \       ||
||     | |    | ||___ \  | | |  _| | |_) |      ||
||     | |___ | | ___) | | | | |___|  _ <       ||
||     |_____|___|____/  |_| |_____|_| \_\\     ||
||                                              ||
==================================================
||                                              ||
|| [1: Add stuff]       | [2: Remove stuff]     ||
|| [3: Clear list]      | [4: Save list]        ||
|| [5: Load list]       | [6: Delete list]      ||
|| [7: Rename list]     | [8: Print the list]   ||
|| [9: Exit program]    |                       ||
||                                              ||
==================================================
-> Deleted packing list : 3a674b10                 #<-dette er fikset

Type the number of your choice, 1 to 9:8
==================================================
||                   MUPHAN'S                   ||
||      _     ___ ____ _____ _____ ____         ||
||     | |   |_ _|  ___|_   _| ____|  _ \       ||
||     | |    | ||___ \  | | |  _| | |_) |      ||
||     | |___ | | ___) | | | | |___|  _ <       ||
||     |_____|___|____/  |_| |_____|_| \_\\     ||
||                                              ||
==================================================
||                                              ||
|| [1: Add stuff]       | [2: Remove stuff]     ||
|| [3: Clear list]      | [4: Save list]        ||
|| [5: Load list]       | [6: Delete list]      ||
|| [7: Rename list]     | [8: Print the list]   ||
|| [9: Exit program]    |                       ||
||                                              ||
==================================================
==================================================
||                                              ||
||                1: skrivesaker                ||
||                 2: notatbok                  ||
||                 3: kaffekopp                 ||
||               4: energidrikke                ||
||                                              ||
==================================================
Type the number of your choice, 1 to 9:9
Quitting program...

Process finished with exit code 0
"""
"""
#Code graveyard.
----

        #gikk bort ifra å ha kategorisert liste for nå
        self.pakkeliste = {"Mat og Drikke"      :[],
                           "Klær"               :[],
                           "Hyggieneartikler"   :[],
                           "Elektronikk"        :[],
                           "Annet"              :[]
                           }
        
----
    def open_list(self):
        return

    def name_list(self):
        print("name")
        return
----
    def load_list(self):
        if len(self.pakkelister) == 0:
            print("\nNo saved lists yet exists, please, remedy that! <3\n")
            return

        saved_lists = []
        for i, key in enumerate(self.pakkelister):
            saved_lists.append([i + 1, key])
        saved_lists.extend([["b", "Back"], ["q", "Quit"]])
        list_keys = list(self.pakkelister.keys())

        rendered_lists = "\n".join(self.generate_gui_content("single_list", data=saved_lists))

        while True:
            print(rendered_lists)
            user_input = input("Choose a number from the menu (or b/q)").strip().lower()

            if user_input == "q":
                print("Quitting...")
                exit()
            elif user_input == "b":
                print("Returning")
                return

            try:
                choice = int(user_input)

                if 1 <= choice <= len(list_keys):
                    selected_list = list_keys[choice-1]
                    self.active_list = self.pakkelister[selected_list]
                    print(f"-> Loaded packing list: '{selected_list}'\n")
                    return
                else:
                    print("Invalid choice. Please try again.")

            except ValueError:
                print("\nInvalid input! Enter a valid number, 'b' to go back or 'q' to quit.\n")
----
"""