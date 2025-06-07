{
  description = "Blender MCP development environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            uv
            python312
            git
          ];

          shellHook = ''
            echo "Blender MCP development environment"
            echo "Available tools:"
            echo "  - uv (Python package manager)"
            echo "  - python3.12"
            echo "  - git"
          '';
        };
      });
}