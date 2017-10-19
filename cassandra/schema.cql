CREATE KEYSPACE IF NOT EXISTS pickle
  WITH replication = {'class': 'NetworkTopologyStrategy', 'pickle-east': 1 };

CREATE TABLE IF NOT EXISTS pickle.employees (
  employee_id uuid,
  PRIMARY KEY ((employee_id))
) WITH comment = 'Table with all employee IDs.';

CREATE TABLE IF NOT EXISTS pickle.timesheets (
  employee_id uuid,
  pickle_tree_id uuid,
  timestamp timeuuid,
  pickle_count int,
  pickle_avg_size float,
  watered boolean,
  PRIMARY KEY ((employee_id), pickle_tree_id, timestamp)
) WITH CLUSTERING ORDER BY (pickle_tree_id ASC, timestamp DESC)
  AND comment = 'The most recent employee visits for each pickle tree.';

CREATE TABLE IF NOT EXISTS pickle.trees (
  pickle_tree_id uuid,
  timestamp timeuuid,
  employee_id uuid,
  pickle_count int,
  pickle_avg_size float,
  watered boolean,
  PRIMARY KEY ((pickle_tree_id), timestamp)
) WITH CLUSTERING ORDER BY (timestamp DESC)
  AND comment = 'The most recent history for each pickle tree';

CREATE TABLE IF NOT EXISTS pickle.production (
  pickle_count int,
  pickle_tree_id uuid,
  timestamp timeuuid,
  PRIMARY KEY ((pickle_count), pickle_tree_id, timestamp)
) WITH CLUSTERING ORDER BY (pickle_tree_id ASC, timestamp ASC)
  AND comment = 'How often a pickle tree produces the same number of pickles.';


CREATE KEYSPACE IF NOT EXISTS reaper_db
  WITH replication = {'class': 'NetworkTopologyStrategy', 'pickle-east': 1 };
