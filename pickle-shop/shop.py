#!/usr/local/bin/env python

import os
import random

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

select_employee = session.prepare("""
    SELECT * FROM pickle.employees
""")
select_employee.consistency_level = ConsistencyLevel.QUORUM

select_timesheet = session.prepare("""
    SELECT * FROM pickle.timesheets
    WHERE employee_id = ?
""")
select_timesheet.consistency_level = ConsistencyLevel.QUORUM



# synchronous execution of prepared statements
print 'Finding all employees...'

employee_ids = []
result = session.execute(select_employee)
for row in result:
    employee_ids.append(row.employee_id)

print 'Found %s employees!' % len(employee_ids)



# sample workforce activity for 10 employees
sample = random.sample(employee_ids, 10)

# asynchronous multi-get
print 'Perform multiple asynchronous read queries...'

futures = []
for employee_id in sample:
    future = session.execute_async(select_timesheet, (employee_id,))
    futures.append(future)



# process returned results

print 'Total Pickles Picked'
print '===================='

for future in futures:
    result = future.result()

    employee_id = None
    pickle_counts = 0
    for row in result:
        employee_id = row.employee_id
        pickle_counts += row.pickle_count

    if employee_id:
        print '%s: %s' % (employee_id, pickle_counts)
