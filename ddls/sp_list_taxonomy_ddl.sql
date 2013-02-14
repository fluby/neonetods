DROP TABLE IF EXISTS species_lists.taxonomy_mammals CASCADE;
CREATE TABLE species_lists.taxonomy_mammals
(
   taxon_id         varchar(255),
   spp_id           varchar(255)     NOT NULL,
   source_id        varchar(255),
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
ALTER TABLE species_lists.taxonomy_mammals
   ADD CONSTRAINT taxonomy_mammals_pkey PRIMARY KEY (spp_id);

COMMENT ON TABLE species_lists.mammals IS 'based on Wilson and Reeder, 2005';
SET search_path TO species_lists;
COMMENT ON COLUMN mammals.itis_number IS 'Integrated Taxonomic Information System';

COMMIT;
------------------------------------------------------------------------
---Bird species_lists
---based on eBird
---More notes

DROP TABLE IF EXISTS species_lists.taxonomy_birds CASCADE;
CREATE TABLE species_lists.taxonomy_birds
(
   taxon_id         varchar(255),
   spp_id           varchar(255)     NOT NULL,
   source_id        varchar(255),
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
------------------------------------------------------------------------
---Beetle species_lists
---based on XXX
---More notes

DROP TABLE IF EXISTS species_lists.taxonomy_inverts CASCADE;
CREATE TABLE species_lists.taxonomy_inverts
(
   taxon_id         varchar(255),
   spp_id           varchar(255)     NOT NULL,
   source_id        varchar(255),
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

ALTER TABLE species_lists.taxonomy_inverts
   ADD CONSTRAINT taxonomy_inverts_pkey PRIMARY KEY (spp_id);
   
SET search_path TO species_lists;
COMMENT ON COLUMN inverts.itis_number IS 'Integrated Taxonomic Information System';
   
---beetles requires foreign key, but there are multiple genera in the beetles 
---table that does not appear in the high level table - RESOLUTION needed

COMMIT;
----------------------------------------------------------------------------
---Plant species_lists table
---from USDA plants (plants.gov)

DROP TABLE IF EXISTS species_lists.taxonomy_plants CASCADE;
CREATE TABLE species_lists.taxonomy_plants
(
   taxon_id         varchar(255),
   spp_id           varchar(255)     NOT NULL,
   source_id        varchar(255),
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
ALTER TABLE species_lists.taxonomy_plants
   ADD CONSTRAINT taxonomy_plants_pkey PRIMARY KEY (spp_id);
   
/*ALTER TABLE species_lists.plants
  ADD CONSTRAINT plants_taxon_id_fkey FOREIGN KEY (taxon_id, genus)
  REFERENCES species_lists.high_level (taxon_id,genus)
   ON UPDATE NO ACTION
   ON DELETE NO ACTION;*/
   
COMMENT ON TABLE species_lists.plants IS 'from USDA plants (plants.gov)';
SET search_path TO species_lists;
COMMENT ON COLUMN plants.itis_number IS 'Integrated Taxonomic Information System';

COMMIT;
----------------------------------------------------------------------------

DROP TABLE IF EXISTS species_lists.taxonomy_herps CASCADE;
CREATE TABLE species_lists.taxonomy_herps
(
   taxon_id         varchar(255),
   spp_id           varchar(255)     NOT NULL,
   source_id        varchar(255),
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
ALTER TABLE species_lists.taxonomy_herps
   ADD CONSTRAINT taxonomy_herps_pkey PRIMARY KEY (spp_id);
