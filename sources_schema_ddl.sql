--DoDoBASE: SOURCES SCHEMA--

---Master Sources Table to which many other schemas reference 
---all sources should also be stored in Mendeley

DROP TABLE sources.sources CASCADE;
CREATE TABLE sources.sources
(
   source_id    varchar(255)    NOT NULL,
   info_type    varchar(255),
   file_type    varchar(255),
   notes        text,
   isbn         varchar(255),
   author       varchar(255),
   title        varchar(255),
   journal      varchar(255),
   volume       integer,
   issue        integer,
   pages        varchar(255),
   year         integer,
   url          varchar(255),
   tags         varchar(255)
);

ALTER TABLE sources.sources
   ADD CONSTRAINT sources_pkey PRIMARY KEY (source_id);
   
COMMENT ON TABLE sources.sources IS 'all sources should also be stored in Mendeley';
SET search_path TO sources;
COMMENT ON COLUMN sources.info_type IS 'e.g., taxonomic reference, dataset, species list - see Mendeley tags table';
COMMENT ON COLUMN sources.tags IS 'all Mendeley tags (see NEON-provided list) in one column, separated by semi-colons';

COMMIT;

---------------------------------------------------------------------
---Mendeley Tags Table 
---controlled list of tags for sources in Mendeley and in the sources table

DROP TABLE sources.mendeley_tags CASCADE;
CREATE TABLE sources.mendeley_tags
(
   domain_number    varchar(255),
   site_id          varchar(4),
   taxon            varchar(255),
   additional_tags  varchar(255),
   habitat          varchar(255),
   info_type        varchar(255)
);

COMMIT;
------------------------------------------------------------------------
