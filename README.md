# avertica

This library contains asynchonous wrappers for the connection and cursor
objects in `vertica-python` library to interact with Vertica database.
It supports simple select queries yet, and there is no transactions,
commit and rollback asynchonous functionality.

Usage example:

```python
import avertica

async with avertica.connect(**conn_info) as conn:
    async with conn.cursor() as cur:
        await cur.execute(query)
        rows = cur.fetchall()
```
