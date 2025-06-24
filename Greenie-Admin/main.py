
import datetime as dt
import os
from Forms.login_Form import Login_Form
if __name__ == "__main__":


    print("Directorio actual:", os.getcwd())
    app = Login_Form()
    app.ejecutar()



