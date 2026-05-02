import Database from "better-sqlite3";
import { resolve } from "path";

let _db: Database.Database | null = null;

export function useDb(): Database.Database {
  if (!_db) {
    const config = useRuntimeConfig();
    const dbPath = resolve(config.databasePath);
    _db = new Database(dbPath, { readonly: true });
    _db.pragma("journal_mode = WAL");
  }
  return _db;
}
