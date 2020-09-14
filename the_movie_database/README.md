# TMDB API v4 - Auth

This simple `express` server is an example of using [The Movie Database API version 4's auth routes](https://developers.themoviedb.org/4/getting-started/authorization). Their latest version of the API tries to make a clearer distinction between auth for an application and auth for accessing account information.

This server goes through TMDB's auth for accessing account information by:

- Accessing an endpoint with the Applcation's Read-Access Token to generate a Request Token
- Redirecting the user to the TMDB's site so they can sign in and approve the Request Token.
- Accessing an endpoint with the approved Request Token and the Application Token to generate an Access Token.
- Accessing an endpoint to retrieve a array of all lists created by a user (even private lists since we have an account-approved access token).
- Accessing an endpoint to receive details information for each list created by the user, including details on private lists.

To start this auth process, start `server.js` and head to `/request` on whichever port the server is running on. It will redirect you to The Movie Database to sign in and verify the request token, and then redirect you back to the server at route `/lists`. You may have to alter the `redirect_to` URL within the `/request` route if your server is not running on port 3000.

## Future Ideas

TMDB is a great site for creating lists, but it doesn't inform you which lists a movie is a member of on a movie's details page. I'm curious if a Chrome Extension could be made that recognizes when you're looking at a detail page for a movie, accesses your lists, and appended the names of lists that the movie is a member of onto the page in the 'facts' box. This way you can easily see where you've listed/tagged a particular movie at a glance.