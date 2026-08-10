
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.Scanner;


public class Main {

    static Scanner sc = new Scanner(System.in);
    static int counter = 1;

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

        // Create customers directly; each Customer IS-A User, so it goes
        // straight into the same map used for login lookups.
        Customer daniel = new Customer(counter++, "Daniel", new ArrayList<>(), "daniel", "daniel123");
        Customer dan = new Customer(counter++, "Dan", new ArrayList<>(), "dan", "dan123");
        Customer danny = new Customer(counter++, "Danny", new ArrayList<>(), "danny", "danny123");

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


        // We just ask the logged-in User to show its own dashboard.
        // Because showDashboard() is overridden differently in Admin and
        // Customer, the correct menu appears automatically. Essentially, this is
        // polymorphism doing the routing instead of an if/else chain.
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
    // branching..
    public abstract void showDashboard();
}
