# Research Papers SQLite MCP

This stdio MCP server provides full administrative access to `research_papers.db`.

## Setup

Build the server once after cloning or changing its source:

```powershell
dotnet build mcp/research-papers-sqlite/ResearchPapersSqliteMcp.csproj
```

Then start `research-papers-sqlite` from the Copilot MCP view. The root `.mcp.json` uses paths relative to the workspace root, so it works from any checkout location.

Use this MCP server's tools instead of the deprecated `@dbclient` chat participant. The extension participant itself is not automatically migrated; use a publisher-provided replacement or disable it after confirming this server covers your database workflow.

## Tools

- `list_tables`
- `describe_table`
- `execute_sql`

The database opens in SQLite read/write mode. `execute_sql` can run one SQL statement with full data and schema privileges, including `INSERT`, `UPDATE`, `DELETE`, `CREATE`, `ALTER`, and `DROP`. Query results are capped at 1,000 rows.