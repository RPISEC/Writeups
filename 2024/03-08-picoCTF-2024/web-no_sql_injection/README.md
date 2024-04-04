# No Sql Injection
### Web 200

> #### Description
> Can you try to get access to this website to get the flag?
> You can download the source here.
> Additional details will be available after launching your challenge instance.

For this challenge, we are given an app.tar.gz. We can extract the files within this tar file with the following command:

```tar -xvzf app.tar.gz```

We then see the app folder, and we take note of a few key things:

<ul>
    <li>The login is located in api/login, named route.ts</li>
    <li>route.ts depends on three files, models/user, util/database, and util/seed</li>
    <li>The email and password field route.ts are parsed as json if the user surrounds their username/password with {}</li>
    <li>The server reponds with the user information if we provide the correct password, otherwise it responds with a status 401 </li>
</ul>

Looking at the database file, we can see that this is using mongoose, for MongoDB. Knowing how to abuse this would be a good idea, and a quick Google search would do.

Looking at [link](https://berkegokmen1.medium.com/your-nodejs-app-is-probably-vulnerable-to-nosql-injection-attacks-69e6acba7b65), we can craft our own payload, with or without the username.
We can see that the user we need to target in the seed file, more notably we are given an email of joshiriya355@mumbama.com

For our username, we can use the email above, and for the password, we can craft the injection payload. Since "password: " is already filled out for us in route, we only need to inject the payload.
We can use the payload below

`{ "$ne": null }`

This tells mongoDB to look for a password where the password field itself isn't null, which will be true (our payload), so it returns the user.
We then can inspect the network traffic in order to find the response, and we are given the username, password, token of the user. 

The user's token resembles a base64 encoded strings, so using [Cyberchef](https://gchq.github.io/CyberChef/) we can decode it and get the flag.

`picoCTF{jBhD2y7XoNzPv_1YxS9Ew5qL0uI6pasql_injection_a2e0d9ef}`

