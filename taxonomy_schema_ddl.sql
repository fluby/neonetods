--DoDoBASE: TAXONOMY SCHEMA--

---High Level Taxonomy table
---Cross taxa taxonomic info from the genus level and higher
---all fields do not have to be filled in for all taxa
---minimum reqs: kingdom, phylum, class, order_name, family, genus
---order has the field name of order_name to avoid confusion with SQL function

DROP TABLE taxonomy.high_level CASCADE;
CREATE TABLE taxonomy.high_level
(
   taxon_id                         varchar(255)     NOT NULL,
   resource_id_family_up    				varchar(255),
   kingdom                          varchar(255),
   subkingdom                       varchar(255),
   superdivision                    varchar(255),
   phylum_or_division               varchar(255),
   subdivision                      varchar(255),
   class                            varchar(255),
   subclass                         varchar(255),
   order_name                       varchar(255),
   family                           varchar(255),
   family_common                    varchar(255),
   resource_id_subfamily_down	  		varchar(255),
   subfamily                        varchar(255),
   tribe                            varchar(255),
   genus                            varchar(255)     NOT NULL,
   notes                            text
);

ALTER TABLE taxonomy.high_level
   ADD CONSTRAINT high_level_pkey PRIMARY KEY (taxon_id, genus);
   
COMMENT ON TABLE taxonomy.high_level IS 'Cross taxa taxonomic info from the genus level and higher';

COMMIT;
---------------------------------------------------------------------
---Mammals of North America taxonomy
---based on Wilson and Reeder, 2005
---the only discrepancy is the inclusion of Microtus mogollonensis
---itis numbers still need to be filled in

DROP TABLE taxonomy.mammals CASCADE;
CREATE TABLE taxonomy.mammals
(
   taxon_id         varchar(255),
   spp_id           varchar(255)     NOT NULL,
   resource_id      varchar(255),
   scientific_name  varchar(255),
   genus            varchar(255),
   subgenus         varchar(255),
   species          varchar(255),
   subspecies       varchar(255),
   authority_name   varchar(255),
   authority_year   numeric,
   itis_number      numeric,
   common_name      varchar(255)
);
ALTER TABLE taxonomy.mammals
   ADD CONSTRAINT mammals_pkey PRIMARY KEY (spp_id);

ALTER TABLE taxonomy.mammals
  ADD CONSTRAINT mammals_taxon_id_fkey FOREIGN KEY (taxon_id, genus)
  REFERENCES taxonomy.high_level (taxon_id,genus)
   ON UPDATE NO ACTION
   ON DELETE NO ACTION;

COMMENT ON TABLE taxonomy.mammals IS 'based on Wilson and Reeder, 2005';
SET search_path TO taxonomy;
COMMENT ON COLUMN mammals.itis_number IS 'Integrated Taxonomic Information System';

COMMIT;
------------------------------------------------------------------------
---Beetle taxonomy
---based on XXX
---More notes

DROP TABLE taxonomy.beetles CASCADE;
CREATE TABLE taxonomy.beetles
(
   taxon_id         varchar(255),
   spp_id           varchar(255)     NOT NULL,
   resource_id      varchar(255),
   scientific_name  varchar(255),
   genus            varchar(255),
   subgenus         varchar(255),
   species          varchar(255),
   subspecies       varchar(255),
   authority_name   varchar(255),
   authority_year   numeric,
   itis_number      numeric,
   common_name      varchar(255)
);

ALTER TABLE taxonomy.beetles
   ADD CONSTRAINT beetles_pkey PRIMARY KEY (spp_id);
   
SET search_path TO taxonomy;
COMMENT ON COLUMN beetles.itis_number IS 'Integrated Taxonomic Information System';
   
---beetles requires foreign key, but there are multiple genera in the beetles 
---table that does not appear in the high level table - RESOLUTION needed

COMMIT;
------------------------------------------------------------------------
---Mosquito taxonomy
---based on XXX
---More notes

DROP TABLE taxonomy.mosquitoes CASCADE;
CREATE TABLE taxonomy.mosquitoes
(
   taxon_id         varchar(255),
   spp_id           varchar(255)     NOT NULL,
   resource_id      varchar(255),
   scientific_name  varchar(255),
   genus            varchar(255),
   subgenus         varchar(255),
   species          varchar(255),
   subspecies       varchar(255),
   authority_name   varchar(255),
   authority_year   numeric,
   itis_number      numeric,
   common_name      varchar(255)
);
ALTER TABLE taxonomy.mosquitoes
   ADD CONSTRAINT mosquitoes_pkey PRIMARY KEY (spp_id);
   
ALTER TABLE taxonomy.mosquitoes
  ADD CONSTRAINT mosquitoes_taxon_id_fkey FOREIGN KEY (taxon_id, genus)
  REFERENCES taxonomy.high_level (taxon_id,genus)
   ON UPDATE NO ACTION
   ON DELETE NO ACTION;

SET search_path TO taxonomy;
COMMENT ON COLUMN mosquitoes.itis_number IS 'Integrated Taxonomic Information System';

COMMIT;

----------------------------------------------------------------------------
---Plant taxonomy table
---from USDA plants (plants.gov)

DROP TABLE taxonomy.plants CASCADE;
CREATE TABLE taxonomy.plants
(
   taxon_id                   varchar(255),
   resource_id                varchar(255),
   spp_id                     varchar(255)     NOT NULL,
   scientific_name            varchar(255),
   hybrid_genus_indicator     varchar(1),
   genus                      varchar(255),
   hybrid_sp_indicator        varchar(1),
   species_epithet            varchar(255),
   subspecies                 varchar(255),
   variety                    varchar(255),
   genera_binomial_author     varchar(255),
   trinomial_author           varchar(255),
   quadranomial_author        varchar(255),
   parents                    varchar(255),
   common_name                varchar(255),
   usdaplants_floristic_area  varchar(255),
   category                   varchar(255),
   itis_number                numeric,
   duration                   varchar(255),
   growth_habit               varchar(255)
);
ALTER TABLE taxonomy.plants
   ADD CONSTRAINT plants_pkey PRIMARY KEY (spp_id);
   
ALTER TABLE taxonomy.plants
  ADD CONSTRAINT plants_taxon_id_fkey FOREIGN KEY (taxon_id, genus)
  REFERENCES taxonomy.high_level (taxon_id,genus)
   ON UPDATE NO ACTION
   ON DELETE NO ACTION;
   
COMMENT ON TABLE taxonomy.plants IS 'from USDA plants (plants.gov)';
SET search_path TO taxonomy;
COMMENT ON COLUMN plants.itis_number IS 'Integrated Taxonomic Information System';

COMMIT;

---TO DO: add Bird taxonomy table  - eBird or Hurlbert table?
---TO DO: add synonomy table for beetles (and mosquitoes?)
