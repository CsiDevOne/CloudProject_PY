from login_ui import *
from registrate_ui import *


class Ui:

    def __init__(self, socket_obj):
        self.socketObj = socket_obj

        self.win = None
        self.header_frame = None
        self.header_label = None
        self.login_btn = None
        self.registrate_btn = None
        self.login_win = None
        self.registrate_win = None

        self.gui_loop()

    def __del__(self):
        del self

    def gui_loop(self):
        ct.set_appearance_mode('dark')
        ct.set_default_color_theme('dark-blue')

        self.win = ct.CTk()

        self.win.height = self.win.winfo_screenheight()
        self.win.width = self.win.winfo_screenwidth()
        self.win.geometry('500x900')  # f'{self.win.width}x{self.win.height}''

        self.win.title('MyCloud.com')
        self.win.iconbitmap(r'../assets/icon.ico')
        self.win.configure(bg='#fff', fg_color='#fff')

        self.header_frame = ct.CTkFrame(master=self.win, height=120, width=500, corner_radius=0)
        self.header_frame.pack(padx=0, pady=10)
        self.header_frame.place(relx=0.0, rely=0.064)

        self.header_label = ct.CTkLabel(master=self.win, height=70, width=500, text='My Cloud',
                                        bg_color='#2c3033', font=('Roboto', 20), text_color='#fff')
        self.header_label.place(relx=0.0, rely=0.0)

        self.login_btn = ct.CTkButton(master=self.header_frame, text='Login', text_color='#fff',
                                      command=self.login_btn_onclick, height=40, width=100)
        self.login_btn.place(relx=0.55, rely=0.4)

        self.registrate_btn = ct.CTkButton(master=self.header_frame, text='Registrate', text_color='#fff',
                                           command=self.registrate_btn_onclick, height=40, width=100)
        self.registrate_btn.place(relx=0.78, rely=0.4)

        self.win.protocol('WM_DELETE_WINDOW', self.stop)

        self.win.mainloop()

    def login_btn_onclick(self):
        self.login_win = LoginUi(self.socketObj, self.win, self)

    def registrate_btn_onclick(self):
        self.registrate_win = RegistrateUi(self.socketObj, self.win, self)

    def stop(self):
        self.socketObj.socket.send('<< !DISCONNECT! >>'.encode())
        self.win.destroy()
        exit(0)
