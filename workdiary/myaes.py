# windows10/python3.5
# -*- coding:utf-8 -*-

import os

import pyaes

############################################################
#-----------------------AES采用CTR模式---------------------#
############################################################

        
def aesMode(rawfile,newfile,operation,aes_keys):
    key = aes_keys.encode("utf-8")
    AES = pyaes.AESModeOfOperationCTR(key)
    file_in = open(rawfile,'rb')
    file_out = open(newfile,'wb')
    if operation == '加密':
        pyaes.encrypt_stream(AES,file_in,file_out)
    elif operation == '解密':
        pyaes.decrypt_stream(AES,file_in,file_out)
    file_in.close()
    file_out.close()
    if operation == '加密':
        plain_db_path = os.path.abspath(rawfile)
        #cmd_command = 'del %s' % plain_db_path
        cmd_command = 'move /Y %s d:/' % plain_db_path
        os.system(cmd_command)