--DoDoBASE: SPECIES LISTS SCHEMA--

---Species Lists Table
---lists of species at, near, or surrounding NEON sites
---includes only NEON taxa: ground beetles, mosquitoes, small mammals, plants, birds
---conservation status is included here, because status can vary across the geographical range of a species
---status should include state and federal listings

DROP TABLE species_lists.species_lists CASCADE;
CREATE TABLE species_lists.species_lists
(
   source_id  				 varchar(255)    NOT NULL,
   site_id                   char(4)         NOT NULL,
   spp_id                    varchar(255)    NOT NULL
);

ALTER TABLE species_lists.species_lists
   ADD CONSTRAINT species_lists_pkey PRIMARY KEY (source_id, site_id, spp_id);

ALTER TABLE species_lists.species_lists
  ADD CONSTRAINT species_lists_site_id_fkey FOREIGN KEY (site_id)
  REFERENCES site_data.site_info_v11 (site_id)
   ON UPDATE NO ACTION
   ON DELETE NO ACTION;

COMMIT;

---------------------------------------------------------------------------------------------------

DROP TABLE species_lists.herps_species_lists CASCADE;
CREATE TABLE species_lists.herps_species_lists
(
   source_id  				 varchar(255)    NOT NULL,
   site_id                   char(4)         NOT NULL,
   order_name                varchar(255),
   family                    varchar(255),
   species                   varchar(255)    NOT NULL,
   common_name               varchar(255)
);

ALTER TABLE species_lists.herps_species_lists
   ADD CONSTRAINT herps_species_lists_pkey PRIMARY KEY (source_id, site_id, species);

ALTER TABLE species_lists.herps_species_lists
  ADD CONSTRAINT herps_species_lists_site_id_fkey FOREIGN KEY (site_id)
  REFERENCES site_data.site_info_v11 (site_id)
   ON UPDATE NO ACTION
   ON DELETE NO ACTION;

COMMIT;

---------------------------------------------------------------------------------------------------

DROP TABLE species_lists.status CASCADE;
CREATE TABLE species_lists.status
(
   spp_id  				varchar(255)    NOT NULL,
   state                varchar(255)    NOT NULL,
   status               varchar(255),
   notes                varchar(255)
);

ALTER TABLE species_lists.status
   ADD CONSTRAINT status_pkey PRIMARY KEY (spp_id, state);

COMMIT;
