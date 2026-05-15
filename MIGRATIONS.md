# Database Migrations Guide

This project uses **Alembic** for database schema migrations.

## Setup

Alembic has been initialized and configured in this project:
- Configuration: `alembic.ini`
- Migration scripts: `alembic/versions/`
- Environment setup: `alembic/env.py`

## Common Commands

### Apply all pending migrations
```bash
alembic upgrade head
```

### View current database revision
```bash
alembic current
```

### View migration history
```bash
alembic history
```

### Create a new migration after model changes
```bash
# Automatically generate based on model changes
alembic revision --autogenerate -m "Description of changes"

# Create empty migration (for custom SQL)
alembic revision -m "Description of changes"
```

### Rollback to previous revision
```bash
# Rollback one revision
alembic downgrade -1

# Rollback to specific revision
alembic downgrade <revision_id>
```

## Workflow

1. **Modify your models** in `models/user.py` or `models/order.py`
2. **Generate a migration**:
   ```bash
   alembic revision --autogenerate -m "Add field to model"
   ```
3. **Review the generated migration** in `alembic/versions/`
4. **Apply the migration**:
   ```bash
   alembic upgrade head
   ```

## Initial Migration

The initial migration creates:
- `users` table with columns: id, username, email, password, is_superuser, created_at, updated_at
- `orders` table with columns: id, user_id, items, total_price, status, delivery_address, created_at, updated_at
- Foreign key constraint: orders.user_id → users.id
- Unique indexes on: users.username, users.email

## Database Requirements

- PostgreSQL database must be running
- DATABASE_URL environment variable or database configuration in `alembic.ini`
- Database name as specified in DATABASE_URL must exist

## Example: Creating and applying a migration

```bash
# 1. Modify your model (e.g., add a new field to User)
# Edit models/user.py

# 2. Generate migration
alembic revision --autogenerate -m "Add phone field to users"

# 3. Review and optionally edit alembic/versions/<revision_id>.py

# 4. Apply the migration
alembic upgrade head

# 5. Verify the migration was applied
alembic current
```

## Troubleshooting

- **"Cannot connect to database"**: Ensure PostgreSQL is running and DATABASE_URL is correct
- **"No changes detected"**: Make sure you modified the model class definition
- **"Alembic command not found"**: Install alembic: `pip install alembic`

For more information, see [Alembic Documentation](https://alembic.sqlalchemy.org/)
