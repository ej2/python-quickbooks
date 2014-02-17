quickbooks-python
=================

This builds on the work of simonv3. I'm adding some functionality to handle additional accounting functions,
beginning with a programmatic export of a chart of accounts and a facility for generating ledger lines from transaction business objects (e.g. Bill, JournalEntry, Purchase).

I'm new to github, eager to build some cool things here, and welcome your constructive feedback on how to
improve my coding, collaboration, and knowledge base.

Update: As I try using the pnl function in report.py, I notice that not all of the activity is making it in. I have to assume it basically doesn't work then. Rather than rebuild it, though, I'm probably going to use other tools outside the  module to massage the ledger_lines I get out of massage.py (rather than build special reporting tools within the quickbooks package).

Generally when using this module (or any of the QBO v3 API wrappers out there), keep in mind that there are some glaring omissions in it's functionality that (AFAIK) no one is able to get around programmatically. For example, you can't access (or create, update, or delete, obvi) Deposits or Transfers.

Intuit has promised reporting features, but who knows...

http://stackoverflow.com/questions/19455750/quickbooks-online-api-financial-data
