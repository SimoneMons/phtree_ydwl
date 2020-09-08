from PyQt5.QtWidgets import QMessageBox


def helper(self):
    """Display help."""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)

    msg.setText("This simple python script allows you to generate a "
                "worklog in rst format based on your repo commits.")
    msg.setInformativeText("You need to generated a token first.")
    msg.setWindowTitle("Help")
    msg.setDetailedText("Simply generate a personnal access token and "
                        "enter it in the first field of the window."
                        "\r\n"
                        "In order to generate this token, go to "
                        "https://github.com/settings/tokens "
                        "under \"Personal access tokens\".")
    msg.exec_()
