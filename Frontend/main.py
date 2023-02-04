import net
import main_ui


if __name__ == '__main__':
    socket_obj = net.Net()
    ui = main_ui.Ui(socket_obj)