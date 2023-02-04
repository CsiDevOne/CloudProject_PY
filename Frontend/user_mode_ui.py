from admin_ui import *
from tkinter import filedialog


class UserModeUi:

    def __init__(self, username,  socket_obj, main_win_ui_obj, main_obj):
        self.username = username
        self.socket_obj = socket_obj
        self.main_win = main_win_ui_obj
        self.main = main_obj

        self.download_btn = None
        self.upload_btn = None
        self.path_input = None
        self.error_output_path = None
        self.welcome_label = None
        self.browse_bn = None
        self.__path = None
        self.path_text_area = None

        if username == 'REALADMIN':
            adminUi(socket_obj, main_obj, main_win_ui_obj)
        else:
            self.gui_loop()

    def gui_loop(self):
        self.main_win.title(f'MyCloud.com | {self.username}')

        for i in [self.main.login_win.main_frame, self.main.login_btn, self.main.registrate_btn]:
            i.pack_forget()
            i.destroy()

        self.main.user_interface_frame = ct.CTkFrame(master=self.main_win, height=(900 - 90), width=500,
                                                     corner_radius=0)
        self.main.user_interface_frame.place(relx=0.0, rely=0.1)

        self.welcome_label = ct.CTkLabel(master=self.main.user_interface_frame, height=70, width=300,
                                         text=f'Welcome {self.username}!', font=('Roboto', 30), text_color='#f0922e')
        self.welcome_label.place(relx=0.0, rely=0.0)

        self.download_btn = ct.CTkButton(master=self.main.user_interface_frame, height=40, width=100, text='Download',
                                         command=self.download)
        self.download_btn.place(relx=0.05, rely=0.2)

        self.upload_btn = ct.CTkButton(master=self.main.user_interface_frame, height=40, width=100, text='upload',
                                       command=self.upload)
        self.upload_btn.place(relx=0.3, rely=0.2)

        self.browse_btn = ct.CTkButton(master=self.main.user_interface_frame, height=60, width=130,
                                       command=self.browse_btn_onclick, text='Browse', font=('Roboto', 20))
        self.browse_btn.place(rely=0.4, relx=0.1)

        self.error_output_path = ct.CTkTextbox(master=self.main.user_interface_frame, height=50, width=400,
                                               border_color='#fff', state='disabled', font=('Roboto', 15),
                                               text_color='#fa3c23')
        self.error_output_path.place(relx=0.1, rely=0.6)

        self.path_text_area = ct.CTkTextbox(master=self.main.user_interface_frame, height=50, width=400,
                                            border_color='#fff', state='disabled', font=('Roboto', 15))
        self.path_text_area.place(relx=0.1, rely=0.5)

    def download(self):
        pass

    def upload(self):
        if self.__path is None:
            self.error_output_path.configure(state='normal')
            self.error_output_path.insert('1.0', 'You must have selected a file path.')
            self.error_output_path.configure(state='disabled')
            return
        else:
            try:
                with open(self.__path, 'r') as f:
                    data = f.read()
                    self.socket_obj.send_upload(self.__path, data)

            except FileNotFoundError as exc:
                self.error_output_path.configure(state='normal')
                self.error_output_path.delete('1,0', 'end')
                self.error_output_path.insert('1.0', repr(exc))
                self.error_output_path.configure(state='disabled')
                self.path_input.delete('1.0', 'end')

    @staticmethod
    def str_find(string, char):
        indexes = []
        index = 0

        for i in string:
            index += 1
            if i == char:
                indexes.append(index)

        return indexes

    def browse_btn_onclick(self):
        self.__path = filedialog.askopenfilename()
        self.path_text_area.configure(state='normal')
        self.path_text_area.insert('1.0', self.__path)
        self.path_text_area.configure(state='disabled')
