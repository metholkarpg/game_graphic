from tkinter import *
from tkinter import font
from tkinter import messagebox


def position_window(root, width, height):
    # get screen width and height
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()

    # calculate position x and y coordinates
    x = (screenwidth / 2) - (width / 2)
    y = (screenheight / 2) - (height / 2)

    root.geometry('%dx%d+%d+%d' % (width, height, x, y))


class StoreWindow(object):
    # CONSTRUTOR
    def __init__(self, char, shop_list, title, save_callback):

        self.save_callback = save_callback
        self.root_screen = Tk()

        # DEFINICAO DE ELEMENTOS DA TELA
        self.shop_list = shop_list
        self.char = char
        self.title = title

        self.img_inven = PhotoImage(file="resources/store_items/backpack-1.png")
        self.img_store = PhotoImage(file="resources/store_items/cart.png")
        self.img_coins = PhotoImage(file="resources/store_items/money.png")

        # FONTS
        self.main_font = font.Font(root=self.root_screen, family='Monotype Corsiva', size=16, weight='normal')
        self.bold_font = font.Font(root=self.root_screen, family='Monotype Corsiva', size=16, weight='bold')
        self.title_font = font.Font(root=self.root_screen, family='Monotype Corsiva', size=20, weight='bold')

        self.root_screen.wm_title(self.title)
        self.root_screen.resizable(0, 0)
        # 513, 490
        position_window(self.root_screen, 513, 550)

        self.str_your_items = StringVar()
        self.str_shop_items = StringVar()
        self.str_item_description = StringVar()
        self.str_user_coins = StringVar()
        self.str_user_coins_title = StringVar()
        self.str_title = StringVar()

        self.lbl_title = Label(self.root_screen, textvariable=self.str_title, font=self.title_font, bg="#A3A385")
        self.lbl_your_items = Label(self.root_screen, textvariable=self.str_your_items, font=self.bold_font)
        self.lbl_shop_items = Label(self.root_screen, textvariable=self.str_shop_items, font=self.bold_font)
        self.lbl_desc = Label(self.root_screen, textvariable=self.str_item_description, relief=GROOVE,
                              font=self.main_font)
        self.lbl_coins = Label(self.root_screen, textvariable=self.str_user_coins, font=self.main_font)
        self.lbl_coins_title = Label(self.root_screen, textvariable=self.str_user_coins_title, font=self.bold_font)
        self.lbl_img_inven = Label(self.root_screen, image=self.img_inven)
        self.lbl_img_store = Label(self.root_screen, image=self.img_store)
        self.lbl_img_coins = Label(self.root_screen, image=self.img_coins)

        self.str_title.set(title)
        self.str_user_coins_title.set("Your Coins: $")
        self.str_your_items.set(" Your Items: ")
        self.str_shop_items.set(" Shop Items: ")
        self.str_user_coins.set(char.coins)

        self.libox_inven = Listbox(self.root_screen, selectmode=SINGLE, relief=RIDGE, font=self.main_font)
        self.libox_inven.bind("<<ListboxSelect>>", self.libox_inven_click)
        self.libox_shop = Listbox(self.root_screen, selectmode=SINGLE, relief=RIDGE, font=self.main_font)
        self.libox_shop.bind("<<ListboxSelect>>", self.libox_shop_click)

        self.buy_button = Button(self.root_screen, text=" Buy ", command=self.buy_button_click, state=DISABLED,
                                 relief=RAISED, fg='black', font=self.main_font, bg="#D1E0B2")
        self.sell_button = Button(self.root_screen, text=" Sell ", command=self.sell_button_click, state=DISABLED,
                                  relief=RAISED, fg='black', font=self.main_font, bg="#D1E0B2")
        self.exit_button = Button(self.root_screen, text=" Leave ", command=self.bye, relief=RAISED, fg='black',
                                  font=self.main_font, bg="#FAE6E6")
        self.place_all()

        # ALIMENTANDO AS LISTAS NA PRIMEIRA EXECUCAO
        for item in char.inventory:
            self.libox_inven.insert(END, item.name)
        for item in self.shop_list:
            self.libox_shop.insert(END, item.name)

    # METODOS

    # LISTA SHOP ON CLICK
    def libox_shop_click(self, event):
        self.sell_button.config(state=DISABLED)
        self.buy_button.config(state=NORMAL)
        widget = event.widget
        selected = self.libox_shop.curselection()
        if not selected == ():
            desc = self.shop_list[selected[0]].name
            price = self.shop_list[selected[0]].price
            self.str_item_description.set("Shop Item Selected: \nDescription: %s \nPrice: $%s" % (desc, price))

    # LISTA INVEN ON CLICK
    def libox_inven_click(self, event):
        self.sell_button.config(state=NORMAL)
        self.buy_button.config(state=DISABLED)
        widget = event.widget
        selected = self.libox_inven.curselection()
        if not selected == ():
            desc = self.char.inventory[selected[0]].name
            price = self.char.inventory[selected[0]].price
            self.str_item_description.set("Your Item Selected: \nDescription: %s \nPrice: $%s" % (desc, price))

    def start_window(self):
        self.root_screen.mainloop()

    def place_all(self):

        self.lbl_title.place(x=0, y=0, width=530, height=50)
        self.exit_button.place(x=443, y=9, width=60, height=35)

        self.lbl_img_inven.place(x=15, y=62)
        self.lbl_your_items.place(x=52, y=63)
        self.lbl_img_store.place(x=297, y=62)
        self.lbl_shop_items.place(x=334, y=63)

        self.libox_inven.place(x=15, y=100, width=200, height=300)
        self.libox_shop.place(x=297, y=100, width=200, height=300)

        self.buy_button.place(x=220, y=331, width=70, height=30)
        self.sell_button.place(x=220, y=368, width=70, height=30)

        self.lbl_img_coins.place(x=15, y=403)
        self.lbl_coins_title.place(x=52, y=406, height=25, width=120)
        self.lbl_coins.place(x=168, y=403)
        self.lbl_desc.place(x=15, y=440, height=100, width=482)

    # BUY BUTTON CLICK
    def buy_button_click(self):

        selected = self.libox_shop.curselection()

        if not selected == ():
            if self.shop_list[selected[0]].price <= self.char.coins:
                self.char.coins -= self.shop_list[selected[0]].price
                self.str_user_coins.set(self.char.coins)

                self.char.inventory.append(self.shop_list[selected[0]])
                self.libox_inven.insert(END, self.shop_list[selected[0]].name)
                self.shop_list.pop(selected[0])
                self.libox_shop.delete(selected[0])
            else:
                self.no_coins()

        self.sell_button.config(state=DISABLED)
        self.buy_button.config(state=DISABLED)
        self.str_item_description.set("")
        self.save_callback()

    # SELL BUTTON CLICK
    def sell_button_click(self):

        selected = self.libox_inven.curselection()

        if not selected == ():
            self.char.coins += self.char.inventory[selected[0]].price
            self.str_user_coins.set(self.char.coins)

            self.shop_list.append(self.char.inventory[selected[0]])
            self.libox_shop.insert(END, self.char.inventory[selected[0]].name)
            self.char.inventory.pop(selected[0])
            self.libox_inven.delete(selected[0])

        self.sell_button.config(state=DISABLED)
        self.buy_button.config(state=DISABLED)
        self.str_item_description.set("")
        self.save_callback()

    def no_coins(self):
        messagebox._show("No coins", "Sorry, you don't have enough coins!")

    def bye(self):
        messagebox._show("Bye!", "Thanks for buying!")
        self.root_screen.destroy()
