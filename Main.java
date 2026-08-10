
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.Scanner;


public class Main {

    static Scanner sc = new Scanner(System.in);

    static int customerCounter = 1;
    static int accountCounter = 1;

    // Using a Map<username, User>. This lets me look up a user directly by
    // key in O(1) (constant time) time instead of O(n) (linear time), and it will prevent
    // duplicate usernames since map keys are unique.
    static Map<String, User> usersByUsername = new HashMap<>();

    // Static initializer block: seeds my in-memory "database" with test data
    static {

        // Implementing Admin as a genuine User in the map, not a hardcoded if-check.
        // This means adding more admins later, or changing the admin password,
        // doesn't require touching the login logic at all.
        Admin admin = new Admin("admin", "admin123");
        usersByUsername.put(admin.getUsername(), admin);

        Customer daniel = new Customer(customerCounter++, "Daniel", new ArrayList<>(), "daniel", "daniel123");
        Customer dan = new Customer(customerCounter++, "Dan", new ArrayList<>(), "dan", "dan123");
        Customer danny = new Customer(customerCounter++, "Danny", new ArrayList<>(), "danny", "danny123");

        usersByUsername.put(daniel.getUsername(), daniel);
        usersByUsername.put(dan.getUsername(), dan);
        usersByUsername.put(danny.getUsername(), danny);
    }


    public static void main(String[] args) {
        welcome();

       
        // login() will return an Optional<User> instead of a String like
        // "admin" / "validation_failed" / username. Optional makes it explicit
        // in the return type itself that login might fail — the caller is
        // forced to handle the "empty" case, rather than relying on us
        // remembering to compare against a specific magic string.
        Optional<User> loggedInUser = login();

        if (loggedInUser.isEmpty()) {
            System.out.println("Validation Failed");
            return; // stop here instead of falling through to a dashboard
        }

        loggedInUser.get().showDashboard();
    }

    // Prompts for "username password", looks the username up in the map,
    // and checks the password. Returns Optional.empty() if anything doesn't match.
    private static Optional<User> login() {
        System.out.println("Please enter username and password, space separated");
        String enteredUsernamePassword = sc.nextLine();

        String[] usernamePassword = enteredUsernamePassword.split(" ");
        // Basic safety check: if the user didn't type two space-separated words,
        // treat it as a failed login instead of throwing an exception.
        if (usernamePassword.length < 2) {
            return Optional.empty();
        }

        String username = usernamePassword[0];
        String password = usernamePassword[1];

        // Direct map lookup instead of looping through every user
        User candidate = usersByUsername.get(username);

        // If no such username exists, or the password doesn't match, fail
        if (candidate == null || !candidate.getPassword().equals(password)) {
            return Optional.empty();
        }

        // Wrap the matched user in an Optional to signal a successful login
        return Optional.of(candidate);
    }

    private static void welcome() {
        System.out.println("Welcome to Daniel's Digital Bank");
    }

  // Shared helper: safely reads an integer from the console.
    // Package-private static so Customer/Admin can call Main.readInt().
    static int readInt() {
        String input = sc.nextLine().trim();
        try {
            return Integer.parseInt(input);
        } catch (NumberFormatException e) {
            System.out.println("(Invalid number entered, using 0)");
            return 0;
        }
    }
}

// Base class for anyone who can log in. Fields are now private with getters
// (better encapsulation than exposing raw public fields), and it declares
// an abstract showDashboard() method that every subclass must implement.
abstract class User {
    private String username;
    private String password;

    public User(String username, String password) {
        this.username = username;
        this.password = password;
    }

    public String getUsername() {
        return username;
    }

    public String getPassword() {
        return password;
    }


    // Each subclass (Admin, Customer) implements this differently.
    // This replaces the if(loginResult.equals("admin")) ... else ...
    public abstract void showDashboard();
}


class Customer extends User {
    private int id;
    private String name;
    private List<Account> accounts;
 
    public Customer(int id, String name, List<Account> accounts, String username, String password) {
        super(username, password);
        this.id = id;
        this.name = name;
        this.accounts = accounts;
    }
 
    public int getId() {
        return id;
    }
 
    public void setId(int id) {
        this.id = id;
    }
 
    public String getName() {
        return name;
    }
 
    public void setName(String name) {
        this.name = name;
    }
 
    public List<Account> getAccounts() {
        return accounts;
    }
 
    public void setAccounts(List<Account> accounts) {
        this.accounts = accounts;
    }
 

    @Override
    public void showDashboard() {
        System.out.println("Welcome customer, " + name);
 
        boolean running = true;
        while (running) {
            System.out.println("\n--- Customer Menu ---");
            System.out.println("1. View My Accounts");
            System.out.println("2. Add Account");
            System.out.println("3. Check Balance");
            System.out.println("4. Add Interest to an Account");
            System.out.println("5. Logout");
            System.out.print("Choose an option: ");
 
            String choice = Main.sc.nextLine().trim();
 
            switch (choice) {
                case "1":
                    viewAccounts();
                    break;
                case "2":
                    addAccount();
                    break;
                case "3":
                    checkBalance();
                    break;
                case "4":
                    addInterestToAccount();
                    break;
                case "5":
                    System.out.println("Logging out...");
                    running = false;
                    break;
                default:
                    System.out.println("Invalid option, please try again.");
            }
        }
    }
 
    private void viewAccounts() {
        if (accounts.isEmpty()) {
            System.out.println("You have no accounts yet.");
            return;
        }
        System.out.println("Your accounts:");
        for (Account acc : accounts) {
            System.out.println("  ID: " + acc.getId()
                    + " | Type: " + acc.getAccountType()
                    + " | Balance: " + acc.getBalance());
        }
    }
 
    private void addAccount() {
        System.out.print("Enter account type (checking/savings): ");
        String type = Main.sc.nextLine().trim().toLowerCase();
 
        System.out.print("Enter starting balance: ");
        int startingBalance = Main.readInt();
 
        Account newAccount;
        if (type.equals("savings")) {
            newAccount = new SavingsAccount();
        } else {
            newAccount = new CheckingAccount();
        }
 
        newAccount.setId(Main.accountCounter++);
        newAccount.setBalance(startingBalance);
        accounts.add(newAccount);
 
        System.out.println("Account created with ID " + newAccount.getId());
    }
 
    private void checkBalance() {
        System.out.print("Enter account ID: ");
        int id = Main.readInt();
 
        Account account = findAccountById(id);
        if (account == null) {
            System.out.println("No account with that ID found on your profile.");
            return;
        }
        System.out.println("Balance for account " + id + ": " + account.getBalance());
    }
 
    private void addInterestToAccount() {
        System.out.print("Enter account ID: ");
        int id = Main.readInt();
 
        Account account = findAccountById(id);
        if (account == null) {
            System.out.println("No account with that ID found on your profile.");
            return;
        }
 
        // Polymorphic call: runs CheckingAccount's 2% or SavingsAccount's 3%
        // depending on the account's real type.
        double updatedBalance = account.addInterest();
        account.setBalance((int) updatedBalance);
        System.out.println("Interest applied. New balance: " + account.getBalance());
    }
 
    private Account findAccountById(int id) {
        for (Account acc : accounts) {
            if (acc.getId() == id) {
                return acc;
            }
        }
        return null;
    }
 
    public String toString() {
        return "Customer{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", accounts=" + accounts +
                '}';
    }
}
 
class Admin extends User {
 
    public Admin(String username, String password) {
        super(username, password);
    }
 

    @Override
    public void showDashboard() {
        System.out.println("Welcome Admin");
        boolean running = true;
 
        while (running) {
            System.out.println("\n--- Admin Menu ---");
            System.out.println("1. View All Customers");
            System.out.println("2. Add Customer");
            System.out.println("3. Delete Customer");
            System.out.println("4. Update Customer Name");
            System.out.println("5. View All Accounts (all customers)");
            System.out.println("6. Logout");
            System.out.print("Choose an option: ");
 
            String choice = Main.sc.nextLine().trim();
 
            switch (choice) {
                case "1":
                    viewAllCustomers();
                    break;
                case "2":
                    addCustomer();
                    break;
                case "3":
                    deleteCustomer();
                    break;
                case "4":
                    updateCustomerName();
                    break;
                case "5":
                    viewAllAccounts();
                    break;
                case "6":
                    System.out.println("Logging out...");
                    running = false;
                    break;
                default:
                    System.out.println("Invalid option, please try again.");
            }
        }
    }
 
    private void viewAllCustomers() {
        boolean any = false;
        for (User u : Main.usersByUsername.values()) {
            // Only print actual Customer entries, skip Admin accounts
            if (u instanceof Customer c) {
                any = true;
                System.out.println("  ID: " + c.getId()
                        + " | Name: " + c.getName()
                        + " | Username: " + c.getUsername()
                        + " | # Accounts: " + c.getAccounts().size());
            }
        }
        if (!any) {
            System.out.println("No customers found.");
        }
    }
 
    private void addCustomer() {
        System.out.print("Enter new customer's name: ");
        String name = Main.sc.nextLine().trim();
 
        System.out.print("Enter new username: ");
        String username = Main.sc.nextLine().trim();
 
        System.out.print("Enter new password: ");
        String password = Main.sc.nextLine().trim();
 
        Customer newCustomer = new Customer(Main.customerCounter++, name, new ArrayList<>(), username, password);
        // Because Admin/Customer share the same map, adding here makes the
        // new customer able to log in immediately - no separate "users" list to sync.
        Main.usersByUsername.put(username, newCustomer);
 
        System.out.println("Customer added with ID " + newCustomer.getId());
    }
 
    private void deleteCustomer() {
        System.out.print("Enter customer ID to delete: ");
        int id = Main.readInt();
 
        String usernameToRemove = null;
        for (User u : Main.usersByUsername.values()) {
            if (u instanceof Customer c && c.getId() == id) {
                usernameToRemove = c.getUsername();
                break;
            }
        }
 
        if (usernameToRemove == null) {
            System.out.println("No customer with that ID found.");
            return;
        }
 
        Main.usersByUsername.remove(usernameToRemove);
        System.out.println("Customer " + id + " deleted.");
    }
 
    private void updateCustomerName() {
        System.out.print("Enter customer ID to update: ");
        int id = Main.readInt();
 
        Customer toUpdate = null;
        for (User u : Main.usersByUsername.values()) {
            if (u instanceof Customer c && c.getId() == id) {
                toUpdate = c;
                break;
            }
        }
 
        if (toUpdate == null) {
            System.out.println("No customer with that ID found.");
            return;
        }
 
        System.out.print("Enter new name: ");
        String newName = Main.sc.nextLine().trim();
        toUpdate.setName(newName);
 
        System.out.println("Customer " + id + " updated.");
    }
 
    private void viewAllAccounts() {
        boolean any = false;
        for (User u : Main.usersByUsername.values()) {
            if (u instanceof Customer c) {
                for (Account acc : c.getAccounts()) {
                    any = true;
                    System.out.println("  Customer: " + c.getName()
                            + " | Account ID: " + acc.getId()
                            + " | Type: " + acc.getAccountType()
                            + " | Balance: " + acc.getBalance());
                }
            }
        }
        if (!any) {
            System.out.println("No accounts exist yet across any customer.");
        }
    }
}
 
abstract class Account {
    private int id;
    private int balance;
 
    abstract double addInterest();
    abstract String getAccountType();
 
    public int getId() {
        return id;
    }
 
    public void setId(int id) {
        this.id = id;
    }
 
    public int getBalance() {
        return balance;
    }
 
    public void setBalance(int balance) {
        this.balance = balance;
    }
}
 
class CheckingAccount extends Account {
    double addInterest() {
        // add 2% to current balance and return the new total
        return getBalance() * 1.02;
    }
 
    String getAccountType() {
        return "CheckingAccount";
    }
}
 
class SavingsAccount extends Account {
    double addInterest() {
        // add 3% to current balance and return the new total
        return getBalance() * 1.03;
    }
 
    String getAccountType() {
        return "SavingsAccount";
    }
}