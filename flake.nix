{
  description = "Python project template";

  inputs = {
    # Latest stable channel (fully cached for darwin) for the generic dev tools.
    nixpkgs.url = "github:nixos/nixpkgs/nixos-26.05";
    # Astral toolchain (uv/ruff/ty) is deliberately tracked from unstable to stay
    # current; these are small Rust binaries cached on unstable, not a build trap.
    nixpkgs-unstable.url = "github:nixos/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";

    # Used for shell.nix
    flake-compat = {
      url = "github:edolstra/flake-compat";
      flake = false;
    };
  };

  outputs = {
    self,
    nixpkgs,
    nixpkgs-unstable,
    flake-utils,
    ...
  } @ inputs: let
    overlays = [
      (final: prev: {
        unstable = import nixpkgs-unstable {
          inherit (prev) system;
        };
      })
    ];

    systems = ["x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin"];
  in
    flake-utils.lib.eachSystem systems (
      system: let
        pkgs = import nixpkgs {
          inherit overlays system;
        };
      in {
        formatter = pkgs.alejandra;

        devShells.default = pkgs.mkShell {
          name = "py-dev";
          nativeBuildInputs = [
            # Astral toolchain — uv manages Python, no nix Python needed
            pkgs.unstable.uv
            pkgs.unstable.ruff
            pkgs.unstable.ty

            # Dev tools
            pkgs.lefthook
            pkgs.jq
            pkgs.ripgrep
          ];
          shellHook =
            ''
              echo "uv $(uv --version)"
            ''
            + (pkgs.lib.optionalString pkgs.stdenv.hostPlatform.isDarwin ''
              unset SDKROOT
              unset DEVELOPER_DIR
              export PATH=/usr/bin:$PATH
            '');
        };

        devShell = self.devShells.${system}.default;
      }
    );
}
