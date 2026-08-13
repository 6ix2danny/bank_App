import { useEffect, useState } from "react";
import * as api from "../api";
import type { Transaction } from "../types";

export default function TransactionsPage() {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [startDate, setStartDate] = useState("");
  const [type, setType] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const [fromAccountId, setFromAccountId] = useState("");
  const [toAccountId, setToAccountId] = useState("");
  const [amount, setAmount] = useState("");
  const [transferring, setTransferring] = useState(false);

  async function load() {
    setLoading(true);
    setError(null);
    try {
      const data = await api.listTransactions({
        start_date: startDate || undefined,
        type: type || undefined,
      });
      setTransactions(data);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load transactions");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function handleTransfer(e: React.FormEvent) {
    e.preventDefault();
    setTransferring(true);
    setError(null);
    try {
      await api.transfer({
        from_account_id: Number(fromAccountId),
        to_account_id: Number(toAccountId),
        amount: Number(amount),
      });
      setFromAccountId("");
      setToAccountId("");
      setAmount("");
      await load();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Transfer failed");
    } finally {
      setTransferring(false);
    }
  }

  return (
    <div>
      <h2>Transactions</h2>
      {error && <p className="error">{error}</p>}

      <form
        className="filters"
        onSubmit={(e) => {
          e.preventDefault();
          load();
        }}
      >
        <input
          type="date"
          value={startDate}
          onChange={(e) => setStartDate(e.target.value)}
        />
        <input
          placeholder="Type (e.g. TRANSFER)"
          value={type}
          onChange={(e) => setType(e.target.value)}
        />
        <button type="submit">Apply</button>
      </form>

      {loading ? (
        <p>Loading...</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Id</th>
              <th>From</th>
              <th>To</th>
              <th>Amount</th>
              <th>Type</th>
              <th>Status</th>
              <th>Created</th>
            </tr>
          </thead>
          <tbody>
            {transactions.map((t) => (
              <tr key={t.id}>
                <td>{t.id}</td>
                <td>{t.from_account_id}</td>
                <td>{t.to_account_id}</td>
                <td>${t.amount.toFixed(2)}</td>
                <td>{t.type}</td>
                <td>{t.status}</td>
                <td>{new Date(t.created_at).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      <h3>New Transfer</h3>
      <form className="create-form" onSubmit={handleTransfer}>
        <input
          placeholder="From account id"
          type="number"
          value={fromAccountId}
          onChange={(e) => setFromAccountId(e.target.value)}
          required
        />
        <input
          placeholder="To account id"
          type="number"
          value={toAccountId}
          onChange={(e) => setToAccountId(e.target.value)}
          required
        />
        <input
          placeholder="Amount"
          type="number"
          step="0.01"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
          required
        />
        <button type="submit" disabled={transferring}>
          {transferring ? "Transferring..." : "Transfer"}
        </button>
      </form>
    </div>
  );
}
