"""
/***************************************************************************
Name                 : Create New Role Dialog
Description          : Dialog for entering new role information
Date                 : 20/June/2013 
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
from datetime import date
import string

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import sqlalchemy

from ui_new_role import Ui_frmNewRole
from stdm.data import Role
from stdm.security import SecurityException,RoleProvider

class newRoleDlg(QDialog, Ui_frmNewRole):
    '''
    Create New Role Dialog
    '''
    def __init__(self,parent = None,role = None):
        QDialog.__init__(self,parent)
        self.setupUi(self)  
        
        self.role = role
        
        #Initialize the dialog
        self.initGui()
        
    def initGui(self):
        '''
        Set control properties based on the mode
        '''                  
        #Set 'Create Role' button properties
        btnCreateRole = self.buttonBox.button(QDialogButtonBox.Ok)
        btnCreateRole.setText(QApplication.translate("newRoleDlg", "Create Role"))
        QObject.connect(btnCreateRole, SIGNAL("clicked()"),self.acceptdlg)
        
        #Set validator for preventing rolename from having whitespace
        rx = QRegExp("\\S+")
        rxValidator = QRegExpValidator(rx,self)
        self.txtRoleName.setValidator(rxValidator)
                    
        self.txtRoleName.setFocus()            
            
    def validateInput(self):
        '''
        Assert whether required fields have been entered
        '''        
        if str(self.txtRoleName.text()) == "":
            QMessageBox.critical(self, QApplication.translate("newRoleDlg","Required field"), 
                                 QApplication.translate("newRoleDlg","Role name cannot be empty"))
            self.txtRoleName.setFocus()
            return False
    
        else:
            return True 
        
    def _setRole(self):
        '''
        Create/update the user object based on the user input
        '''      
        roleName = self.txtRoleName.text()
        roleDescription = self.txtRoleDescription.text()
        
        if self.role == None:            
            self.role = Role()   
            self.role.name = roleName
            self.role.description = string.strip(roleDescription)                 
                        
    def acceptdlg(self):
        '''
        On user clicking the create user button
        '''
        if self.validateInput():  
                     
            roleProvider = RoleProvider()
            
            try:
                #Create new or update user
                if self.role == None:
                    self._setRole()   
                    
                    #Update the db cluster roles as well
                    roleProvider.CreateRole(self.role.name, self.role.description) 
                                     
                    roleProvider.AddSTDMRole(self.role.name, self.role.description)                                                      
                              
                self.accept()
                
            except SecurityException as se:
                QMessageBox.critical(self, 
                                     QApplication.translate("newUserDlg","Create New User Error"), str(se)) 
                self.user = None
                
            except sqlalchemy.exc.ProgrammingError as pe:
                QMessageBox.critical(self, 
                                     QApplication.translate("newUserDlg","Create New User Error"), str(pe.message))
                self.user = None               
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
            
        
        
        
        
        
        
        
        
        
        
        
        