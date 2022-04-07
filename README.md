# krita-ml

For now, the plugin works in Linux environment and only when `Krita` is not installed in an isolated environment (`Flatpak`, `Snap`, `AppImage`, etc)

This requirement will be removed when we are able to install python packages directly using the plugin. For now `Krita` uses the python packages installed in global environment.

Steps:

1. Install `Krita`.
2. Install the optional dependency `python-pyqt5` for Python Plugins.
3. Download the [plugin](https://github.com/wistic/krita-ml/releases/download/Alpha/kritaml.zip) and [`requirements.txt`](https://github.com/wistic/krita-ml/releases/download/Alpha/requirements.txt) file from releases section of this repo.
4. Install all the necessary pip packages by running `pip install -r requirements.txt`.
5. Install the plugin by using [Python Plugin Importer.](https://docs.krita.org/en/user_manual/python_scripting/install_custom_python_plugin.html#using-python-plugin-importer). 

Now the plugin in enabled and all options should be available in `Tool->Scripts->Krita-ML`.
