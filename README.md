# socialSim
An HTN-based discrete step simulator.  Most domains are/will be social things.

## Documentation

Following the video tutorial [How to Document using Sphinx](https://www.youtube.com/playlist?list=PLE72UCmIe7T9HewaqCUhKqiMK3LxYStjy), 
I setup  `sphinx` for this project's documentation, which should be installed with the other project requirements. 
After installation, run

```commandline
sphinx-quickstart
```

and answer the questions to setup the documentation in the __docs__ directory. Note: hitting enter will 
accept the default value. Check the __docs__ directory to confirm all the expected files are there.

For the rest of this section, move to the __docs__ directory root. Next, we will install the theme for this project's 
documentation with:

```commandline
pip install sphinx-rtd-theme
```

Now, to view the documentation run:

```commandline
make html
cd build/html
open -a"Google Chrome" index.html
```

This example uses __Google Chrome__, but you can replace `Google Chrome` with the browser of your choice 
in the command above. This should open the documentation in this browser.

