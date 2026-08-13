import { useEffect, useState } from "react";
import * as api from "../api";
import type { Account } from "../types";

export default function AccountsPage() {
  const [accounts, setAccounts] = useState<Account[]>([]);
  const [accountType, setAccountType] = useState("");
  const [minBalance, setMinBalance] = useState("");
  const [maxBalance, setMaxBalance] = useState("");
  const [customerId, setCustomerId] = useState("");
  const [branchId, setBranchId] = useState("");
  const [sortBy, setSortBy] = useState("");
  const [order, setOrder] = useState<"asc" | "desc">("asc");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const [newCustomerId, setNewCustomerId] = useState("");
  const [newBranchId, setNewBranchId] = useState("");
  const [newAccountType, setNewAccountType] = useState<"checking" | "savings">("checking");
  const [newBalance, setNewBalance] = useState("0");
  const [creating, setCreating] = useState(false);

  async function load() {
    setLoading(true);
    setError(null);
    try {
      const data = await api.listAccounts({
        account_type: accountType || undefined,
        min_balance: minBalance ? Number(minBalance) : undefined,
        max_balance: maxBalance ? Number(maxBalance) : undefined,
        customer_id: customerId ? Number(customerId) : undefined,
        branch_id: branchId ? Number(branchId) : undefined,
        sort_by: sortBy || undefined,
        order,
      });
      setAccounts(data);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load accounts");
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
      await api.createAccount({
        customer_id: Number(newCustomerId),
        branch_id: Number(newBranchId),
        account_type: newAccountType,
        balance: Number(newBalance),
      });
      setNewCustomerId("");
      setNewBranchId("");
      setNewBalance("0");
      await load();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to create account");
    } finally {
      setCreating(false);
    }
  }

  async function handleAddInterest(id: number) {
    setError(null);
    try {
      await api.addInterest(id);
      await load();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to add interest");
    }
  }

  async function handleDelete(id: number) {
    setError(null);
    try {
      await api.deleteAccount(id);
      await load();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to delete account");
    }
  }

  return (
    <div>
      <h2>Accounts</h2>
      {error && <p className="error">{error}</p>}

      <form
        className="filters"
        onSubmit={(e) => {
          e.preventDefault();
          load();
        }}
      >
        <select value={accountType} onChange={(e) => setAccountType(e.target.value)}>
          <option value="">Any type</option>
          <option value="checking">Checking</option>
          <option value="savings">Savings</option>
        </select>
        <input
          placeholder="Min balance"
          type="number"
          value={minBalance}
          onChange={(e) => setMinBalance(e.target.value)}
        />
        <input
          placeholder="Max balance"
          type="number"
          value={maxBalance}
          onChange={(e) => setMaxBalance(e.target.value)}
        />
        <input
          placeholder="Customer id"
          type="number"
          value={customerId}
          onChange={(e) => setCustomerId(e.target.value)}
        />
        <input
          placeholder="Branch id"
          type="number"
          value={branchId}
          onChange={(e) => setBranchId(e.target.value)}
        />
        <select value={sortBy} onChange={(e) => setSortBy(e.target.value)}>
          <option value="">Sort by...</option>
          <option value="balance">Balance</option>
          <option value="id">Id</option>
          <option value="account_type">Type</option>
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
              <th>Customer</th>
              <th>Branch</th>
              <th>Type</th>
              <th>Balance</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {accounts.map((a) => (
              <tr key={a.id}>
                <td>{a.id}</td>
                <td>{a.customer_id}</td>
                <td>{a.branch_id}</td>
                <td>{a.account_type}</td>
                <td>${a.balance.toFixed(2)}</td>
                <td>
                  <button onClick={() => handleAddInterest(a.id)}>Add Interest</button>{" "}
                  <button onClick={() => handleDelete(a.id)}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      <h3>New Account</h3>
      <form className="create-form" onSubmit={handleCreate}>
        <input
          placeholder="Customer id"
          type="number"
          value={newCustomerId}
          onChange={(e) => setNewCustomerId(e.target.value)}
          required
        />
        <input
          placeholder="Branch id"
          type="number"
          value={newBranchId}
          onChange={(e) => setNewBranchId(e.target.value)}
          required
        />
        <select
          value={newAccountType}
          onChange={(e) => setNewAccountType(e.target.value as "checking" | "savings")}
        >
          <option value="checking">Checking</option>
          <option value="savings">Savings</option>
        </select>
        <input
          placeholder="Initial balance"
          type="number"
          value={newBalance}
          onChange={(e) => setNewBalance(e.target.value)}
        />
        <button type="submit" disabled={creating}>
          {creating ? "Creating..." : "Create Account"}
        </button>
      </form>
    </div>
  );
}
