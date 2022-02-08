# krita-ml

For now, the plugin works in Linux environment and only when `Krita` is not installed in an isolated environment (`Flatpak`, `Snap`, `AppImage`, etc)

This requirement will be removed when we are able to install python packages directly using the plugin. For now `Krita` uses the python packages installed in global environment.

Steps:

1. Install `Krita`
2. Install also the optional dependency `python-pyqt5` for Python Plugins
3. Open the `Krita` resource directory by going to `Settings->Configure Krita`. In the `Resource` tab of `General` section, open the `Resource Folder` location in File Browser. Lets say the resource folder is `$resource_folder`
4. Clone [Krita-ML repository](https://github.com/wistic/krita-ml.git) and extract it.
5. Copy `kritaml` directory, `kritaml.action`  file and `kritaml.desktop` file of cloned repository to `$resource_folder/pykrita`
6. Download [Monodepth model weights](https://github.com/intel-isl/DPT/releases/download/1_0/dpt_hybrid-midas-501f0c75.pt) and place it in `$resource_folder/pykrita/kritaml/features/monodepth/` directory. Name the file as `weights.pt`. Finally the file will be placed as `$resource_folder/pykrita/kritaml/features/monodepth/weights.pt`
7. Download [Dehazer model weights](https://github.com/MayankSingal/PyTorch-Image-Dehazing/blob/master/snapshots/dehazer.pth) and place it in `$resource_folder/pykrita/kritaml/features/dehaze` directory. Name the file as `weights.pt`. Finally the file will be placed as `$resource_folder/pykrita/kritaml/features/dehaze/weights.pt`
8. Restart `Krita`
9. Go to `Settings->Configure Krita`. Enable `Krita ML Plugin` in the `Python Plugin Manager`.

Now the plugin in enabled and all options should be available in `Tool->Scripts`
