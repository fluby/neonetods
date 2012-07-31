import psycopg2 as dbapi
import getpass


def main(user=None, password=None):
    connection = dbapi.connect(
                               host='serenity.bluezone.usu.edu',
                               port=5432,
                               user=user if user else raw_input('Username:'),
                               password=password if password else getpass.getpass(),
                               database='dodobase',
                               )
    cursor = connection.cursor()


if __name__ == '__main__':
    main()
