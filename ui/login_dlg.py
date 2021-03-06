"""
/***************************************************************************
Name                 : STDM Login Dialog
Description          : Display the dialog window for users to login in order 
                        to access STDM tools and modules
Date                 : 24/May/2013 
copyright            : (C) 2013 by John Gitau
email                : gkahiu@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from .ui_login import Ui_frmLogin
from .db_conn_dlg import dbconnDlg
from .notification import NotificationBar,ERROR

from stdm.data import DatabaseConfig, DatabaseConnection
from stdm.security import User

class loginDlg(QDialog, Ui_frmLogin):
    '''
    This class handles user authentication for accessing STDM resources
    '''
    def __init__(self,plugin):
        QDialog.__init__(self,plugin.iface.mainWindow())
        self.setupUi(self)
        
        #gui initialization
        self.initGui()
        
        #class properties
        self.User = None
        self.dbConn = None
        
    def initGui(self):
        '''
        Initialize GUI
        '''
        #Change the name of the OK button to Login
        btnLogin=self.btnBox.button(QDialogButtonBox.Ok)
        btnLogin.setText(QApplication.translate("LoginDialog","Login"))
        #Connect slots
        self.connect(self.btnBox, SIGNAL("accepted()"), self.acceptdlg)
        
        #Configure notification bar
        self.notifBar = NotificationBar(self.vlNotification)
                        
    def validateInput(self):
        '''
        Assert whether required fields have been entered
        '''        
        self.notifBar.clear()
        
        if self.txtUserName.text() == "":
            self.notifBar.insertErrorNotification(QApplication.translate("LoginDialog","UserName field cannot be empty"))
            self.txtUserName.setFocus()
            return False
        
        if self.txtPassword.text() == "":
            self.notifBar.insertErrorNotification(QApplication.translate("LoginDialog","Password field cannot be empty"))
            self.txtPassword.setFocus()
            return False 
        
        else:
            return True 
        
    def __setUser(self):
        '''
        Create the user object based on the user input
        '''      
        username = self.txtUserName.text()
        password = self.txtPassword.text()
        self.User = User(username,password)
        
    def acceptdlg(self):
        '''
        On user clicking the login button
        '''
        isValid = self.validateInput()
        if isValid:
            #Set user object
            self.__setUser()
            #Get DB connection
            dbconfig = DatabaseConfig()
            dbconn = dbconfig.read()
            if dbconn == None:
                msg = QApplication.translate("LoginDialog","The STDM database connection has not been configured in your system.\nWould you like to configure it now?")
                response = QMessageBox.warning(self, QApplication.translate("LoginDialog","Database Connection"), 
                                               msg, QMessageBox.Yes|QMessageBox.No, QMessageBox.Yes)
                if response == QMessageBox.Yes:
                    dbDlg = dbconnDlg(self)
                    retstatus = dbDlg.exec_()
                    if retstatus == QDialog.Accepted:
                        #set the partial database connection properties
                        dbconn = dbDlg.dbconn
                #Whatever the outcome of the database settings definition process                
                if dbconn == None:
                    return                
            dbconn.User = self.User
            #Test connection
            success, msg = dbconn.validateConnection()
            if success:
                self.dbConn = dbconn
                self.accept()
            else:
                QMessageBox.critical(self, QApplication.translate("LoginDialog","Authentication Failed"), msg)
                self.txtPassword.setFocus()
                self.txtPassword.selectAll()
            
        
        
        
        
        
        
        
        
        
        
        
        
