import config
import pg_interface as p

def get_spp_list(taxon, site, *connection_args):
    if not connection_args: connection_args = config.connection_args
    p.get_connection(*connection_args)

    c = p.connection
    cur = c.cursor()

    cur.execute("""SELECT DISTINCT t.spp_id, t.scientific_name, t.common_name 
    FROM species_lists.%s s 
    JOIN taxonomy.%s t ON s.spp_id=t.spp_id 
    WHERE s.site_id='%s' 
    ORDER BY t.spp_id;""" % (taxon, taxon, site))
    return cur.fetchall()
