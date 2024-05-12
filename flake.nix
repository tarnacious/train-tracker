{
  inputs = {
    nixpkgs.url = "nixpkgs/nixos-23.11";
    nixpkgs-unstable.url = "nixpkgs/master";
  };

  outputs = { self, ... }@inputs:
    let
      system = "x86_64-linux";
      pkgs = import inputs.nixpkgs {
        inherit system;
      };
      unstable = import inputs.nixpkgs-unstable {
        inherit system;
      };

      app = let
          mypkg = pkgs.stdenv.mkDerivation {
            name = "mypkg";
            src = self;
            installPhase = ''
              #echo "out", $out
              mkdir -p $out/
              cp -r ./* $out/
            '';
          };
          python = (unstable.python312.withPackages (python-pkgs: [
              python-pkgs.requests
              python-pkgs.sqlmodel
              python-pkgs.jinja2
            ]));
        in pkgs.writeShellApplication {
          name = "train-tracker";
          runtimeInputs = [
            python
          ];
          text = ''
            ${python}/bin/python ${mypkg}/run.py
          '';
        };
    in {
      packages.${system} = {
        default = app;
        train-tracker = app;
      };

      devShells.${system}.default = pkgs.mkShell {
        buildInputs = [
          (pkgs.sqlite.override { interactive=true; })
          unstable.python312
          unstable.python312Packages.requests
          unstable.python312Packages.sqlmodel
          unstable.python312Packages.jinja2
          unstable.python312Packages.pytest
          #pkgs.python312Packages.mypy
        ];
      };
    };
}
