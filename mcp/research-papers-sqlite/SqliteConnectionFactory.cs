using Microsoft.Data.Sqlite;

public sealed class SqliteConnectionFactory
{
    public SqliteConnection Create()
    {
        var databasePath = Environment.GetEnvironmentVariable("RESEARCH_PAPERS_DB_PATH");
        if (string.IsNullOrWhiteSpace(databasePath))
        {
            throw new InvalidOperationException("The RESEARCH_PAPERS_DB_PATH environment variable is required.");
        }

        var builder = new SqliteConnectionStringBuilder
        {
            DataSource = databasePath,
            Mode = SqliteOpenMode.ReadWrite
        };
        return new SqliteConnection(builder.ConnectionString);
    }
}