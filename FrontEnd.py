import flet
from flet import *
#from Farkle import *
# Commented out due to the clash of main() 



def screen(page: page):
    page.title = "DICE GAME"
    page.vertical_alignment = "center"

    def roll_button():
        page.title = "RICE GAME"
        page.update()
    
    def keep_button():
        page.title = "DICE GAME"
        page.update()

    page.add(
        Row(
            controls = [
                ElevatedButton(text="Roll", on_click=roll_button()),
                ElevatedButton(text="Keep", on_click=keep_button())
            ]
        )
    )


def main():

    flet.app(target=screen)

main()
