# Current

Find the documents your accountant needs and send them to the right return in Current.

Install Current in your assistant, then sign in to Current when asked to connect. You need an existing Current client portal login and an assistant account that permits plugins. Your organization may restrict plugin installation.

Ask: “Use Current to help me find the documents my accountant still needs.” Your assistant reads your outstanding requests, asks which return you mean if necessary, and searches only the sources you authorize. Before uploading, it confirms the files and destination with you.

The plugin contains one document collection skill and one remote Current MCP connector. It can discover authorized destinations, read document requests, authorize uploads, and verify your upload receipts. It does not expose your accountant's internal notes or return contents. Uploaded files and document request data are handled by Current and your assistant; files from other services require your separate access to those services.

Uploading requires an assistant runtime that can read your files and send an outbound HTTP upload. If that capability is unavailable, use the Current portal to upload; the assistant must not report success until Current confirms receipt. A receipt confirms delivery, not accountant review.

Disconnect Current in your portal's connected-app settings to revoke its access. Removing the plugin alone is not a substitute for revoking Current's authorization.
