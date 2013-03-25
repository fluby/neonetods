--CREATE SCHEMA species_lists;
--DoDoBASE: SPECIES LISTS SCHEMA--

---Species Lists Table
---lists of species at, near, or surrounding NEON sites
---includes only NEON taxa: ground beetles, mosquitoes, small mammals, plants, birds
---conservation status is included here, because status can vary across the geographical range of a species
---status should include state and federal listings

DROP TABLE IF EXISTS species_lists.mammals_raw CASCADE;
CREATE TABLE species_lists.mammals_raw
(

site_id		varchar(1000)    NOT NULL,
genus		varchar(1000),
sp		varchar(1000),
subsp		varchar(1000),
common_name	varchar(1000),
source_id	varchar(1000)    NOT NULL

);


ALTER TABLE species_lists.mammals_raw
  ADD CONSTRAINT mammals_raw_site_id_fkey FOREIGN KEY (site_id)
  REFERENCES site_data.site_info_V11 (site_id);

ALTER TABLE species_lists.mammals_raw
  ADD CONSTRAINT mammals_raw_source_id_fkey FOREIGN KEY (source_id)
  REFERENCES sources.sources (source_id);

COMMIT;
---------------------------------------------------------------------------------------------------

DROP TABLE IF EXISTS species_lists.inverts_raw CASCADE;
CREATE TABLE species_lists.inverts_raw
(

site_id		varchar(1000)    NOT NULL,
genus		varchar(1000),
sp		varchar(1000),
subsp		varchar(1000),
common_name	varchar(1000),
source_id	varchar(1000)    NOT NULL

);


ALTER TABLE species_lists.inverts_raw
  ADD CONSTRAINT inverts_raw_site_id_fkey FOREIGN KEY (site_id)
  REFERENCES site_data.site_info_V11 (site_id);

ALTER TABLE species_lists.inverts_raw
  ADD CONSTRAINT inverts_raw_source_id_fkey FOREIGN KEY (source_id)
  REFERENCES sources.sources (source_id);

COMMIT;
-----------------------------------------------------------------------------------
DROP TABLE IF EXISTS species_lists.birds_raw CASCADE;
CREATE TABLE species_lists.birds_raw
(

site_id		varchar(1000)    NOT NULL,
genus		varchar(1000),
sp		varchar(1000),
subsp		varchar(1000),
common_name	varchar(1000),
source_id	varchar(1000)    NOT NULL

);


ALTER TABLE species_lists.birds_raw
  ADD CONSTRAINT birds_raw_site_id_fkey FOREIGN KEY (site_id)
  REFERENCES site_data.site_info_V11 (site_id);

ALTER TABLE species_lists.birds_raw
  ADD CONSTRAINT birds_raw_source_id_fkey FOREIGN KEY (source_id)
  REFERENCES sources.sources (source_id);

COMMIT;
-----------------------------------------------------------------------------------
DROP TABLE IF EXISTS species_lists.plants_raw CASCADE;
CREATE TABLE species_lists.plants_raw
(

site_id		varchar(1000)    NOT NULL,
genus		varchar(1000),
sp		varchar(1000),
subsp		varchar(1000),
common_name	varchar(1000),
source_id	varchar(1000)    NOT NULL

);


ALTER TABLE species_lists.plants_raw
  ADD CONSTRAINT plants_raw_site_id_fkey FOREIGN KEY (site_id)
  REFERENCES site_data.site_info_V11 (site_id);

ALTER TABLE species_lists.plants_raw
  ADD CONSTRAINT plants_raw_source_id_fkey FOREIGN KEY (source_id)
  REFERENCES sources.sources (source_id);

COMMIT;
-----------------------------------------------------------------------------------
DROP TABLE IF EXISTS species_lists.herps_raw CASCADE;
CREATE TABLE species_lists.herps_raw
(

site_id		varchar(1000)    NOT NULL,
genus		varchar(1000),
sp		varchar(1000),
subsp		varchar(1000),
common_name	varchar(1000),
source_id	varchar(1000)    NOT NULL

);

ALTER TABLE species_lists.herps_raw
  ADD CONSTRAINT herps_raw_site_id_fkey FOREIGN KEY (site_id)
  REFERENCES site_data.site_info_V11 (site_id);

ALTER TABLE species_lists.herps_raw
  ADD CONSTRAINT herps_raw_source_id_fkey FOREIGN KEY (source_id)
  REFERENCES sources.sources (source_id);

COMMIT;
-----------------------------------------------------------------------------------
-----------------------------------------------------------------------------------

DROP TABLE IF EXISTS species_lists.mammals CASCADE;
CREATE TABLE species_lists.mammals
(
   source_id  			varchar(1000)    NOT NULL,
   site_id                   varchar(4)      NOT NULL,
   spp_id                    varchar(255)    NOT NULL
);

ALTER TABLE species_lists.mammals
   ADD CONSTRAINT mammals_pkey PRIMARY KEY (source_id, site_id, spp_id);

ALTER TABLE species_lists.mammals
  ADD CONSTRAINT mammals_site_id_fkey FOREIGN KEY (site_id)
  REFERENCES site_data.site_info_v11 (site_id);

ALTER TABLE species_lists.mammals
  ADD CONSTRAINT mammals_source_id_fkey FOREIGN KEY (source_id)
  REFERENCES sources.sources (source_id);

COMMIT;

---------------------------------------------------------------------------------------------------

DROP TABLE IF EXISTS species_lists.birds CASCADE;
CREATE TABLE species_lists.birds
(
   source_id  			varchar(1000)    NOT NULL,
   site_id                   varchar(4)      NOT NULL,
   spp_id                    varchar(255)    NOT NULL
);

ALTER TABLE species_lists.birds
   ADD CONSTRAINT birds_pkey PRIMARY KEY (source_id, site_id, spp_id);

ALTER TABLE species_lists.birds
  ADD CONSTRAINT birds_site_id_fkey FOREIGN KEY (site_id)
  REFERENCES site_data.site_info_v11 (site_id);

ALTER TABLE species_lists.birds
  ADD CONSTRAINT birds_source_id_fkey FOREIGN KEY (source_id)
  REFERENCES sources.sources (source_id);

COMMIT;

---------------------------------------------------------------------------------------------------

DROP TABLE IF EXISTS species_lists.plants CASCADE;
CREATE TABLE species_lists.plants
(
   source_id  			varchar(1000)    NOT NULL,
   site_id                   varchar(4)      NOT NULL,
   spp_id                    varchar(255)    NOT NULL
);

ALTER TABLE species_lists.plants
   ADD CONSTRAINT plants_pkey PRIMARY KEY (source_id, site_id, spp_id);

ALTER TABLE species_lists.plants
  ADD CONSTRAINT plants_site_id_fkey FOREIGN KEY (site_id)
  REFERENCES site_data.site_info_v11 (site_id);

ALTER TABLE species_lists.plants
  ADD CONSTRAINT plants_source_id_fkey FOREIGN KEY (source_id)
  REFERENCES sources.sources (source_id);

COMMIT;

---------------------------------------------------------------------------------------------------

DROP TABLE IF EXISTS species_lists.inverts CASCADE;
CREATE TABLE species_lists.inverts
(
   source_id  			varchar(1000)    NOT NULL,
   site_id                   varchar(4)      NOT NULL,
   spp_id                    varchar(255)    NOT NULL
);

ALTER TABLE species_lists.inverts
   ADD CONSTRAINT inverts_pkey PRIMARY KEY (source_id, site_id, spp_id);

ALTER TABLE species_lists.inverts
  ADD CONSTRAINT inverts_site_id_fkey FOREIGN KEY (site_id)
  REFERENCES site_data.site_info_v11 (site_id);

ALTER TABLE species_lists.inverts
  ADD CONSTRAINT inverts_source_id_fkey FOREIGN KEY (source_id)
  REFERENCES sources.sources (source_id);

COMMIT;

---------------------------------------------------------------------------------------------------

DROP TABLE IF EXISTS species_lists.herps CASCADE;
CREATE TABLE species_lists.herps
(
   source_id  			varchar(1000)    NOT NULL,
   site_id                   varchar(4)      NOT NULL,
   spp_id                    varchar(255)    NOT NULL
);

ALTER TABLE species_lists.herps
   ADD CONSTRAINT herps_pkey PRIMARY KEY (source_id, site_id, spp_id);

ALTER TABLE species_lists.herps
  ADD CONSTRAINT herps_site_id_fkey FOREIGN KEY (site_id)
  REFERENCES site_data.site_info_v11 (site_id);

ALTER TABLE species_lists.herps
  ADD CONSTRAINT herps_source_id_fkey FOREIGN KEY (source_id)
  REFERENCES sources.sources (source_id);

COMMIT;

---------------------------------------------------------------------------------------------------

DROP TABLE IF EXISTS species_lists.status CASCADE;
CREATE TABLE species_lists.status
(
   spp_id  		varchar(255)    NOT NULL,
   state                varchar(255)    NOT NULL,
   fed_status           varchar(255),
   state_status         varchar(255), 
   fed_notes            varchar(1000),
   state_notes          varchar(1000),
   fed_source_id        varchar(1000),
   state_source_id      varchar(1000)
);

ALTER TABLE species_lists.status
   ADD CONSTRAINT status_pkey PRIMARY KEY (spp_id, state);

COMMIT;

DROP TABLE IF EXISTS species_lists.status_raw CASCADE;
CREATE TABLE species_lists.status_raw
(
   genus  							varchar(255),
   sp		                varchar(255),
   subsp		            varchar(255),
   state			          varchar(255), 
   federal_status       varchar(1000),
   state_status         varchar(1000),
   notes				        varchar(1000),
   state_source		      varchar(1000)
);

ALTER TABLE species_lists.status_raw
   ADD CONSTRAINT status_raw_pkey PRIMARY KEY (genus,sp,subsp,state);

COMMIT;
