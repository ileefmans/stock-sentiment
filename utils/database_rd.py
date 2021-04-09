import mysql.connector
import argparse


def get_args():
	parser = argparse.ArgumentParser(description="Model Options")
    parser.add_argument("user", type=str, help="mysql user")
    parser.add_argument("password", type=str, help="mysql password")
    parser.add_argument("--host", type=str, default='127.0.0.1', help="mysql host")
    return parser.parse_args()


args  = get_args()
user = args.user
password = args.password
host = args.host

# Establish connection and create cursor
conn = mysql.connector.connect(user=user, password=password, host=host)
cursor = conn.cursor()
cursor.execute("CREATE database STOCKS")

