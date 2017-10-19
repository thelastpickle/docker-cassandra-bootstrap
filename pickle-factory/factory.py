#!/usr/local/bin/env python

import os
import random
import uuid

from cassandra import ConsistencyLevel
from cassandra.io.libevreactor import LibevConnection
from cassandra.cluster import Cluster
from cassandra.policies import DCAwareRoundRobinPolicy



# connect to Cassandra

CASSANDRA_HOST = os.environ['CASSANDRA_HOST']
CASSANDRA_DC = os.environ['CASSANDRA_DC']
cluster = Cluster([CASSANDRA_HOST],
                  load_balancing_policy=DCAwareRoundRobinPolicy(
                      local_dc=CASSANDRA_DC), )
cluster.connection_class = LibevConnection
session = cluster.connect()



# prepare statements
print 'Preparing statements...'

insert_employee = session.prepare("""
    INSERT INTO pickle.employees
      (employee_id)
    VALUES
      (?)
""")
insert_employee.consistency_level = ConsistencyLevel.QUORUM

insert_timesheet = session.prepare("""
    INSERT INTO pickle.timesheets
      (employee_id, pickle_tree_id, timestamp, pickle_count, pickle_avg_size, watered)
    VALUES
      (?, ?, ?, ?, ?, ?)
""")
insert_timesheet.consistency_level = ConsistencyLevel.QUORUM

insert_tree = session.prepare("""
    INSERT INTO pickle.trees
      (pickle_tree_id, timestamp, employee_id, pickle_count, pickle_avg_size, watered)
    VALUES
      (?, ?, ?, ?, ?, ?)
""")
insert_tree.consistency_level = ConsistencyLevel.ONE

insert_production = session.prepare("""
    INSERT INTO pickle.production
      (pickle_count, pickle_tree_id, timestamp)
    VALUES
      (?, ?, ?)
""")
insert_production.consistency_level = ConsistencyLevel.ONE



# generate employee_ids
print 'Generating employee IDs...'

futures = []
employee_uuids = []
pickle_tree_ids = []
for _ in xrange(100):
    employee_uuid = uuid.uuid4()  # random uuid

    future = session.execute_async(insert_employee, (employee_uuid,))
    employee_uuids.append(employee_uuid)

    pickle_tree_id = uuid.uuid4()  # randome uuid
    pickle_tree_ids.append(pickle_tree_id)

# confirm all futures were written
while futures:
    print 'Committing employee information...'
    future = futures.pop()
    future.result()



# generate simulated workforce

for _ in xrange(100000):
    employee_uuid = random.choice(employee_uuids)
    pickle_tree_id = random.choice(pickle_tree_ids)
    timestamp = uuid.uuid1()  # contains time information
    pickle_count = random.randint(0, 100)
    pickle_avg_size = random.uniform(0, 2)
    watered = random.randint(0, 1)

    future = session.execute_async(insert_timesheet,
                                   (employee_uuid, pickle_tree_id, timestamp,
                                    pickle_count, pickle_avg_size, watered))
    futures.append(future)

    future = session.execute_async(insert_tree,
                                   (pickle_tree_id, timestamp, employee_uuid,
                                    pickle_count, pickle_avg_size, watered))
    futures.append(future)

    future = session.execute_async(insert_production,
                                   (pickle_count, pickle_tree_id, timestamp))
    futures.append(future)

    if len(futures) > 3000:
        print 'Committing timesheets...'
        while futures:
            future = futures.pop()
            future.result()

# confirm all futures were written
while futures:
    print 'Committing last timesheets...'
    future = futures.pop()
    future.result()

print 'Done.'
