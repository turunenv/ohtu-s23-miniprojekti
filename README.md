# Miniproject

[![GHA_workflow_badge](https://github.com/turunenv/ohtu-s23-miniprojekti/workflows/CI/badge.svg)](https://github.com/turunenv/ohtu-s23-miniprojekti/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/turunenv/ohtu-s23-miniprojekti/graph/badge.svg?token=ZYGSDB5DQM)](https://codecov.io/gh/turunenv/ohtu-s23-miniprojekti)


## Backlogs

- [Backlogs](https://github.com/users/turunenv/projects/1)
- [Task estimation and burndown chart](https://docs.google.com/spreadsheets/d/1_CVzRfBNQlAJu8JO0la84PiaUmfVOdazKIZoOWZOVVI/edit#gid=0)

## Definition of Done

- Requirements met.
- Python test coverage at a decent level
- Pushed to main branch and main branch is not broken.

## Loppuraportti
- [Linkki loppuraporttiin](https://docs.google.com/document/d/1Mq3A44wzgUl_FAoOyu5s4ZrCxR_VRWEi0aB5gCgkTKI/edit?usp=sharing)

## Installation

1. Install poetry:
```
poetry install
```

2. Enter virtual environment with the command:
```
poetry shell
```

3. Run initialization procedures with the command:
```
python3 src/build.py
```

4. Start the app with the command:
```
python3 src/index.py
```

## Manual

### Running the app

You can run the app in the virtual environment.

Enter virtual environment with the command:
```
poetry shell
```

Start the app with the command:
```
python3 src/index.py
```

### Commands

The app will open to the starting menu:
```
Type "help" to list commands and their descriptions
Command:
```

If you type ***help*** the app prints the following:
```
To EXIT the program simply press enter in the starting menu
add:      Add a new reference by provinding the required information
list:     List all stored references
delete:   Delete a reference using its reference key
tag:      Enter a tag name and a reference key to tag a reference
search:   Enter tag name to search tagged references
cancel:   Return to the starting menu
file:     Enter a file name to create a .bib file of all references
doi:      Add a new reference using DOI identifier or full DOI URL
Valid inputs:
   year:      Year must consist of only numbers
   volume:    Volume must consist of only numbers
   pages:     Pages must consist of numbers separated by "--"
```

#### Listing references

If you type ***list*** the app will print a table of added references.

#### Adding a reference

If you type ***add*** you can add a new reference.
```
Type "cancel" to cancel
Give source type:
```
Currently the supported reference types are book, article and inproceedings.
If you type ***cancel*** before a reference is added, you can cancel adding a reference and return to the starting menu.

The required information for a book are:

- Reference key
- Author
- Title
- Year
- Publisher

The required information for an article are:

- Reference key
- Author
- Title
- Journal
- Year
- Volume
- Pages

The required information for an inproceedings are:

- Reference key
- Author
- Title
- Booktitle
- Year

Once a reference is successfully added, the app will print:
```
ADDED!
```

#### Adding a reference with DOI

If you type ***doi*** you can add a new reference by giving it's DOI identifier or full URL.
```
Type "cancel" to cancel
Give ref_key for this reference:
```
After you have given a valid reference key, give the reference's DOI identifier or full URL. Keep in mind not all references have a DOI.

The app prints the reference's information and asks for confirmation. Write a capital or lowercase y to confirm.
```
y
```

#### Deleting a reference

If you type ***delete*** you can delete an existing reference.
```
Type "cancel" to cancel
Give source reference key:
```
To delete a reference you need the correct reference key. You can check by using the command ***list*** to see all sources and their reference keys.

After giving the key the app asks for confimation. To confirm write a capital or lowercase y.
```
y
```
Any other value will cancel the deletion

Once a reference is succesfully deleted, the app will print:
```
DELETED!
```

#### Tagging a file

If you type ***tag*** you can give an existing reference a tag
```
Type "cancel" to cancel
Give tag name:
```
To give a tag to a reference you need the correct reference key. You can check by using the command ***list*** to see all sources and their reference keys.

After giving the key the app asks for confirmation. To confirm write a capital or lowercase y.
```
y
```

#### Searching with a tag

If you type ***search*** you can search for references that have the same tag.
```
Type "cancel" to cancel
Give tag name:
```
The app will print all references with the tag in question.

#### Creating a BibTex -file

If you type ***file*** you can create a bibtex file containing your references.
```
Give the name of file:
```
Give the file a suitable name. For example my_references.

The app prints a message containing how many references were saved to a BibTex-file
```
2 references succesfully written to my_references.bib
```

#### Closing the app

You can close the app by pressing enter in the starting menu:
```
Type "help" to list commands and their descriptions
Command:
```
