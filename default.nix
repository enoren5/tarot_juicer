

with import <nixpkgs> { };

pkgs.mkShell {
  name = "impurePythonEnv";
  buildInputs = [
    uv

    # In order to compile any binary extensions the project's dependencies may
    # require, the following packages need to be installed locally:
    taglib
    openssl
    git
    libxml2
    libxslt
    libzip
    zlib
    postgresql_17
  ];

  # Create/sync the .venv (managed by uv, driven by pyproject.toml/uv.lock)
  # every time the shell is entered.
  shellHook = ''
    unset SOURCE_DATE_EPOCH
    uv sync
    source .venv/bin/activate
  '';
}
