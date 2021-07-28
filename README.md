# Visualizing-Bread

A five part project for a university assingment in which the data visualization pipeline is implimented.

Data from the first 1000 recipes on allrecipes.com were scraped for data on the recipe name, the ingredients list, the rating of the recipe, and the url at which the recipe is located

Data cleaning was conducted through the use of whitelists and blacklists on the recipe name and ingredients, requireing that things such as 'flour' or 'dough' be found in the ingredients list, while recipes with names including 'noodles' or other non-bread items being excluded.

After cleaning, the data is placed into dataframes to allow the data to be visualized in a parallell lines plot. This technique lends itself well to the catogorical nature of the types of flour and leavening agent used. The rating of the recipe is used to map to a red-green color spectrum and used to color the lines representing the recipes, allowing users a more intuitive way on interpreting the quality of a recipe.

A visualization tool was created to assist working with the dataset, that allows a user to select the types of flour, leavening agents, and recipe ratings to be visualized. The visualization tool also allows a user to refine the results of a previous search.
The plot itself opens in the users prefered web browser, while information on the recipes visualized, such as the name, rating, and the webaddress it is located at are displayed in the visualization tool.
