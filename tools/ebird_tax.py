import xlrd
import sys
reload(sys)
sys.setdefaultencoding('latin-1')

tax_file = '../data/ebird-taxonomy-1-52_12-aug-2011.xls'
output_file = '../data/ebird_tax_clean.csv'

book = xlrd.open_workbook(tax_file)
sheet = book.sheet_by_index(0)
rows = sheet.nrows

output = open(output_file, 'w')
output.write('spp_id,scientific_name,common_name')
for i in range(1, rows):
    row = sheet.row(i)
    if row:
        _, sp_type, sci_name, comm_name, _, spp_id = [str(s.value) for s in row]
        if sp_type == 'species':
            output.write('\n%s,%s,%s' % (spp_id, sci_name, comm_name))