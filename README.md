# OT_Hra_Jindra - GDD

**Autor**: Ivan Jindra

**Vybraná téma**: Color as a gameplay feature

---
## **1. Úvod**
Ako finálny projekt ku záverečnej skúške bola navrhnutá hra na tému témou Color as a gameplay feature, tému spĺňa v tom že hra má charakter zbierania predmetov rôznej farby, kde farba je podstatná pritom kedy sa predmety môžu a mali by sa zbierať.

### **1.1 Inšpirácia**
<ins>**Všetky plošinovky**</ins>

Ako príklad vyberám hru Super Mario, ako základ všetkých plošinoviek. Je to hra kde sa postavička musí dostať, zo začiatku mapy na koniec mapy bez toho aby stratil priveľa životov. Pri vymýšľaní hry som sa vyslovene ale neinšpiroval žiadnou špecifickou hrou, ako prichádzali nápady tak prichádzali featur-y

<p align="center">
  <img src="https://github.com/ivanos2234/OT_Hra_Jindra/blob/main/Super_mario.jpg" alt="super_mario">
  <br>
  <em>Super Mario - ukážka</em>
</p>

### **1.2 Herný zážitok**
Cieľom hry je zbierať po mape ovocie rovnakej farby akú vám práve hra (v ľavom hornom rohu) ukazuje, toto ovocie sa po každom úspešnom pozbieraní zmení, a navýši sa skóre, po nesprávnom sa skóre zníži, ktoré ale nie je vašim finálnym hodnotením to je počet pozbieraných ovocí, ale hra má háčik každú určenú časovú jednotku sa vám odpočíta skóre o daný decrement, a keď nemáte dostatok skóre po odpočte (a vlastne hocikedy v hre) hra končí, snažil som sa vutvoriť hru kde collectibl-y budú vlastne aj prekážky a v neskorších fázach (ako sa hra aj zrýchluje každ=ym odočtom) budú ovocia akurát nesprávnej farby pózovať prekážku keďže zníženie bodov za zobranie nesprávneho ovocia môže viesť k rýchlej prehre, vďaka extenzívnemu testovaniu boli vaiceré hodnoty nastavené na dufám že príjemný hrací zážitok

### **1.3 Vývojový softvér**
- **Pygame-CE**: zvolený programovací jazyk.
- **Intellij IDEA 2024.2.3**: vybrané IDE.
- **Tiled 1.10.2**: grafický nástroj na vytváranie levelov.
- **Itch.io**: zdroj grafických assetov a zvukov do hry.

---
## **2. Koncept**

### **2.1 Prehľad hry**
V pravidelnom časovom intervale sa na mape na vopred predurčených lokáciach spawnujú rôzne ovocia (vždy tak aby bolo od každého aspoň jedno), a hráč ovláda postavu a snaží sa vyhnúť nesprávnym ovociam (všetky typy ktoré práve nemá pozbierať) a nájsť to správne, hráč bol obdarený nekonečným počtom skokov kvôli lepšej hrateľnosti

### **2.2 Interpretácia témy (Color as a gameplay feature)**
**"Color as a gameplay feature"** - Hlavná herná mechanika je založená na zbieraní ovocia správnej farby, ovocia sú vybrané tak aby každé malo inú farbu a boli jednoducho rozoznateľné

### **2.3 Základné mechaniky**
- **Ovocie**: Vľavo hore má hráč k dispozícii jak current ovocie tak aj ovocie ktoré bude nasledovať po ňom, čiže je tu možnosť kombenia dvoch, troch a viacerých ovocií po sebe, pridáva to opať faktor strategizácie
- **Pevne stanovené miesta generovania ovocia**: ovocie na prednastavených miestach dodá hre istú predvídateľnosť, a hráč sa vďaka tomu po pár hraniach bude vedieť v leveloch lepšie orientovať
- **Nekonečno skokov**: hráč nemá vyslovene stanovený limit skokov čiže celú hru by ani nemusel pristať na zemi, je to dizajn v tom že vďaka nekonečnu skokov sa dá orientovať v bludiskách ktoré si hra v neskorších fázach pripraví

### **2.4 Návrh tried**
- **Game**: trieda, v ktorej sa bude nachádzať hlavná herná logika (menu-loop, game-loop, loadovanie assetov, ...).
- **Tilemap**: trieda v ktorej si načítam danú mapu a spawnpointy a tiež je v nej logika fyzických objektov tým že sa okolo hráča každý frame vyhľadávajú susedné políčka a collision sa porovnáva len na nich.
- **Player**: trieda reprezentujúca hráča, ovládanie hráča, vykreslenie postavy,  animáciu, gravitáciu a daný collision detection sa vykonáva v triede player.
- **Button**: trieda pre tlačítka ktoré sú v hlavnom menu

---
## **3. Grafika**

### **3.1 Interpretácia témy (Color as a gameplay feature)**
Pomocou assetov z itch.io, ako aj hudby, bol vytvorený na pohľad príjemný grafický dizajn. Boli vybrané štyri druhy ovocia ako bolo už spomenuté a asset hlavného hrdinu ktorý má idle, running, jumping a falling animácie.

<p align="center">
  <img src="https://github.com/ivanos2234/OT_Hra_Jindra/blob/main/Gameplay_picture.png" alt="Screen z hry">
  <br>
  <em>Ukážka screenu z rozohratej hry kde sú vidno všetky sprite-y</em>
</p>

### **3.2 Dizajn**
V hre boli použité assety z itch.io, konkrétne Pixel Adventure 1 (https://pixelfrog-assets.itch.io/pixel-adventure-1), všetky objekty v terrain, všetky políčka (tile) majú fyziku a vlastnosť zastaviť hráča. V hre sú zatiaľ len dva levely ale pridávanie nových levelov by v budúcnosti nemal priniesť problém.

<p align="center">
  <img src="https://github.com/ivanos2234/OT_Hra_Jindra/blob/main/level_1.png" alt="Prvý level">
  <br>
  <em>Ukážka prvého levelu</em>
</p>

---
## **4. Zvuk**

### **4.1 Hudba**
Hudba bola vybraná taká aby bola dosť akčná a vystihovala time pressure v hre, preto bola použitá hudba Arena Fight na loope z voľne dostupného zdroja (https://danistob.itch.io/sci-fi-adventure-music-pack)

### **4.2 Zvuky**
Zvuky v hre boli orientované skôr komickejšie, ku klasickému skoku a pickupu nesprávneho ovocia, bol pridaný mierne humorný pickup správneho ovocia ktorý bol zvlášť namixovaný, zvyšok bol zobraný z voľne dostupného zdroja free sound effectov (https://phoenix1291.itch.io/sound-effects-pack-2)

---
## **5. Herný zážitok**

### **5.1 Používateľské rozhranie**
Na rozhranie boli použité mierne poupravené tlačítka zo zdroju (https://joshua-briggs.itch.io/2d-64x16-pixel-button-pack), menu má dva levely možnosť opustiť hru a v hre má hráč možnosť vrátiť sa do hlavného menu

### **5.2 Ovládanie**
<ins>**Klávesnica**</ins>
- **ŠÍPKY DOPRAVA DOĽAVA**: pohyb hráča doprava a doľava.
- **ŠÍPKA HORE**: záhajenie skoku.
