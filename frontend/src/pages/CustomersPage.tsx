import { useEffect, useState } from "react";
import * as api from "../api";
import type { CustomerWithAccounts } from "../types";

export default function CustomersPage() {
  const [customers, setCustomers] = useState<CustomerWithAccounts[]>([]);
  const [search, setSearch] = useState("");
  const [sortBy, setSortBy] = useState("");
  const [order, setOrder] = useState<"asc" | "desc">("asc");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const [name, setName] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [creating, setCreating] = useState(false);

  async function load() {
    setLoading(true);
    setError(null);
    try {
      const data = await api.listCustomers({
        search: search || undefined,
        sort_by: sortBy || undefined,
        order,
      });
      setCustomers(data);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load customers");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function handleCreate(e: React.FormEvent) {
    e.preventDefault();
    setCreating(true);
    setError(null);
    try {
      await api.createCustomer({ name, username, password });
      setName("");
      setUsername("");
      setPassword("");
      await load();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to create customer");
    } finally {
      setCreating(false);
    }
  }

  async function handleDeactivate(id: number) {
    setError(null);
    try {
      await api.deactivateCustomer(id);
      await load();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to deactivate customer");
    }
  }

  return (
    <div>
      <h2>Customers</h2>
      {error && <p className="error">{error}</p>}

      <form
        className="filters"
        onSubmit={(e) => {
          e.preventDefault();
          load();
        }}
      >
        <input
          placeholder="Search name or username"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <select value={sortBy} onChange={(e) => setSortBy(e.target.value)}>
          <option value="">Sort by...</option>
          <option value="name">Name</option>
          <option value="username">Username</option>
          <option value="id">Id</option>
        </select>
        <select value={order} onChange={(e) => setOrder(e.target.value as "asc" | "desc")}>
          <option value="asc">Asc</option>
          <option value="desc">Desc</option>
        </select>
        <button type="submit">Apply</button>
      </form>

      {loading ? (
        <p>Loading...</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Id</th>
              <th>Name</th>
              <th>Username</th>
              <th>Active</th>
              <th>Accounts</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {customers.map((c) => (
              <tr key={c.id}>
                <td>{c.id}</td>
                <td>{c.name}</td>
                <td>{c.username}</td>
                <td>{c.is_active ? "Yes" : "No"}</td>
                <td>
                  {c.accounts.length === 0
                    ? "—"
                    : c.accounts
                        .map((a) => `#${a.id} ${a.account_type} $${a.balance.toFixed(2)}`)
                        .join(", ")}
                </td>
                <td>
                  {c.is_active && (
                    <button onClick={() => handleDeactivate(c.id)}>Deactivate</button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      <h3>New Customer</h3>
      <form className="create-form" onSubmit={handleCreate}>
        <input
          placeholder="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
        <input
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <input
          placeholder="Password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit" disabled={creating}>
          {creating ? "Creating..." : "Create Customer"}
        </button>
      </form>
    </div>
  );
}
