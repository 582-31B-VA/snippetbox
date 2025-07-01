# Snippetbox

This semester, we'll be building a web application called Snippetbox,
which lets people paste and share snippets of text — a bit like
[Pastebin] or GitHub's [Gists].

Our application will start off super simple, with just one web page.
Then with each course we'll build it up step-by-step until a user can
save and view snippets via the app. This will take us through topics
like how to structure a project, routing requests, working with a
database, processing forms and displaying dynamic data safely. Then
we'll add user accounts, and restrict the application so that only
registered users can create snippets. This will take us through more
advanced topics like session management, user authentication and
middleware.

To run the application on you local machine, clone this repository, `cd`
into the `snippetbox` directory, and use the following command:

```sh
uv run flask --app snippetbox run --debug
```

Each step will be recorded in a separate commit. You can use `git pull`
to fetch the newest version of the application. To view past versions,
use `git log` and `git checkout`.

[Pastebin]: https://pastebin.com/
[Gists]: https://gist.github.com/
