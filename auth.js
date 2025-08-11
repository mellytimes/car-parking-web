let auth0Client = null;

const configureClient = async () => {
  auth0Client = await auth0.createAuth0Client({
    domain: "dev-6iyz7zfcbxikkoik.us.auth0.com",
    clientId: "xxzaucZxtqwdwv6ZcNjEhAKTUSdZpXej",
    authorizationParams: {
      redirect_uri: 'http://127.0.0.1:5500'
    }
  });
};

window.onload = async () => {
  await configureClient();

  console.log("Auth0 client configured.");

  // Handle Auth0 redirect after login
  const query = window.location.search;
  if (query.includes("code=") && query.includes("state=")) {
    try {
      await auth0Client.handleRedirectCallback();
      window.history.replaceState({}, document.title, "/");
      window.location.href = "Web_1920__7.html";
      return;
    } catch (e) {
      console.error("Auth0 callback error:", e);
    }
  }

  // Now that auth0Client is ready, attach event listeners here:

  document.getElementById("login-btn").addEventListener("click", async () => {
    await auth0Client.loginWithRedirect();
  });

  document.getElementById("signup-link").addEventListener("click", async (e) => {
    e.preventDefault();
    await auth0Client.loginWithRedirect({
      authorizationParams: {
        screen_hint: "signup"
      }
    });
  });

// AFTER
document.getElementById("google-login-btn").addEventListener("click", async () => {
  console.log("Google button clicked!"); // <-- ADD THIS LINE
  await auth0Client.loginWithRedirect({
    authorizationParams: {
      connection: "google-oauth2"
    }
  });
});

  document.getElementById("facebook-login-btn").addEventListener("click", async () => {
    await auth0Client.loginWithRedirect({
      authorizationParams: {
        connection: "facebook"
      }
    });
  });
};
