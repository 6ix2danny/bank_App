// Mirrors app/models/schemas.py

export interface Branch {
  id: number;
  name: string;
  address: string;
}

export interface Account {
  id: number;
  customer_id: number;
  branch_id: number;
  account_type: "checking" | "savings";
  balance: number;
}

export interface Customer {
  id: number;
  name: string;
  username: string;
  is_active: boolean;
}

export interface CustomerWithAccounts extends Customer {
  accounts: Account[];
}

export interface Transaction {
  id: number;
  from_account_id: number;
  to_account_id: number;
  amount: number;
  type: string;
  status: string;
  created_at: string;
}

export interface CustomerCreate {
  name: string;
  username: string;
  password: string;
}

export interface AccountCreate {
  customer_id: number;
  branch_id: number;
  account_type: "checking" | "savings";
  balance: number;
}

export interface BranchCreate {
  name: string;
  address: string;
}

export interface TransactionCreate {
  from_account_id: number;
  to_account_id: number;
  amount: number;
}
