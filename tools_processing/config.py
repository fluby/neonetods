import sys
#first try server location, if on local machine, define in except statement
try: 
    sys.path.append('/home/fsu/sp_list_processing')
    import data as data ##requires init file in directory
    DATA_DIR = '/'.join(data.__file__.split('/')[:-1]) + '/'
except: DATA_DIR = K:\FSU1\Technician_Shared_Documents\Julia\dodobase\code\entered_data.pkl

#Sentinelia log-in info
mendeley_args = ('fsu.neoninc@gmail.com', 'insertpasswordhere')

#define taxonomic groups
groups = ['mammals', 'birds', 'plants', 'inverts', 'herps']