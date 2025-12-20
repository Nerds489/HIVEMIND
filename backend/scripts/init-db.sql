-- =============================================================================
-- HIVEMIND Database Initialization Script
-- =============================================================================
-- This script runs when PostgreSQL container first starts.
-- Creates necessary extensions and initial schema setup.

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- For fuzzy text search
CREATE EXTENSION IF NOT EXISTS "btree_gin"; -- For GIN indexes on scalars

-- Create custom types
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'task_status') THEN
        CREATE TYPE task_status AS ENUM (
            'pending',
            'running',
            'completed',
            'failed',
            'cancelled'
        );
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'agent_state') THEN
        CREATE TYPE agent_state AS ENUM (
            'idle',
            'pending',
            'running',
            'success',
            'error',
            'paused'
        );
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'team_id') THEN
        CREATE TYPE team_id AS ENUM (
            'DEV',
            'SEC',
            'INF',
            'QA'
        );
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'message_type') THEN
        CREATE TYPE message_type AS ENUM (
            'user',
            'assistant',
            'system',
            'tool_use',
            'tool_result'
        );
    END IF;
END$$;

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE hivemind TO hivemind;

-- Log initialization
DO $$
BEGIN
    RAISE NOTICE 'HIVEMIND database initialized successfully';
END$$;
