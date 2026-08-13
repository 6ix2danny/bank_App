import type {
  Account,
  AccountCreate,
  Branch,
  BranchCreate,
  Customer,
  CustomerCreate,
  CustomerWithAccounts,
  Transaction,
  TransactionCreate,
} from "./types";

const BASE_URL = import.meta.env.VITE_API_BASE_URL as string;

export class ApiError extends Error {
  status: number;
  constructor(status: number, message: string) {
    super(message);
    this.status = status;
  }
}

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new ApiError(res.status, body.detail ? JSON.stringify(body.detail) : res.statusText);
  }
  if (res.status === 204) return undefined as T;
  return res.json() as Promise<T>;
}

function toQuery(params: Record<string, string | number | undefined>): string {
  const entries = Object.entries(params).filter(([, v]) => v !== undefined && v !== "");
  if (entries.length === 0) return "";
  return "?" + new URLSearchParams(entries as [string, string][]).toString();
}

// ---- Customers ----

export function listCustomers(params: {
  search?: string;
  sort_by?: string;
  order?: string;
  min_accounts?: number;
} = {}): Promise<CustomerWithAccounts[]> {
  return request(`/customers${toQuery(params)}`);
}

export function getCustomer(id: number): Promise<CustomerWithAccounts> {
  return request(`/customers/${id}`);
}

export function createCustomer(payload: CustomerCreate): Promise<Customer> {
  return request("/customers", { method: "POST", body: JSON.stringify(payload) });
}

export function deactivateCustomer(id: number): Promise<void> {
  return request(`/customers/${id}`, { method: "DELETE" });
}

// ---- Accounts ----

export function listAccounts(params: {
  account_type?: string;
  min_balance?: number;
  max_balance?: number;
  customer_id?: number;
  branch_id?: number;
  sort_by?: string;
  order?: string;
} = {}): Promise<Account[]> {
  return request(`/accounts${toQuery(params)}`);
}

export function createAccount(payload: AccountCreate): Promise<Account> {
  return request("/accounts", { method: "POST", body: JSON.stringify(payload) });
}

export function addInterest(id: number): Promise<Account> {
  return request(`/accounts/${id}/add-interest`, { method: "POST" });
}

export function deleteAccount(id: number): Promise<void> {
  return request(`/accounts/${id}`, { method: "DELETE" });
}

// ---- Branches ----

export function listBranches(): Promise<Branch[]> {
  return request("/branches");
}

export function createBranch(payload: BranchCreate): Promise<Branch> {
  return request("/branches", { method: "POST", body: JSON.stringify(payload) });
}

// ---- Transactions ----

export function listTransactions(params: {
  start_date?: string;
  type?: string;
} = {}): Promise<Transaction[]> {
  return request(`/transactions${toQuery(params)}`);
}

export function transfer(payload: TransactionCreate): Promise<Transaction> {
  return request("/transactions/transfer", { method: "POST", body: JSON.stringify(payload) });
}
