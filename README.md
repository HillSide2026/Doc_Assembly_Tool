# Document Assembly Tool

This project is a minimal Python/Flask starter for a document assembly application. It provides a basic web endpoint and includes dependencies for working with Word documents, with folders ready for templates, generated output, and data sources.

## Engagement File Structure (Authoritative)

All generated documents are written to:

engagements/{engagement_id}/

Each engagement directory contains:

- intake.json
- engagement_vN.docx
- engagement_vN.pdf
- manifest.json

Files are never overwritten. New versions increment `vN`.
