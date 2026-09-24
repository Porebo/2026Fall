# Research Papers SQLite MCP

This stdio MCP server provides full administrative access to `research_papers.db`.

## Setup

Build the server once after cloning or changing its source:

```powershell
dotnet build mcp/research-papers-sqlite/ResearchPapersSqliteMcp.csproj
```

Then start `research-papers-sqlite` from the VS Code MCP view. Its configuration in `.vscode/mcp.json` provides the absolute database path automatically.

## Tools

- `list_tables`
- `describe_table`
- `execute_sql`

The database opens in SQLite read/write mode. `execute_sql` can run one SQL statement with full data and schema privileges, including `INSERT`, `UPDATE`, `DELETE`, `CREATE`, `ALTER`, and `DROP`. Query results are capped at 1,000 rows.