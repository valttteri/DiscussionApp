## Tietokannat ja Web-ohjelmointi, syksy 2023

Tämän projektin aihe on keskustelusovellus.

#### Lopullinen palautus

Projektini aihe on keskustelusovellus. Sovelluksesta löytyy keskustelukanavia, joilla käyttäjät voivat jutella erilaisista asioista.
Käyttäjät voivat luoda uusia kanavia, sekä keskusteluita kanaville. Omia keskusteluita voi muokata ja poistaa. Keskusteluihin voi jättää kommentteja.
Käyttäjät voivat myös luoda ryhmäkeskusteluita, joihin vain tietyt henkilöt pääsevät käsiksi. Sovellukseen voi luoda oman käyttäjän, 
jonka jälkeen voi kirjautua sisään ja ulos nappia painamalla. Ylläpitäjiin ei päde käyttäjäkohtaiset rajoitukset. He voivat poistaa
poistaa minkä tahansa kommentin, keskustelun tai kanavan. Sovelluksen rakenne:

Etusivu
- Etusivulla näkyy kaikki sovellukseen luodut keskustelut
- Keskustelun kommentteja pääsee lukemaan kuvaketta klikkaamalla
- Jos käyttäjä on kirjautunut sisään, siitä näkyy maininta sivun yläosassa
- Sivun ylänurkasta löytyy hakutoiminto, jonka avulla voi etsiä yksittäisiä keskusteluita tai kommentteja

Kanavat
- Tällä sivulla näkyy lista sovelluksen keskustelukanavista
- Jokaisen kanavan kohdalla näkyy, montako keskustelua se sisältää ja milloin se on viimeksi ollut aktiivinen
- Kanavan keskusteluita voi mennä lukemaan kanavan nimeä klikkaamalla
- Käyttäjä voi luoda uusia kanavia, mutta vain ylläpitäjä voi poistaa niitä
- Sivun ylänurkasta löytyy sama hakutoiminto kuin etusivulta

Omat keskustelut
- Sivulla on lista ryhmäkeskusteluista, joiden jäsen käyttäjä on
- Käyttäjä voi luoda tai poistaa ryhmäkeskusteluja

Info
- Sivulla näkyy muutama tilasto sovelluksesta sekä sovelluksen kommentoiduin keskustelu

Sovelluksessa on keskustelukanavia, joilla käyttäjät voivat keskustella erilaisista asioista. Sovellukseen voi tehdä oman
käyttäjän, jonka jälkeen voi luoda keskustelukanavia, keskusteluita ja kommentteja. Käyttäjät voivat poistaa ja muokata omia keskustelui
Sovelluksen etusivulla on keskusteluketjuja, joissa käsitellään erilaisia aiheita. Kun on luonut sovellukseen käyttäjän, on mahdolista luoda keskusteluita ja
lisätä niihin kommentteja. Lähtökohtana on, että valmis sovellus tulee täyttämään kurssisivulla mainitut vaatimukset. Jos aikaa jää, niin toteutan sovellukseen lisää ominaisuuksia.

Sovellusta ei voi testata tuotannossa. Testausohjeet

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

