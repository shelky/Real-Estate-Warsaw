# Real-Estate-Warsaw
The scripts to download and analyse apartments for sale in Warsaw

At this point there are two scrapers finding the apartment ads for two districts: Praga Południe and Bielany

get_ads_pp.py
downloads ads from gumtree.pl which were added in Praga Południe district section within last 24 hours and meet the custom filter settings
and then exports them to the apartments_praga_poludnie.cvs table.

get_ads_bielany.pl
downloads ads from gumtree.pl which were added in Bielany district section within last 24 hours and meet the custom filter settings
and then exports them to the apartments_bielany.cvs table.

GUI_scripts.py
Opens basic GUI to view ads from apartments_praga_poludnie.cvs file which have a flag "not seen".
After inspection one can mark some ads as "seen" and they will no longer be visible in GUI.
They will still be accesible from .csv file.

GUI_scripts_bielany.py
Opens basic GUI to view ads from apartments_bielany.csv which have a flag "not seen".
After inspection one can mark some ads as "seen" and they will no longer be visible in GUI.
They will still be accesible from .csv file.

WSscripts.py
Main library of the project

