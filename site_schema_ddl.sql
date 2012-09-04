--CREATE SCHEMA site_data;
--DoDoBASE: SITE DATA SCHEMA--
 
---Site Info Table
---provided by NEON EHS, versioning from EHS
DROP TABLE IF EXISTS site_data.site_info CASCADE;
CREATE TABLE site_data.site_info
(
   domain_number                     varchar(255),
   domain_name                       varchar(255),
   site_id                           varchar(4)     NOT NULL,
   site_name                         varchar(255),
   site_type                         varchar(255),
   latitude                          numeric,
   longitude                         numeric,
   zone                              integer,
   easting                           numeric,
   northing                          numeric,
   source                            varchar(255),
   ownership                         varchar(255),
   notes                             varchar(255),
   state                             varchar(255),
   county                            varchar(255),
   nearest_city                      varchar(255),
   distance_to_city_mi       		numeric null,
   existing_infrastructure		varchar(255),
   website                           varchar(255),
   additional_website                varchar(255)
);

ALTER TABLE site_data.site_info
   ADD CONSTRAINT pk_site_info_site_id PRIMARY KEY (site_id);

COMMENT ON TABLE site_data.site_info IS 'provided by NEON EHS, versioning from EHS';
SET search_path TO site_data;
COMMENT ON COLUMN site_info.domain_number IS 'NEON-assigned, 1-20';
COMMENT ON COLUMN site_info.domain_name IS 'NEON-assigned';
COMMENT ON COLUMN site_info.site_id IS 'FSU-assigned';
COMMENT ON COLUMN site_info.site_type IS 'NEON use - core or relocatable';
COMMENT ON COLUMN site_info.latitude IS 'in decimal degrees';
COMMENT ON COLUMN site_info.longitude IS 'in decimal degrees';
COMMENT ON COLUMN site_info.source IS 'source of coordinates';

COMMIT;

------------------------------------------------------------------------------
--Site Personnel table
--TO DO: ultimately merge with Mel's table of DSECC and collections folk
DROP TABLE IF EXISTS site_data.site_personnel CASCADE;
CREATE TABLE site_data.site_personnel
(
   site_id        varchar(4)    	NOT NULL,
   contact_name   varchar(255)    	NOT NULL,
   contact_title  varchar(255),
   contact_phone  varchar(255),
   contact_email  varchar(255),
   affiliation    varchar(255),
   specialty      varchar(255),
   url            varchar(255)
);

ALTER TABLE site_data.site_personnel
   ADD CONSTRAINT site_personnel_pkey PRIMARY KEY (site_id, contact_name);
   
ALTER TABLE site_data.site_personnel
  ADD CONSTRAINT site_personnel_site_id_fkey FOREIGN KEY (site_id)
  REFERENCES site_data.site_info (site_id)
   ON UPDATE NO ACTION
   ON DELETE NO ACTION;
   
SET search_path TO site_data;
COMMENT ON COLUMN site_personnel.specialty IS 'in NEON-relevant terms';

COMMIT;
