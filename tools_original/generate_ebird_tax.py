import xlrd
import sys
reload(sys)
sys.setdefaultencoding('latin-1')

tax_file = '../data/eBird-Clements-taxonomy-v1-53_21-Aug-2012.xls'
output_file = '../data/ebird_tax_clean.csv'

book = xlrd.open_workbook(tax_file)
sheet = book.sheet_by_index(0)
rows = sheet.nrows
taxon_id = 'bird'
output = open(output_file, 'w')
output.write('taxon_id, spp_id, source_id, scientific_name, common_name, order_name, family_name')
for i in range(1, rows):
    row = sheet.row(i)
    if row:
        _, sp_type, spp_id, sci_name, comm_name, order1, family = [str(s.value) for s in row]
        if sp_type == 'species':
            out = '\nbird,%s,ebird,%s,%s,%s,%s' % (spp_id, sci_name, comm_name, order1, family)
            output.write(out)
output.close()