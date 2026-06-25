<!-- dynamo-canary GUID: keep-the-original-guid-from-the-scaffold -->

Read the Apache-style access log at /app/access.log and create a JSON report at /app/log_report.json.

Parse each non-empty valid log line that matches this structure:

<client_ip> <identity> <user> [<timestamp>] "<method> <path> <protocol>" <status_code> <size>

The output file /app/log_report.json must be a valid JSON object with exactly these keys:

- "total_requests": an integer count of parsed valid log entries.
- "status_counts": an object whose keys are HTTP status codes as strings and whose values are integer counts. Sort the status-code keys in ascending string order.
- "top_ip": the client IP address that appears most often. If there is a tie, choose the lexicographically smallest IP address.
- "top_path": the request path that appears most often. If there is a tie, choose the lexicographically smallest path.
- "error_rate": the number of parsed requests with 4xx or 5xx status codes divided by total_requests, rounded to 4 decimal places.

Do not modify /app/access.log. Do not write the answer anywhere except /app/log_report.json.

You have 120 seconds to complete this task. Do not cheat by using online solutions or hints specific to this task.