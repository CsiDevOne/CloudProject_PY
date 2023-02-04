from user_mode_ui import *


class LoginUi:

    def __init__(self, socket_obj, main_win_ui_obj, main_obj):
        self.socket_obj = socket_obj
        self.main_win = main_win_ui_obj
        self.main = main_obj
        self.remaining_attempts = 3

        self.main_frame = None
        self.title = None
        self.username_input = None
        self.username_label = None
        self.password_input = None
        self.password_label = None
        self.submit_btn = None
        self.error_output = None
        self.email_input = None
        self.email_label = None

        self.gui_loop()

    def gui_loop(self):
        self.delete()

        self.main_frame = ct.CTkFrame(master=self.main_win, width=400, height=600)
        self.main_frame.place(relx=0.1, rely=0.25)

        self.title = ct.CTkLabel(master=self.main_frame, width=100, height=40, text='Login', font=('Roboto', 20),
                                 text_color='#3776ab')
        self.title.pack(padx=20, pady=10)
        self.title.place(relx=0.4, rely=0.1)

        self.username_input = ct.CTkTextbox(master=self.main_frame, width=200, height=30, font=('Roboto', 13),
                                            text_color='#3776ab')
        self.username_input.pack(padx=20, pady=10)
        self.username_input.place(relx=0.3, rely=0.2)

        self.username_label = ct.CTkLabel(master=self.main_frame, height=10, width=60, text='Username',
                                          font=('Roboto', 12))
        self.username_label.place(relx=0.3, rely=0.25)

        self.email_input = ct.CTkTextbox(master=self.main_frame, width=200, height=30, font=('Roboto', 13),
                                         text_color='#3776ab')
        self.email_input.place(relx=0.3, rely=0.3)

        self.email_label = ct.CTkLabel(master=self.main_frame, height=10, width=60, text='Email   ',
                                       font=('Roboto', 12))
        self.email_label.place(relx=0.3, rely=0.35)

        self.password_input = ct.CTkTextbox(master=self.main_frame, width=200, height=30, font=('Roboto', 13),
                                            text_color='#3776ab')
        self.password_input.pack(padx=20, pady=10)
        self.password_input.place(relx=0.3, rely=0.4)

        self.password_label = ct.CTkLabel(master=self.main_frame, height=10, width=60, text='Password',
                                          font=('Roboto', 12))
        self.password_label.place(relx=0.3, rely=0.45)

        self.submit_btn = ct.CTkButton(master=self.main_frame, text='Submit', font=('Roboto', 20), height=40, width=100,
                                       command=self.submit_btn_onclick)
        self.submit_btn.place(relx=0.4, rely=0.7)

        self.error_output = ct.CTkTextbox(master=self.main_frame, height=60, width=200, font=('Roboto', 12),
                                          text_color='#fa3c23', bg_color='#2d383c', state='disabled')
        self.error_output.place(relx=0.3, rely=0.55)

    def submit_btn_onclick(self):
        self.error_output.configure(state='normal')
        self.error_output.delete('1.0', 'end')
        self.error_output.configure(state='disabled')

        username = self.username_input.get('1.0', 'end').replace('\n', '')
        email = self.email_input.get('1.0', 'end').replace('\n', '')
        password = self.password_input.get('1.0', 'end').replace('\n', '')

        if username is not None and password is not None:
            self.socket_obj.send_credentials([username, email, password])

            if self.socket_obj.socket.recv(1024).decode() == '< success >':
                self.error_output.configure(state='normal', text_color='#298a36')
                self.error_output.insert('1.0', 'Logged in !')
                self.error_output.configure(state='disabled')

                UserModeUi(username, self.socket_obj, self.main_win, self.main)
                del username, password

            else:
                if self.remaining_attempts == 1:
                    exit(0)
                self.remaining_attempts -= 1
                self.error_output.configure(state='normal')
                self.error_output.insert('1.0', f'Failed to log in properly !\n{self.remaining_attempts}'
                                                ' attempts remain!')
                self.error_output.configure(state='disabled')
                self.password_input.delete('1.0', 'end')
        else:
            return

    def delete(self):
        self.main_win.title('MyCloud.com | Login')
