--CREATE SCHEMA sources;
--DoDoBASE: SOURCES SCHEMA--

---Master Sources Table to which many other schemas reference 
---all sources should also be stored in Mendeley

DROP TABLE IF EXISTS sources.sources CASCADE;
CREATE TABLE sources.sources
(
   source_id    varchar(1000)    NOT NULL,
   info_type    varchar(255),
   file_type    varchar(255),
   notes        text,
   isbn         varchar(255),
   author       varchar(255),
   title        varchar(1000),
   journal      varchar(255),
   volume       varchar(255),
   issue        varchar(255),
   pages        varchar(255),
   year         integer null,
   url          varchar(255),
   tags         varchar(1000),
   spat_scale   varchar(255),
   spat_extent  varchar(255)
);

ALTER TABLE sources.sources
   ADD CONSTRAINT sources_pkey PRIMARY KEY (source_id);
   
COMMENT ON TABLE sources.sources IS 'all sources should also be stored in Mendeley';
SET search_path TO sources;
COMMENT ON COLUMN sources.info_type IS 'e.g., taxonomic reference, dataset, species list - see Mendeley tags table';
COMMENT ON COLUMN sources.tags IS 'all Mendeley tags (see NEON-provided list) in one column, separated by semi-colons';

COMMIT;
