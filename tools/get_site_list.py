import config
import pg_interface as p

def get_site_list(*connection_args):
    if not connection_args: connection_args = config.connection_args
    p.get_connection(*connection_args)

    c = p.connection
    cur = c.cursor()

    cur.execute("SELECT DISTINCT site_id FROM site_data.site_info ORDER BY site_id;")
    return [c[0] for c in cur.fetchall()]
