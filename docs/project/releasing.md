# Releasing

Since cihai is used in production projects, breaking changes are deferred
until a major feature release.

## Version numbering

Given a current version of `0.36.0`:

- **0.36.0post0** -- post-release, packaging fix only
- **0.36.1** -- bugfix / security / tweak
- **0.37.0** -- new features or breaking changes

## Release checklist

1. Update `CHANGES` -- ensure every merged PR since the last tag is listed.
   Set the header to the new version and today's date. Keep the *unreleased*
   placeholder at the top.

2. Bump the version in `pyproject.toml` and `src/cihai/__about__.py`.

3. Commit and tag:

```console
$ git commit -m 'Tag v0.36.1'
```

```console
$ git tag v0.36.1
```

```console
$ git push && git push --tags
```

## Automated deployment

GitHub Actions detects the new tag and runs `uv build` followed by a push
to PyPI.

## Manual deployment

If CI is unavailable:

```console
$ uv build
```

```console
$ uv publish
```
