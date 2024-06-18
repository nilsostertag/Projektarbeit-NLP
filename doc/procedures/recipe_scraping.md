# Recipe Scraping

### Tags
- Struktur\
Rezept-Tags befinden sich in den a-Elementen des Recupe-Tags divs.
    ```HTML
    <div class="ds-box recipe tags">
        <!--Filtern nach Rezept-Tags-->
        <a>Asien</a>
    </div>
    ```

### Autor
- Struktur\
Nutzername des Autors befindet sich in einem Span-Element in a-Element des recipe-author-divs.
    ```HTML
    <div class="... recipe-author">
        <a>
            <span>Autorname<span>
        </a>
    </div>
    ```