{ pkgs ? import <nixpkgs> {} }:

let
  # Create a custom Python environment containing aiogram
  myPython = pkgs.python3.withPackages (ps: [
    ps.aiogram
  ]);
in
pkgs.mkShell {
  name = "aiogram-env";
  
  # Put the custom Python environment into the shell packages
  packages = [
    myPython
  ];

  shellHook = ''
    echo "Aiogram development environment activated!"
  '';
}
