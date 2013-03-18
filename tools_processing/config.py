import sys
#first try server location, if on local machine, define in except statement
try: 
    sys.path.append('/home/fsu/neon_portal')
    import dodobase.data as data
    DATA_DIR = '/'.join(data.__file__.split('/')[:-1]) + '/'
except: DATA_DIR = 'insertlocaldirectoryhere'

#Sentinelia log-in info
mendeley_args = ('fsu.neoninc@gmail.com', 'insertpasswordhere')

#define taxonomic groups
groups = ['mammals', 'birds', 'plants', 'inverts', 'herps']