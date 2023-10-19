## Testausohje

Sovellusta ei voi testata tuotannossa. Testausohjeet:

1. Kloonaa repositorio koneellesi ja luo projektikansioon .env-tiedosto.
```
~/ $ git clone https://github.com/valttteri/Tsoha2023.git
~/ $ cd Tsoha2023
~/Tsoha2023/ $ touch .env
```

2. Määritä .env-tiedoston sisältö seuraavanlaiseksi:
```
DATABASE_URL='tietokannan-paikallinen-osoite' esim. DATABASE_URL='postgresql://<username>:<password>@localhost:5432/<database-name>'
SECRET_KEY='salainen-avain' esim. SECRET_KEY='many-characters-here-32-in-total'
```

3. Luo virtuaaliympäristö ja aktivoi se.
```
~/Tsoha2023/ $ python -m venv venv
```
Linux:
```
~/Tsoha2023/ $ source venv/bin/activate
```
Windows:
```
~/Tsoha2023/ $ source venv/Scripts/activate
```
4. Asenna sovelluksen riippuvuudet.
```
~/Tsoha2023/ $ pip install -r ./requirements.txt
```

5. Siirry src-kansioon ja määritä tietokannan skeema esim. seuraavalla tavalla. Tarkista, että tietokanta jota käytät on tyhjä.
Skeemaan sisältyy käyttäjät NormalUser ja AdminUser joista molempien salasana on 1234.
```
~/Tsoha2023/ $ cd src
~/src/ $ psql -U <username> -d <database-name> -f schema.sql
```

6. Käynnistä sovellus.
```
~/src/ $ flask run
```
