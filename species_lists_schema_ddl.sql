--DoDoBASE: SPECIES LISTS SCHEMA--

---Species Lists Table
---lists of species at, near, or surrounding NEON sites
---includes only NEON taxa: ground beetles, mosquitoes, small mammals, plants, birds
---conservation status is included here, because status can vary across the geographical range of a species
---status should include state and federal listings

DROP TABLE species_lists.species_lists CASCADE;
CREATE TABLE species_lists.species_lists
(
   resource_id_list  				 varchar(255)    NOT NULL,
   site_id                   char(4)         NOT NULL,
   spp_id                    varchar(255)    NOT NULL,
   resource_id_status        varchar(255),
   status                    varchar(255)
);

ALTER TABLE species_lists.species_lists
   ADD CONSTRAINT species_lists_pkey PRIMARY KEY (resource_id_list, site_id, spp_id);

ALTER TABLE species_lists.species_lists
  ADD CONSTRAINT species_lists_site_id_fkey FOREIGN KEY (site_id)
  REFERENCES site_data.site_info_v11 (site_id)
   ON UPDATE NO ACTION
   ON DELETE NO ACTION;

COMMIT;

---------------------------------------------------------------------------------------------------

DROP TABLE species_lists.spatial_info CASCADE;
CREATE TABLE species_lists.spatial_info
(
   resource_id_list  				 varchar(255)    NOT NULL,
   spatial_scale             varchar(255),
   spatial_extent            numeric
);

ALTER TABLE species_lists.spatial_info
   ADD CONSTRAINT spatial_info_pkey PRIMARY KEY (resource_id_list);

COMMIT;

-----------------------------------------------------------------------------------------------------

DROP TABLE species_lists.herps_species_lists CASCADE;
CREATE TABLE species_lists.herps_species_lists
(
   resource_id_list  				 varchar(255)    NOT NULL,
   site_id                   char(4)         NOT NULL,
   order_name                varchar(255),
   family                    varchar(255),
   species                   varchar(255)    NOT NULL,
   common_name               varchar(255),
   resource_id_status        varchar(255),
   status                    varchar(255)
);

ALTER TABLE species_lists.herps_species_lists
   ADD CONSTRAINT herps_species_lists_pkey PRIMARY KEY (resource_id_list, site_id, species);

ALTER TABLE species_lists.herps_species_lists
  ADD CONSTRAINT herps_species_lists_site_id_fkey FOREIGN KEY (site_id)
  REFERENCES site_data.site_info_v11 (site_id)
   ON UPDATE NO ACTION
   ON DELETE NO ACTION;

COMMIT;
