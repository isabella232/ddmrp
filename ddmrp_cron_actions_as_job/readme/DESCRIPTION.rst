DDMRP Buffer calculations are now run with Queue Jobs.

When auto-update of NFP is active, each time the state of a stock move changes,
a new computation is triggered, but thanks to identity keys on jobs, only one
job at a time is generated for the same buffer.

The ``<stock.buffer>.cron_actions`` method is automatically delayed when the
context contains ``auto_delay_ddmrp_cron_actions=True``.
