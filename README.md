autopkg
=======

AutoPKG Recipes for sysadmins.

Several of my recipes use parent recipes from the following repos;

*  https://github.com/autopkg/recipes
*  https://github.com/autopkg/arubdesu-recipes
*  https://github.com/autopkg/dankeller-recipes
*  https://github.com/autopkg/hjuutilainen-recipes
*  https://github.com/autopkg/homebysix-recipes
*  https://github.com/autopkg/keeleysam-recipes
*  https://github.com/autopkg/n8felton-recipes
*  https://github.com/autopkg/scriptingosx-recipes

Just add em all...

```

autopkg repo-add https://github.com/autopkg/recipes https://github.com/autopkg/arubdesu-recipes https://github.com/autopkg/dankeller-recipes https://github.com/autopkg/hjuutilainen-recipes https://github.com/autopkg/homebysix-recipes https://github.com/autopkg/keeleysam-recipes https://github.com/autopkg/n8felton-recipes https://github.com/autopkg/scriptingosx-recipes

```

My SCCM Shared Processor requires the CMAppUtil binary which can be found in the macclient.dmg 

Unfortunately Microsoft only offer this download as an MSI file so you need to extract that first to get to the DMG file.

http://www.microsoft.com/en-au/download/details.aspx?id=39360