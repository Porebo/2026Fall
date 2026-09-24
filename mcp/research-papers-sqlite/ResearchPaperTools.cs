using System.ComponentModel;
using System.Text.Json;
using System.Text.RegularExpressions;
using Microsoft.Data.Sqlite;
using ModelContextProtocol.Server;

[McpServerToolType]
public sealed class ResearchPaperTools
{
    private const int DefaultRowLimit = 100;
    private const int MaximumRowLimit = 1_000;
    private static readonly Regex Identifier = new(@"^[A-Za-z_][A-Za-z0-9_]*$", RegexOptions.CultureInvariant);

    private readonly SqliteConnectionFactory _connections;

    public ResearchPaperTools(SqliteConnectionFactory connections) => _connections = connections;

    [McpServerTool, Description("List the tables and views in the local research papers SQLite database.")]
    public Task<string> ListTables(CancellationToken cancellationToken) =>
        ExecuteQueryAsync("SELECT name, type FROM sqlite_master WHERE type IN ('table', 'view') AND name NOT LIKE 'sqlite_%' ORDER BY type, name;", DefaultRowLimit, cancellationToken);

    [McpServerTool, Description("Describe a table or view in the local research papers SQLite database.")]
    public Task<string> DescribeTable(
        [Description("The table or view name.")] string table,
        CancellationToken cancellationToken = default)
    {
        if (!Identifier.IsMatch(table))
        {
            throw new ArgumentException("The table name must be a simple SQLite identifier.", nameof(table));
        }

        return ExecuteQueryAsync($"PRAGMA table_info(\"{table}\");", MaximumRowLimit, cancellationToken);
    }

    [McpServerTool, Description("Execute one SQL statement against the local research papers SQLite database. This tool has full read, write, delete, and schema-administration access. Query results are capped at 1,000 rows.")]
    public Task<string> ExecuteSql(
        [Description("One SQLite SQL statement, including SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER, DROP, or PRAGMA.")] string sql,
        [Description("Maximum number of rows to return, from 1 to 1,000.")] int maxRows = DefaultRowLimit,
        CancellationToken cancellationToken = default)
    {
        if (string.IsNullOrWhiteSpace(sql))
        {
            throw new ArgumentException("A SQL statement is required.", nameof(sql));
        }

        return ExecuteQueryAsync(sql, Math.Clamp(maxRows, 1, MaximumRowLimit), cancellationToken);
    }

    private async Task<string> ExecuteQueryAsync(string sql, int maxRows, CancellationToken cancellationToken)
    {
        await using var connection = _connections.Create();
        await connection.OpenAsync(cancellationToken);
        await using var command = connection.CreateCommand();
        command.CommandText = sql;
        await using var reader = await command.ExecuteReaderAsync(cancellationToken);

        if (reader.FieldCount == 0)
        {
            return JsonSerializer.Serialize(new { rowsAffected = reader.RecordsAffected }, new JsonSerializerOptions { WriteIndented = true });
        }

        var columns = Enumerable.Range(0, reader.FieldCount).Select(reader.GetName).ToArray();
        var rows = new List<Dictionary<string, object?>>();
        while (rows.Count < maxRows && await reader.ReadAsync(cancellationToken))
        {
            var row = new Dictionary<string, object?>(StringComparer.OrdinalIgnoreCase);
            for (var index = 0; index < columns.Length; index++)
            {
                row[columns[index]] = await reader.IsDBNullAsync(index, cancellationToken) ? null : reader.GetValue(index);
            }
            rows.Add(row);
        }

        return JsonSerializer.Serialize(new { rowCount = rows.Count, truncated = rows.Count == maxRows, rows }, new JsonSerializerOptions { WriteIndented = true });
    }
}