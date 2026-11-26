"""Background watcher: polls smilebus.by for active requests.

TODO: asyncio loop every POLL_INTERVAL_SECONDS: load active requests,
call the API, compare with last_seen_schedule, notify users.
"""
