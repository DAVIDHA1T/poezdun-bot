{ pkgs ? import <nixpkgs> {} }:

let
  myPython = pkgs.python3.withPackages (ps: [
    ps.aiogram
    ps.python-dotenv
  ]);
in
pkgs.mkShell {
  name = "aiogram-env";
  
  packages = [
    myPython
  ];

  shellHook = ''
    echo "Aiogram development environment activated!"
  '';
}
