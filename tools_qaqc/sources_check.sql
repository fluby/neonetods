DROP TABLE IF EXISTS sources.allodem;

SELECT DISTINCT source_id
INTO sources.allodem
FROM species_lists.inverts
UNION ALL
SELECT DISTINCT source_id
FROM species_lists.birds
UNION ALL
SELECT DISTINCT source_id
FROM species_lists.mammals
UNION ALL
SELECT DISTINCT source_id
FROM species_lists.herps
UNION ALL
SELECT DISTINCT source_id
FROM species_lists.plants;

DROP TABLE IF EXISTS sources.failed;

SELECT DISTINCT(allodem.source_id)
INTO sources.failed 
FROM sources.allodem
LEFT JOIN sources.sources ON allodem.source_id = sources.source_id
WHERE sources.source_id IS NULL;
