{
  description = "amsatop template. This flakes is only for creating a devshell (makes Pablo happy and allows it to run on his computer 🥶)";

  inputs.nixpkgs = {
    url = "github:nixos/nixpkgs/nixos-unstable?shallow=1";
  };

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";  # or "aarch64-darwin" etc. depending on your system
      pkgs = import nixpkgs {
        inherit system; 
        config.allowUnfree = true;
      };
    in {
      devShells.${system}.default = pkgs.mkShell {
        buildInputs = [ pkgs.uv ];
      };
    };
}
