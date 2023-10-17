## Tietokannat ja Web-ohjelmointi, syksy 2023

Tämä on Valtteri Aholan repositorio kurssille Tietokannat ja Web-ohjelmointi. Projektini aihe on yksi kurssisivulla mainituista esimerkeistä, eli keskustelusovellus.
Sovelluksen etusivulla on keskusteluketjuja, joissa käsitellään erilaisia aiheita. Kun on luonut sovellukseen käyttäjän, on mahdolista luoda keskusteluita ja
lisätä niihin kommentteja. Lähtökohtana on, että valmis sovellus tulee täyttämään kurssisivulla mainitut vaatimukset. Jos aikaa jää, niin toteutan sovellukseen lisää ominaisuuksia.

#### Ensisijaiset ominaisuudet (kurssisivua lainaten):
- Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
- Käyttäjä näkee sovelluksen etusivulla listan alueista sekä jokaisen alueen ketjujen ja viestien määrän ja viimeksi lähetetyn viestin ajankohdan.
- Käyttäjä voi luoda alueelle uuden ketjun antamalla ketjun otsikon ja aloitusviestin sisällön.
- Käyttäjä voi kirjoittaa uuden viestin olemassa olevaan ketjuun.
- Käyttäjä voi muokata luomansa ketjun otsikkoa sekä lähettämänsä viestin sisältöä. Käyttäjä voi myös poistaa ketjun tai viestin.
- Käyttäjä voi etsiä kaikki viestit, joiden osana on annettu sana.
- Ylläpitäjä voi lisätä ja poistaa keskustelualueita.
- Ylläpitäjä voi luoda salaisen alueen ja määrittää, keillä käyttäjillä on pääsy alueelle.

#### Mahdolliset lisäominaisuudet:
- Ylläpitäjä voi antaa bannit käyttäjälle tai poistaa käyttäjän tilin kokonaan.
- Käyttäjät voivat antaa tykkäyksiä muiden käyttäjien kommenteille
- Käyttäjät voivat lisätä muita käyttäjiä kavereiksi
- Kaverit voivat lähettää toisilleen yksityisviestejä
- Käyttäjä voi nappia painamalla päästä tarkastelemaan omaa profiiliaan. Profiilissa näkyy tietoja käyttäjästä, esim. keskusteluketjut, joissa käyttäjä on mukana,
  lähetettyjen viestien määrä, saatujen tykkäyksien määrä yms.

#### Välipalautus 2
Keskustelusovelluksen yllä listatuista ensisijaisista ominaisuuksista on toteutettu jollain tasolla jokainen paitsi salaiset alueet. Sen toteuttaminen on vasta alussa. 
Tällä hetkellä sovellukseen voi siis luoda käyttäjän, ja osallistua eri aihepiirien keskusteluihin. Toistaiseksi vain ylläpitäjät voivat luoda uusia keskustelukanavia sovellukseen.
Käyttäjälle voi antaa ylläpitäjän oikeudet komentoriviltä asettamalla kohdan 'admin' arvoksi TRUE.

#### Välipalautus 3

Tällä hetkellä sovellus on viimeistelyä vaille valmis. Jokainen ensisijainen ominaisuus on toteutettu.\
Tässä on sovelluksen testausohjeet:

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

