export const redirectGoogleAuth = () => {
    const googleAuthUrl = 'https://accounts.google.com/o/oauth2/v2/auth';

    const options = {
        redirect_uri: 'http://localhost:8080/auth/google/callback', // Must match what you set in the Google Console
        client_id: '186610135245-8624gp66b4j4n5pm8q95nkc9gcv9r8f8.apps.googleusercontent.com', // Your Client ID
        access_type: 'offline', // To get a refresh token
        response_type: 'code',
        prompt: 'consent',
        scope: [
        'https://www.googleapis.com/auth/gmail.insert',
        'https://www.googleapis.com/auth/gmail.readonly',
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/gmail.send', // The permission you need
        ].join(' '),
    };

    // Format the options into a URL query string
    const qs = new URLSearchParams(options).toString();

    // Redirect the user to the Google login page
    window.location.href = `${googleAuthUrl}?${qs}`;
  };