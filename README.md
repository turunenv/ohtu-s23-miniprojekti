# Miniprojekti

![GHA_workflow_badge](https://github.com/turunenv/ohtu-s23-miniprojekti/workflows/CI/badge.svg)
[![codecov](https://codecov.io/gh/turunenv/ohtu-s23-miniprojekti/graph/badge.svg?token=ZYGSDB5DQM)](https://codecov.io/gh/turunenv/ohtu-s23-miniprojekti)


## Backlogit
- [Backlogit](https://github.com/users/turunenv/projects/1)
- [Taskien estimointi ja burndown kaavio](https://docs.google.com/spreadsheets/d/1_CVzRfBNQlAJu8JO0la84PiaUmfVOdazKIZoOWZOVVI/edit#gid=0)

# Definition of Done

- Requirements met.
- Python test coverage at a decent level
- Pushed to main branch and main branch is not broken.

## Asennus

1. Asenna poetry:
```
poetry install
```

2. Avaa virtuaaliympäristö komennolla:
```
poetry shell
```

3. Suorita vaadittavat alustustoimenpiteet komennolla:
```
python3 src/build.py
```

4. Käynnistä sovellus komennolla:
```
python3 src/index.py
```

## Käyttöohje

### Ohjelman suorittaminen

Ohjelman pystyy suorittamaan virtuaaliympäristössä.

Avaa virtuaaliympäristö komennolla:
```
poetry shell
```

Suorita ohjelma komennolla:
```
python3 src/index.py
```

### Komennot

Sovellus aukeaa näkymään:
```
Command (add or list)
```

Antamalla komennon ***add*** voit lisätä viitteen.
Sovellus pyytää seuraavia tietoja:

- Give source type eli viitteen tyyppi
- Add ref_key of the book eli viitteen avain
- Add author of the book eli kirjailijan nimi
- Add title of the book eli kirjan nimi
- Add year of the book eli kirjan julkaisuvuosi
- Add publisher of the book eli kirjan julkaisija

Antamalla komennon ***list*** sovellus antaa listan lisätyistä viitteistä.

Sovelluksen voi sulkea painamalla enteriä näkymässä:
```
Command (add or list)
```
