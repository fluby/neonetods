import dodobase.data as data
DATA_DIR = '/'.join(data.__file__.split('/')[:-1]) + '/'

output_csv_args = ('email', 'password')
connection_args = ('user', 'password', 'host', 'db')

groups = ['mammals', 'birds', 'plants', 'inverts', 'herps']