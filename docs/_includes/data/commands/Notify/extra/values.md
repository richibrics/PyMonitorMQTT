### Set values for the notification

For this command you can configure:
1. Notification title
2. Notification message

These data can be set in two ways:
1. From configuration file
2. Directly from the trigger message

If data are passed via message, these will be used; if not, the settings will be taken from the configuration file; if you don't set them in the configuration file, default data will be used.

Default data:
- Title: Notification
- Message: PyMonitorMQTT

Title and message can be set together, only one of them or none.