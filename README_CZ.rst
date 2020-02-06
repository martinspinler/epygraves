Program Graves
==============

Autor: Martin Špinler <martin.spinler@gmail.com>

Verze: 0.0.1

Určeno pro: Andulici Koudelici

Základní informace
------------------

Cílem programu je zjednodušit postup při vyhledávání společných epigenetických znaků kosterního materiálu v rámci archeologického výzkumu.

Vstup programu
--------------

Vstupem je jeden či více datových souborů ve formátu CSV v následujícím formátu:

::

 name;nazev_hrobu1;nazev_hrobu2;nazev_hrobu3...
 nazev_vlastnosti1;hodnota_vlastnosti1_pro_hrob1,hodnota_vlastnosti1_pro_hrob_2;hodnota_vlastnosti1_pro_hrob_3...
 nazev_vlastnosti2;hodnota_vlastnosti2_pro_hrob1,hodnota_vlastnosti2_pro_hrob_2;hodnota_vlastnosti2_pro_hrob_3...
 nazev_vlastnosti3;hodnota_vlastnosti3_pro_hrob1,hodnota_vlastnosti3_pro_hrob_2;hodnota_vlastnosti3_pro_hrob_3...
 ...


hodnota_vlastnosti může nabývat těchto hodnot (bez nebo s uvozovkami):

====    =====================================================================================================================
Znak    Význam
====    =====================================================================================================================
\-      unilaterální znak není přítomen
1       unilaterální znak je přítomen
0       přítomnost unilaterálního znak nebylo možné rozhodnout
-1      bilaterální znak není přítomen na levé straně, je přítomen na pravé straně
1-      bilaterální znak je přítomen na levé straně, není přítomen na pravé straně
0,1     přítomnost bilaterálního znaku na levé straně nebylo možné rozhodnout, je přítomen na pravé straně
0-1     přítomnost bilaterálního znaku na levé straně nebylo možné rozhodnout, není přítomen na pravé straně
11      bilaterální znak je přítomen na levé i na pravé straně
-10     bilaterální znak není přítomen na levé straně, přítomnost bilaterálního znaku na pravé straně nebylo možné rozhodnout
10      bilaterální znak je přítomen na levé straně, přítomnost bilaterálního znaku na pravé straně nebylo možné rozhodnout
====    =====================================================================================================================

Pro jméno sloupce (místo nazev_hrobuX) může být jedenkrát použit nadpis 'freq'.
V tom případě se tento sloupec použije jako výchozí frekvence pro příslušné vlastnosti, viz níže.

Instalace a spuštění
--------------------

Samotný program se nijak neinstaluje, ale potřebuje ke svému běhu prostředí Python, jehož instalátor lze stáhnout např zde: https://www.python.org/ftp/python/3.7.0/python-3.7.0.exe

Po instalaci prostředí Python je možné spustit program pomocí souboru graves.py podobně jako jiný program.

Program je vytvořen nikoliv jako grafické prostředí ale jako konzolová aplikace, proto jeho výstupem je text v okně terminálu.

Chování
-------

Pokud programu není předložen nějaký konkrétní CSV soubor, pokusí se načíst soubor "graves.csv" v aktuálním adresáři.
Následně se z něho pokusí načíst data. Případné chyby ohlásí a místo chybných hodnot doplní znakem "0" (viz tabulka výše).
Pokud existuje sloupec s názvem 'freq', použije jeho hodnoty jako referenční frekvence. V opačném případě frekvence dopočítá z aktuální datové sady.

Případný výpočet frekvence je prováděn podle metody "veleminsky", je možné jednoduše naprogramovat jiný výpočet.

Další krok je vytvoření párů, což znamená matematickou kombinaci. Pro každý pár je vypočítán koeficient potencionálu příbuznosti jako aritmetický průměr frekvencí společných znaků.
Páry jsou následně seřazeny podle tohoto koeficientu.

Nakonec je vytvořen CSV soubor obsahující vypočítané (nebo vstupní) frekvence a CSV soubor obsahující všechny páry s jejich koeficienty.

Známé problémy
--------------

- Není ověřena korektnost výstupních frekvencí a koeficientů potenciálu příbuznosti.

Historie verzí
--------------

Verze 0.0.1 (beta)

  - první veřejná testovací verze
