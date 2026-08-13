import { useState } from "react";
import "./App.css";
import CustomersPage from "./pages/CustomersPage";
import AccountsPage from "./pages/AccountsPage";
import BranchesPage from "./pages/BranchesPage";
import TransactionsPage from "./pages/TransactionsPage";

const TABS = ["Customers", "Accounts", "Branches", "Transactions"] as const;
type Tab = (typeof TABS)[number];

function App() {
  const [tab, setTab] = useState<Tab>("Customers");

  return (
    <div className="app">
      <header>
        <h1>Daniel's Digital Bank</h1>
        <nav>
          {TABS.map((t) => (
            <button
              key={t}
              className={t === tab ? "active" : ""}
              onClick={() => setTab(t)}
            >
              {t}
            </button>
          ))}
        </nav>
      </header>
      <main>
        {tab === "Customers" && <CustomersPage />}
        {tab === "Accounts" && <AccountsPage />}
        {tab === "Branches" && <BranchesPage />}
        {tab === "Transactions" && <TransactionsPage />}
      </main>
    </div>
  );
}

export default App;
