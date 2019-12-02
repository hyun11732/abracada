import mysql.connector as con
import pandas as pd

mydb = con.connect(
  host="localhost",
  user="myusername",
  passwd="mypassword"
)
