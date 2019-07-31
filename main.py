from flask import Flask
from flask import request
import json
import requests
import mysql.connector

db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="toor",
  database="evoting"
)

mycursor = db.cursor()

app = Flask(__name__)
def request_to_get_leader(list_address, index):
  print ('This request to get leader')

  if index > 4:
    return -1

  try:
    URL = list_address[index] + '/get_leader'
    r = requests.get(URL)
    data = r.text
  except:
    return request_to_get_leader(list_address, index+1)
  else:
    return data

@app.route('/vote', methods=['POST'])
def vote():
  content = request.json
  sender_n = int(content['sender_n'])
  sender_e = int(content['sender_e'])
  sender_d = int(content['sender_d'])
  choice = int(content['choice'])

  try:
    print('Try Block')

    sql = 'SELECT * FROM map_blockchains WHERE nilai_n=%s AND nilai_e=%s'
    val = (sender_n, sender_e)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()

    id_blockchain = myresult[0][0]

    sql = 'SELECT * FROM pilihans WHERE id_blockchain=%s AND id_pilihan=%s'
    val = (id_blockchain, choice)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()

    receiver_n = myresult[0][2]
    receiver_e = myresult[0][3]

    sql = 'SELECT * FROM alamat_blockchains WHERE id_blockchain='+str(id_blockchain)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    alamat_blockchains = []
    for result in myresult:
      alamat_blockchains.append(result[1])

    leader_address = request_to_get_leader(alamat_blockchains, 0)

    if leader_address == -1:
      return "-1"

    PARAMS = {'sender_n': sender_n,
              'sender_e': sender_e,
              'sender_d': sender_d,
              'receiver_n': receiver_n,
              'receiver_e': receiver_e
    }

    URL = leader_address + '/vote'

    r = requests.get(url = URL, params = PARAMS)

    return r.text
  except:
    print('There is something wrong')
    return "0"
  else: 
    return "1"

if __name__ == '__main__':
  app.run(host='localhost', port=8081, debug=True)


