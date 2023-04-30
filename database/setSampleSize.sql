--TABLESAMPLE BERNOULLI method samples directly on each row of the underlying relation. This sampling method will actually scan
--the whole relation and randomly pick individual tuples (it basically does "coin flip" for each tuple).
--The number XX after TABLESAMPLE BERNOULLI  (XX) returns XX% of rows using BERNOULLI method

DELETE FROM test.verwerk_project WHERE id IN (
SELECT id FROM test.verwerk_project TABLESAMPLE BERNOULLI  (80)
);

DELETE FROM test.project WHERE id NOT IN (
SELECT id FROM test.verwerk_project
)